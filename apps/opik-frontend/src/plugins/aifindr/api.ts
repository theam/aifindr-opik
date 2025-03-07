import { ACCESS_TOKEN_KEY } from "@/constants/user";
import { UseQueryOptions } from "@tanstack/react-query";
import axios from "axios";

// Obtain the base URL from the runtime config
const getBaseURL = () => {
  if (!window.RUNTIME_CONFIG && !import.meta.env.VITE_AIFINDR_DOMAIN) {
    console.error('AIFINDR_DOMAIN is not set neither in runtime nor in environment variables');
  }
  return window.RUNTIME_CONFIG?.AIFINDR_DOMAIN || import.meta.env.VITE_AIFINDR_DOMAIN || '';
};

const axiosInstance = axios.create({
  baseURL: getBaseURL(),
});
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
