package com.comet.opik.infrastructure.auth;

import java.net.URI;
import java.util.Base64;
import java.util.List;
import java.util.Optional;

import org.apache.commons.lang3.StringUtils;

import static com.comet.opik.api.AuthenticationErrorResponse.MISSING_API_KEY;
import static com.comet.opik.api.AuthenticationErrorResponse.MISSING_WORKSPACE;
import static com.comet.opik.api.AuthenticationErrorResponse.NOT_ALLOWED_TO_ACCESS_WORKSPACE;
import com.comet.opik.domain.ProjectService;
import com.comet.opik.infrastructure.AuthenticationConfig.UrlConfig;
import com.comet.opik.infrastructure.auth.CacheService.AuthCredentials;
import com.comet.opik.infrastructure.lock.LockService;
import com.comet.opik.infrastructure.lock.LockService.Lock;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.inject.Provider;
import jakarta.ws.rs.ClientErrorException;
import jakarta.ws.rs.InternalServerErrorException;
import jakarta.ws.rs.client.Client;
import jakarta.ws.rs.client.Entity;
import jakarta.ws.rs.core.Cookie;
import jakarta.ws.rs.core.HttpHeaders;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@RequiredArgsConstructor
@Slf4j
class RemoteAuthService implements AuthService {
    // AIFindr: constants
    // TODO: move this to a better place
    private static final String CAPABILITIES_CLAIM = "pgpt:capabilities";
    private static final String EVALUATIONS_CAPABILITY = "evaluations-view";

    private static final String USER_NOT_FOUND = "User not found";
    private final @NonNull Client client;
    private final @NonNull UrlConfig apiKeyAuthUrl;
    private final @NonNull UrlConfig uiAuthUrl;
    private final @NonNull Provider<RequestContext> requestContext;
    private final @NonNull CacheService cacheService;
    private final @NonNull LockService lockService;

    record AuthRequest(String workspaceName, String path) {
    }

    record AuthResponse(String user, String workspaceId) {
    }

    // AIFindr: add Auth0 support
    record Auth0Verification(AuthRequest authRequest, String apiKey) {
    }

    @JsonIgnoreProperties(ignoreUnknown = true)
    record Auth0SpecificResponse(String sub, String name) {
    }

    record ValidatedAuthCredentials(boolean shouldCache, String userName, String workspaceId) {
    }

    @Override
    public void authenticate(HttpHeaders headers, Cookie sessionToken, String path) {

        var currentWorkspaceName = getCurrentWorkspaceName(headers);

        if (currentWorkspaceName.isBlank()) {
            log.warn("Workspace name is missing");
            throw new ClientErrorException(MISSING_WORKSPACE, Response.Status.FORBIDDEN);
        } else if (ProjectService.DEFAULT_WORKSPACE_NAME.equalsIgnoreCase(currentWorkspaceName)) {
            log.warn("Default workspace name is not allowed");
            throw new ClientErrorException(NOT_ALLOWED_TO_ACCESS_WORKSPACE, Response.Status.FORBIDDEN);
        }

        if (sessionToken != null) {
            authenticateUsingSessionToken(sessionToken, currentWorkspaceName, path);
            requestContext.get().setWorkspaceName(currentWorkspaceName);
            return;
        }

        authenticateUsingApiKey(headers, currentWorkspaceName, path);
        requestContext.get().setWorkspaceName(currentWorkspaceName);
    }

    private String getCurrentWorkspaceName(HttpHeaders headers) {
        return Optional.ofNullable(headers.getHeaderString(RequestContext.WORKSPACE_HEADER))
                .orElse("");
    }

    private void authenticateUsingSessionToken(Cookie sessionToken, String workspaceName, String path) {
        try (var response = client.target(URI.create(uiAuthUrl.url()))
                .request()
                .accept(MediaType.APPLICATION_JSON)
                .cookie(sessionToken)
                .post(Entity.json(new AuthRequest(workspaceName, path)))) {

            AuthResponse credentials = verifyResponse(response, null);

            setCredentialIntoContext(credentials.user(), credentials.workspaceId());
            requestContext.get().setApiKey(sessionToken.getValue());
        }
    }

    private void authenticateUsingApiKey(HttpHeaders headers, String workspaceName, String path) {

        String apiKey = Optional.ofNullable(headers.getHeaderString(HttpHeaders.AUTHORIZATION))
                .orElse("");

        if (apiKey.isBlank()) {
            log.info("API key not found in headers");
            throw new ClientErrorException(MISSING_API_KEY, Response.Status.UNAUTHORIZED);
        }

        var lock = new Lock(apiKey, workspaceName);

        ValidatedAuthCredentials credentials = lockService.executeWithLock(
                lock,
                Mono.fromCallable(() -> validateApiKeyAndGetCredentials(workspaceName, apiKey, path))
                        .subscribeOn(Schedulers.boundedElastic()))
                .block();

        if (credentials.shouldCache()) {
            log.debug("Caching user and workspace id for API key");
            cacheService.cache(apiKey, workspaceName, credentials.userName(), credentials.workspaceId());
        }

        setCredentialIntoContext(credentials.userName(), credentials.workspaceId());
        requestContext.get().setApiKey(apiKey);
    }

