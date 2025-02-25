import { QueryFunctionContext, useQuery } from "@tanstack/react-query";
import api, { QueryConfig } from "./api";
import { Workspace } from "./types";

const getAllUserWorkspaces = async (
  { signal }: QueryFunctionContext,
) => {
  // TODO: Remove this when we load workspaces from backend
  const testWorkspaces: Workspace[] = [
    {
      workspaceId: "default-test",
      workspaceName: "default",
      workspaceOwner: "Álvaro",
      workspaceCreator: "default-test",
      organizationId: "default-test",
      default: true,
      createdAt: 1,
      collaborationFeaturesDisabled: false,
    },{
      workspaceId: "workspace-test-id-1",
      workspaceName: "workspace-test-name-1",
      workspaceOwner: "workspace-test-owner-1",
      workspaceCreator: "workspace-test-creator-1",
      organizationId: "organization-test-id-1",
      default: false,
      createdAt: 2,
      collaborationFeaturesDisabled: false,
    },{
      workspaceId: "workspace-test-id-2",
      workspaceName: "workspace-test-name-2",
      workspaceOwner: "workspace-test-owner-2",
      workspaceCreator: "workspace-test-creator-2",
      organizationId: "organization-test-id-2",
      default: false,
      createdAt: 3,
      collaborationFeaturesDisabled: false,
    }
  ]

  return testWorkspaces;
  // const allWorkspacesPromise = api
  //   .get<Workspace[]>(`/workspaces`, {
  //     signal,
  //     params: { withoutExtendedData: true },
  //   })
  //   .then(({ data }) => data);

  // const workspacesPromises = organizationIds?.map((organizationId) => {
  //   return api
  //     .get<Workspace[]>(`/workspaces`, {
  //       signal,
  //       params: { organizationId, withoutExtendedData: true },
  //     })
  //     .then(({ data }) => data);
  // });

  // const workspaces = await Promise.all([
  //   allWorkspacesPromise,
  //   ...(workspacesPromises || []),
  // ]);

  // return uniqBy(workspaces.flat(), "workspaceId");
};

export default function useAllUserWorkspaces(
  options?: QueryConfig<Workspace[]>,
) {

  return useQuery({
    queryKey: ["workspaces", {} ],
    queryFn: (context) => getAllUserWorkspaces(context),
    ...options,
    enabled: options?.enabled,
  });
}
