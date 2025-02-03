/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";
import { JsonNode } from "./JsonNode";
import { ErrorInfo } from "./ErrorInfo";
import { FeedbackScore } from "./FeedbackScore";
import { Comment } from "./Comment";

export const Trace: core.serialization.ObjectSchema<serializers.Trace.Raw, OpikApi.Trace> = core.serialization.object({
    id: core.serialization.string().optional(),
    projectName: core.serialization.property("project_name", core.serialization.string().optional()),
    projectId: core.serialization.property("project_id", core.serialization.string().optional()),
    name: core.serialization.string(),
    startTime: core.serialization.property("start_time", core.serialization.date()),
    endTime: core.serialization.property("end_time", core.serialization.date().optional()),
    input: JsonNode.optional(),
    output: JsonNode.optional(),
    metadata: JsonNode.optional(),
    tags: core.serialization.list(core.serialization.string()).optional(),
    errorInfo: core.serialization.property("error_info", ErrorInfo.optional()),
    usage: core.serialization.record(core.serialization.string(), core.serialization.number()).optional(),
    createdAt: core.serialization.property("created_at", core.serialization.date().optional()),
    lastUpdatedAt: core.serialization.property("last_updated_at", core.serialization.date().optional()),
    createdBy: core.serialization.property("created_by", core.serialization.string().optional()),
    lastUpdatedBy: core.serialization.property("last_updated_by", core.serialization.string().optional()),
    feedbackScores: core.serialization.property("feedback_scores", core.serialization.list(FeedbackScore).optional()),
    comments: core.serialization.list(Comment).optional(),
    totalEstimatedCost: core.serialization.property("total_estimated_cost", core.serialization.number().optional()),
    duration: core.serialization.number().optional(),
});

export declare namespace Trace {
    export interface Raw {
        id?: string | null;
        project_name?: string | null;
        project_id?: string | null;
        name: string;
        start_time: string;
        end_time?: string | null;
        input?: JsonNode.Raw | null;
        output?: JsonNode.Raw | null;
        metadata?: JsonNode.Raw | null;
        tags?: string[] | null;
        error_info?: ErrorInfo.Raw | null;
        usage?: Record<string, number> | null;
        created_at?: string | null;
        last_updated_at?: string | null;
        created_by?: string | null;
        last_updated_by?: string | null;
        feedback_scores?: FeedbackScore.Raw[] | null;
        comments?: Comment.Raw[] | null;
        total_estimated_cost?: number | null;
        duration?: number | null;
    }
}
