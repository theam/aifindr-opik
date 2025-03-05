import { QueryFunctionContext, useQuery } from "@tanstack/react-query";
import api, { QueryConfig } from "./api";
import { Project, Workspace } from "./types";

const getAllUserWorkspaces = async (
  { signal }: QueryFunctionContext,
) => {
  const { data: projects } = await api.get<Project[]>(`/admin/api/projects`)
  const workspaces: Workspace[] = projects.map((project) => {
    return {
      workspaceId: project.ID.toString(),
      workspaceName: project.slug,
      workspaceDisplayName: project.name,
      workspaceOwner: "",
      workspaceCreator: "",
      organizationId: "",
      default: false,
      createdAt: project.CreatedAt,
      collaborationFeaturesDisabled: false,
    }
  })

  // TODO: Error if no workspaces are found
  // TODO: Manage if the above query fails

  // Set the first workspace as default
  workspaces[0].default = true;

  return workspaces;
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
