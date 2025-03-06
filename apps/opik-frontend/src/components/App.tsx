import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { RouterProvider } from "@tanstack/react-router";
import { router } from "@/router";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/ui/toaster";
import { QueryParamProvider } from "use-query-params";
import { WindowHistoryAdapter } from "use-query-params/adapters/window";
import useCustomScrollbarClass from "@/hooks/useCustomScrollbarClass";
import { Auth0Provider } from '@auth0/auth0-react';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

// Declaración para TypeScript
declare global {
  interface Window {
    RUNTIME_CONFIG: {
      AUTH_DOMAIN: string;
      AUTH_CLIENT_ID: string;
      AUTH_AUDIENCE: string;
      AIFINDR_DOMAIN: string;
    };
  }
}

function App() {
  useCustomScrollbarClass();

  const auth0Config = {
    domain: window.RUNTIME_CONFIG?.AUTH_DOMAIN || import.meta.env.VITE_AUTH_DOMAIN || '',
    clientId: window.RUNTIME_CONFIG?.AUTH_CLIENT_ID || import.meta.env.VITE_AUTH_CLIENT_ID || '',
    authorizationParams: {
      redirect_uri: window.location.origin,
      audience: window.RUNTIME_CONFIG?.AUTH_AUDIENCE || import.meta.env.VITE_AUTH_AUDIENCE,
    },
  };

  return (
    <Auth0Provider {...auth0Config}>
      <QueryClientProvider client={queryClient}>
        <QueryParamProvider adapter={WindowHistoryAdapter}>
          <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
            <RouterProvider router={router} />
            <Toaster />
          </ThemeProvider>
        </QueryParamProvider>
      </QueryClientProvider>
    </Auth0Provider>
  );
}

export default App;
