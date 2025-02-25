import { ACCESS_TOKEN_KEY } from "@/constants/user";
import { UseQueryOptions } from "@tanstack/react-query";
import axios from "axios";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_AIFINDR_API_URL,
});
axiosInstance.defaults.withCredentials = true;
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export type QueryConfig<TQueryFnData, TData = TQueryFnData> = Omit<
  UseQueryOptions<
    TQueryFnData,
    Error,
    TData,
    [string, Record<string, unknown>, ...string[]]
  >,
  "queryKey" | "queryFn"
>;

export default axiosInstance;