    private ValidatedAuthCredentials validateApiKeyAndGetCredentials(String workspaceName, String apiKey, String path) {
        log.info("----------> 1");
        Optional<AuthCredentials> credentials = cacheService.resolveApiKeyUserAndWorkspaceIdFromCache(apiKey,
                workspaceName);

        log.info("----------> 2");
        if (credentials.isEmpty()) {
            log.info("----------> 3 {}", apiKeyAuthUrl.url());
            log.debug("User and workspace id not found in cache for API key");
            AuthRequest authRequest = new AuthRequest(workspaceName, path);
            try (var response = client.target(URI.create(apiKeyAuthUrl.url()))
                    .request()
                    .accept(MediaType.APPLICATION_JSON)
                    .header(HttpHeaders.AUTHORIZATION,
                            apiKey)
                    .post(Entity.json(authRequest))) {

                log.info("----------> 4 {}", response);
                Auth0Verification auth0Verification = apiKeyAuthUrl.isAuth0() ? new Auth0Verification(authRequest, apiKey) : null;
                AuthResponse authResponse = verifyResponse(response, auth0Verification);
                return new ValidatedAuthCredentials(true, authResponse.user(), authResponse.workspaceId());
            }
        } else {
            return new ValidatedAuthCredentials(false, credentials.get().userName(), credentials.get().workspaceId());
        }
    }

    private AuthResponse verifyResponse(Response response, Auth0Verification auth0Verification) {
        AuthResponse authResponse;
        log.info("----------> 5");
        if (response.getStatusInfo().getFamily() == Response.Status.Family.SUCCESSFUL) {
            // AIFindr: add Auth0 response support
            if (auth0Verification != null) {
                var responseData = response.readEntity(Auth0SpecificResponse.class);
                
                // Decode the JWT token to extract capabilities
                List<String> capabilities = extractCapabilitiesFromToken(auth0Verification.apiKey());
                log.debug("Extracted capabilities from token: {}", capabilities);

                if (!capabilities.contains(EVALUATIONS_CAPABILITY)) {
                    log.warn("User does not have Evaluations capability");
                    throw new ClientErrorException("User is not authorized to access evaluations", Response.Status.UNAUTHORIZED); 
                }
                
                // TODO: no workspace id yet
                authResponse = new AuthResponse(responseData.name(), auth0Verification.authRequest().workspaceName());
            } else {
                var responseData = response.readEntity(AuthResponse.class);
                authResponse = new AuthResponse(responseData.user(), responseData.workspaceId());
            }

            if (StringUtils.isEmpty(authResponse.user())) {
                log.warn("User not found");
                throw new ClientErrorException(USER_NOT_FOUND, Response.Status.UNAUTHORIZED);
            }

            return authResponse;
        } else if (response.getStatus() == Response.Status.UNAUTHORIZED.getStatusCode()
                || response.getStatus() == Response.Status.BAD_REQUEST.getStatusCode()) {
            throw new ClientErrorException(response.getStatusInfo().getReasonPhrase(), response.getStatus());
        } else if (response.getStatus() == Response.Status.FORBIDDEN.getStatusCode()) {
            // EM never returns FORBIDDEN as of now
            throw new ClientErrorException(NOT_ALLOWED_TO_ACCESS_WORKSPACE, Response.Status.FORBIDDEN);
        }

        log.error("Unexpected error while authenticating user, received status code: {}", response.getStatus());
        throw new InternalServerErrorException();
    }

    // AIFindr: Extract capabilities from token
    private List<String> extractCapabilitiesFromToken(String token) {
        try {
            // Remove "Bearer " prefix if it exists
            String actualToken = token.startsWith("Bearer ") ? token.substring(7) : token;
            
            // Split token into its parts (header, payload, signature)
            String[] parts = actualToken.split("\\.");
            if (parts.length < 2) {
                log.warn("Invalid JWT token format");
                return List.of();
            }

            // Decode the payload part
            String payload = new String(Base64.getUrlDecoder().decode(parts[1]));
            ObjectMapper mapper = new ObjectMapper();
            var claims = mapper.readTree(payload);
            
            // Extract the "pgpt:capabilities" claim
            if (claims.has(CAPABILITIES_CLAIM)) {
                return mapper.convertValue(
                    claims.get(CAPABILITIES_CLAIM),
                    mapper.getTypeFactory().constructCollectionType(List.class, String.class)
                );
            }
            
            return List.of();
        } catch (Exception e) {
            log.error("Error decoding JWT token", e);
            return List.of();
        }
    }

    private void setCredentialIntoContext(String userName, String workspaceId) {
        requestContext.get().setUserName(userName);
        requestContext.get().setWorkspaceId(workspaceId);
    }

}
