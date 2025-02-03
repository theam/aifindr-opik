/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as core from "../../core";
import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import { AutomationRuleEvaluatorLlmAsJudgeWrite } from "./AutomationRuleEvaluatorLlmAsJudgeWrite";

const _Base = core.serialization.object({
    name: core.serialization.string(),
    samplingRate: core.serialization.property("sampling_rate", core.serialization.number().optional()),
    action: core.serialization.stringLiteral("evaluator").optional(),
});
export const AutomationRuleEvaluatorWrite: core.serialization.Schema<
    serializers.AutomationRuleEvaluatorWrite.Raw,
    OpikApi.AutomationRuleEvaluatorWrite
> = core.serialization
    .union("type", {
        llm_as_judge: AutomationRuleEvaluatorLlmAsJudgeWrite.extend(_Base),
    })
    .transform<OpikApi.AutomationRuleEvaluatorWrite>({
        transform: (value) => value,
        untransform: (value) => value,
    });

export declare namespace AutomationRuleEvaluatorWrite {
    export type Raw = AutomationRuleEvaluatorWrite.LlmAsJudge;

    export interface LlmAsJudge extends _Base, AutomationRuleEvaluatorLlmAsJudgeWrite.Raw {
        type: "llm_as_judge";
    }

    export interface _Base {
        name: string;
        sampling_rate?: number | null;
        action?: "evaluator" | null;
    }
}
