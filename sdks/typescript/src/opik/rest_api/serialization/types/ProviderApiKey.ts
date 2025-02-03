/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";
import { ProviderApiKeyProvider } from "./ProviderApiKeyProvider";

export const ProviderApiKey: core.serialization.ObjectSchema<serializers.ProviderApiKey.Raw, OpikApi.ProviderApiKey> =
    core.serialization.object({
        id: core.serialization.string().optional(),
        provider: ProviderApiKeyProvider,
        apiKey: core.serialization.property("api_key", core.serialization.string()),
        name: core.serialization.string().optional(),
        createdAt: core.serialization.property("created_at", core.serialization.date().optional()),
        createdBy: core.serialization.property("created_by", core.serialization.string().optional()),
        lastUpdatedAt: core.serialization.property("last_updated_at", core.serialization.date().optional()),
        lastUpdatedBy: core.serialization.property("last_updated_by", core.serialization.string().optional()),
    });

export declare namespace ProviderApiKey {
    export interface Raw {
        id?: string | null;
        provider: ProviderApiKeyProvider.Raw;
        api_key: string;
        name?: string | null;
        created_at?: string | null;
        created_by?: string | null;
        last_updated_at?: string | null;
        last_updated_by?: string | null;
    }
}
