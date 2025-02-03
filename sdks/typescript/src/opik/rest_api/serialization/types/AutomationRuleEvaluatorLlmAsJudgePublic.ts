/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";
import { LlmAsJudgeCodePublic } from "./LlmAsJudgeCodePublic";

export const AutomationRuleEvaluatorLlmAsJudgePublic: core.serialization.ObjectSchema<
    serializers.AutomationRuleEvaluatorLlmAsJudgePublic.Raw,
    OpikApi.AutomationRuleEvaluatorLlmAsJudgePublic
> = core.serialization.object({
    code: LlmAsJudgeCodePublic.optional(),
});

export declare namespace AutomationRuleEvaluatorLlmAsJudgePublic {
    export interface Raw {
        code?: LlmAsJudgeCodePublic.Raw | null;
    }
}
