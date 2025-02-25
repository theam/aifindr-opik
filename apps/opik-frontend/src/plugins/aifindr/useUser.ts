import { QueryFunctionContext, useQuery } from "@tanstack/react-query";
import api, { QueryConfig } from "./api";
import { Auth0User, User } from "./types";

const getUser = async ({ signal }: QueryFunctionContext) => {
  const { data } = await api.get<Auth0User>("/userinfo", {
    signal,
    baseURL: import.meta.env.VITE_AUTH_AUTHORITY,
    headers: {
      Authorization: `Bearer <token>`,
    },
    withCredentials: false,
  });

  const user: User = {
    defaultWorkspace: "default-test", // TODO: Add default workspace
    email: data.email,
    profileImages: {
      small: data.picture,
      large: data.picture,
    },
    userName: data.nickname,
    loggedIn: true,
  };

  return user;
};

export default function useUser(options?: QueryConfig<User>) {
  return useQuery({
    queryKey: ["user", {}],
    queryFn: (context) => getUser(context),
    ...options,
  });
}
