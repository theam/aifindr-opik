/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as core from "../../core";
import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import { AutomationRuleEvaluatorLlmAsJudgePublic } from "./AutomationRuleEvaluatorLlmAsJudgePublic";

const _Base = core.serialization.object({
    id: core.serialization.string().optional(),
    projectId: core.serialization.property("project_id", core.serialization.string().optional()),
    name: core.serialization.string(),
    samplingRate: core.serialization.property("sampling_rate", core.serialization.number().optional()),
    createdAt: core.serialization.property("created_at", core.serialization.date().optional()),
    createdBy: core.serialization.property("created_by", core.serialization.string().optional()),
    lastUpdatedAt: core.serialization.property("last_updated_at", core.serialization.date().optional()),
    lastUpdatedBy: core.serialization.property("last_updated_by", core.serialization.string().optional()),
    action: core.serialization.stringLiteral("evaluator").optional(),
});
export const AutomationRuleEvaluatorPublic: core.serialization.Schema<
    serializers.AutomationRuleEvaluatorPublic.Raw,
    OpikApi.AutomationRuleEvaluatorPublic
> = core.serialization
    .union("type", {
        llm_as_judge: AutomationRuleEvaluatorLlmAsJudgePublic.extend(_Base),
    })
    .transform<OpikApi.AutomationRuleEvaluatorPublic>({
        transform: (value) => value,
        untransform: (value) => value,
    });

export declare namespace AutomationRuleEvaluatorPublic {
    export type Raw = AutomationRuleEvaluatorPublic.LlmAsJudge;

    export interface LlmAsJudge extends _Base, AutomationRuleEvaluatorLlmAsJudgePublic.Raw {
        type: "llm_as_judge";
    }

    export interface _Base {
        id?: string | null;
        project_id?: string | null;
        name: string;
        sampling_rate?: number | null;
        created_at?: string | null;
        created_by?: string | null;
        last_updated_at?: string | null;
        last_updated_by?: string | null;
        action?: "evaluator" | null;
    }
}
