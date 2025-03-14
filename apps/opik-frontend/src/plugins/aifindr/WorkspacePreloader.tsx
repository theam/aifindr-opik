import {
  Link,
  Navigate,
  useMatchRoute,
  useParams,
} from "@tanstack/react-router";
import { MoveLeft } from "lucide-react";
import React from "react";

import Loader from "@/components/shared/Loader/Loader";
import useAppStore from "@/store/AppStore";
import Logo from "./Logo";
import useAllUserWorkspaces from "./useAllUserWorkspaces";
import useUser from "./useUser";
import { buildUrl } from "./utils";
import { useToast } from "@/components/ui/use-toast";

type WorkspacePreloaderProps = {
  children: React.ReactNode;
};

const WorkspacePreloader: React.FunctionComponent<WorkspacePreloaderProps> = ({
  children,
}) => {
  const { toast } = useToast();
  const { data: user, isLoading, loginWithRedirect } = useUser();
  const res = useAllUserWorkspaces({
    enabled: !!user?.loggedIn,
  });
  console.log("Res: ", res)

  const { data: workspaces, isLoading: isWorkspacesLoading, error: workspacesError } = res
  
  const matchRoute = useMatchRoute();
  const workspaceNameFromURL = useParams({
    strict: false,
    select: (params) => params["workspaceName"],
  });
  const isRootPath = matchRoute({ to: "/" });

  if (isLoading) {
    return <Loader />;
  }

  if (!user || !user.loggedIn) {
    loginWithRedirect({
      appState: { 
        returnTo: workspaceNameFromURL 
          ? `/${workspaceNameFromURL}` 
          : '/'
      }
    });
    return null;
  }

  if (isWorkspacesLoading) {
    return <Loader />;
  }

  if (!workspaces || workspacesError) {    
    toast({
      title: "Error loading workspaces",
      description: workspacesError?.message || "Failed to load workspaces",
      variant: "destructive",
    });
    return null
  }

  const workspace = workspaceNameFromURL
    ? workspaces.find(
        (workspace) => workspace.workspaceName === workspaceNameFromURL,
      )
    : null;

  if (workspace) {
    useAppStore.getState().setActiveWorkspaceName(workspace.workspaceName);
  } else {
    const defaultWorkspace = workspaces.find((workspace) => workspace.default);

    if (defaultWorkspace) {
      if (isRootPath) {
        useAppStore
          .getState()
          .setActiveWorkspaceName(defaultWorkspace.workspaceName);

        return (
          <Navigate
            to="/$workspaceName"
            params={{ workspaceName: defaultWorkspace.workspaceName }}
          />
        );
      }

      return (
        <main>
          <nav className="comet-header-height flex w-full items-center justify-between gap-6 border-b">
            <Link
              to="/$workspaceName"
              className="absolute left-[18px] z-10 block"
              params={{ workspaceName: defaultWorkspace.workspaceName }}
            >
              <Logo expanded />
            </Link>
          </nav>

          <div className="flex flex-col items-center gap-4 px-10 py-24">
            <div className="comet-title-m text-muted-slate">
              This is a private project
            </div>
            <Link
              to="/$workspaceName"
              params={{ workspaceName: defaultWorkspace.workspaceName }}
            >
              <div className="comet-body flex flex-row items-center justify-end text-[#5155F5]">
                <MoveLeft className="mr-2 size-4" /> Go back to your workspace
              </div>
            </Link>
          </div>
        </main>
      );
    }

    window.location.href = buildUrl("login");
    return null;
  }

  return children;
};

export default WorkspacePreloader;
