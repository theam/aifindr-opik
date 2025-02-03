/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../../../../index";
import * as OpikApi from "../../../../../api/index";
import * as core from "../../../../../core";
import { JsonNodeWrite } from "../../../../types/JsonNodeWrite";
import { PromptWriteType } from "../../types/PromptWriteType";

export const PromptWrite: core.serialization.Schema<serializers.PromptWrite.Raw, OpikApi.PromptWrite> =
    core.serialization.object({
        id: core.serialization.string().optional(),
        name: core.serialization.string(),
        description: core.serialization.string().optional(),
        template: core.serialization.string().optional(),
        metadata: JsonNodeWrite.optional(),
        changeDescription: core.serialization.property("change_description", core.serialization.string().optional()),
        type: PromptWriteType.optional(),
    });

export declare namespace PromptWrite {
    export interface Raw {
        id?: string | null;
        name: string;
        description?: string | null;
        template?: string | null;
        metadata?: JsonNodeWrite.Raw | null;
        change_description?: string | null;
        type?: PromptWriteType.Raw | null;
    }
}
