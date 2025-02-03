/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";
import { JsonNodePublic } from "./JsonNodePublic";
import { PromptVersionPublicType } from "./PromptVersionPublicType";

export const PromptVersionPublic: core.serialization.ObjectSchema<
    serializers.PromptVersionPublic.Raw,
    OpikApi.PromptVersionPublic
> = core.serialization.object({
    id: core.serialization.string().optional(),
    promptId: core.serialization.property("prompt_id", core.serialization.string().optional()),
    commit: core.serialization.string().optional(),
    template: core.serialization.string(),
    metadata: JsonNodePublic.optional(),
    type: PromptVersionPublicType.optional(),
    changeDescription: core.serialization.property("change_description", core.serialization.string().optional()),
    createdAt: core.serialization.property("created_at", core.serialization.date().optional()),
    createdBy: core.serialization.property("created_by", core.serialization.string().optional()),
});

export declare namespace PromptVersionPublic {
    export interface Raw {
        id?: string | null;
        prompt_id?: string | null;
        commit?: string | null;
        template: string;
        metadata?: JsonNodePublic.Raw | null;
        type?: PromptVersionPublicType.Raw | null;
        change_description?: string | null;
        created_at?: string | null;
        created_by?: string | null;
    }
}
