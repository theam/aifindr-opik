import { useMutation, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import get from "lodash/get";
import api, { EXPERIMENTS_REST_ENDPOINT } from "@/api/api";
import { useToast } from "@/components/ui/use-toast";

type ExperimentRunParams = {
  workspaceName: string;
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
      // Convert camelCase keys to snake_case for the backend
      const snakeCaseParams = {
        workspace_name: params.workspaceName,
        dataset_name: params.datasetName,
        experiment_name: params.experimentName,
        project_name: params.projectName,
        base_prompt_name: params.basePromptName,
        workflow: params.workflow
      };
      
      const { data } = await api.post(EXPERIMENTS_REST_ENDPOINT + 'run', snakeCaseParams);
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
