import { UseQueryOptions } from "@tanstack/react-query";
import axios from "axios";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_AIFINDR_API_URL,
});
axiosInstance.defaults.withCredentials = true;

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
