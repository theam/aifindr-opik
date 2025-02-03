/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";

export const LlmAsJudgeMessageRole: core.serialization.Schema<
    serializers.LlmAsJudgeMessageRole.Raw,
    OpikApi.LlmAsJudgeMessageRole
> = core.serialization.enum_(["SYSTEM", "USER", "AI", "TOOL_EXECUTION_RESULT"]);

export declare namespace LlmAsJudgeMessageRole {
    export type Raw = "SYSTEM" | "USER" | "AI" | "TOOL_EXECUTION_RESULT";
}
