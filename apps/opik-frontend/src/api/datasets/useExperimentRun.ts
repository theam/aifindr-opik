import { useMutation, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import get from "lodash/get";
import api, { EXPERIMENTS_RUN_ENDPOINT } from "@/api/api";
import { useToast } from "@/components/ui/use-toast";

type ExperimentRunParams = {
  datasetName: string;
  experimentName: string;
  projectName: string;
  basePromptName: string;
  workflow: string;
};

const useExperimentRunMutation = () => {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: async (params: ExperimentRunParams) => {
      const { data } = await api.post(EXPERIMENTS_RUN_ENDPOINT, params);
      return data;
    },
    onError: (error: AxiosError) => {
      const message = get(
        error,
        ["response", "data", "message"],
        error.message,
      );

      toast({
        title: "Error",
        description: message,
        variant: "destructive",
      });
    },
    onSettled: () => {
      return queryClient.invalidateQueries({
        queryKey: ["experiments"],
      });
    },
  });
};

export default useExperimentRunMutation;
