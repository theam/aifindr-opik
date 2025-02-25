export interface User {
  defaultWorkspace: string;
  email: string;
  profileImages: ProfileImages;
  loggedIn: boolean;
  userName: string;
}

export interface Auth0User {
  sub: string;
  given_name: string;
  family_name: string;
  nickname: string;
  name: string;
  picture: string;
  updated_at: string;
  email: string;
}

export interface ProfileImages {
  small: string;
  large: string;
}

export interface Workspace {
  createdAt: number;
  workspaceId: string;
  workspaceName: string;
  workspaceOwner: string;
  workspaceCreator: string;
  organizationId: string;
  collaborationFeaturesDisabled: boolean;
  default: boolean;
}
