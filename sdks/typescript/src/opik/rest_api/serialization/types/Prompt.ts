/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";
import { JsonNode } from "./JsonNode";
import { PromptType } from "./PromptType";
import { PromptVersion } from "./PromptVersion";

export const Prompt: core.serialization.ObjectSchema<serializers.Prompt.Raw, OpikApi.Prompt> =
    core.serialization.object({
        id: core.serialization.string().optional(),
        name: core.serialization.string(),
        description: core.serialization.string().optional(),
        template: core.serialization.string().optional(),
        metadata: JsonNode.optional(),
        changeDescription: core.serialization.property("change_description", core.serialization.string().optional()),
        type: PromptType.optional(),
        createdAt: core.serialization.property("created_at", core.serialization.date().optional()),
        createdBy: core.serialization.property("created_by", core.serialization.string().optional()),
        lastUpdatedAt: core.serialization.property("last_updated_at", core.serialization.date().optional()),
        lastUpdatedBy: core.serialization.property("last_updated_by", core.serialization.string().optional()),
        versionCount: core.serialization.property("version_count", core.serialization.number().optional()),
        latestVersion: core.serialization.property("latest_version", PromptVersion.optional()),
    });

export declare namespace Prompt {
    export interface Raw {
        id?: string | null;
        name: string;
        description?: string | null;
        template?: string | null;
        metadata?: JsonNode.Raw | null;
        change_description?: string | null;
        type?: PromptType.Raw | null;
        created_at?: string | null;
        created_by?: string | null;
        last_updated_at?: string | null;
        last_updated_by?: string | null;
        version_count?: number | null;
        latest_version?: PromptVersion.Raw | null;
    }
}
