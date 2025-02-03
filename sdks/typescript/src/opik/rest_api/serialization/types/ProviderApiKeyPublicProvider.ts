/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";

export const ProviderApiKeyPublicProvider: core.serialization.Schema<
    serializers.ProviderApiKeyPublicProvider.Raw,
    OpikApi.ProviderApiKeyPublicProvider
> = core.serialization.enum_(["openai", "anthropic", "gemini"]);

export declare namespace ProviderApiKeyPublicProvider {
    export type Raw = "openai" | "anthropic" | "gemini";
}
