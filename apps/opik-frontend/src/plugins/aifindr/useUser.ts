import { Auth0ContextInterface, useAuth0 } from "@auth0/auth0-react";
import { User } from "./types";
import { ACCESS_TOKEN_KEY } from "@/constants/user";

type UserWithAuth0 = {data: User} & Auth0ContextInterface

export default function useUser(): UserWithAuth0 {
  const {user, ...auth0AuthData} = useAuth0();
  
  // Actualiza el token en localStorage cada vez que useUser es llamado
  if (auth0AuthData.isAuthenticated) {
    auth0AuthData.getAccessTokenSilently().then(token => {
      localStorage.setItem(ACCESS_TOKEN_KEY, token);
    });
  }
  const userResponse = {
    data: {
      defaultWorkspace: "", // TODO: Add default workspace
      email: user?.email || "",
      profileImages: {
        small: user?.picture || "",
        large: user?.picture || "",
      },
      userName: user?.name || "",
      loggedIn: auth0AuthData.isAuthenticated,
    },
    ...auth0AuthData,
  }
  return userResponse;
}
