/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../../../../index";
import * as OpikApi from "../../../../../api/index";
import * as core from "../../../../../core";

export const PromptVersionRetrieveDetail: core.serialization.Schema<
    serializers.PromptVersionRetrieveDetail.Raw,
    OpikApi.PromptVersionRetrieveDetail
> = core.serialization.object({
    name: core.serialization.string(),
    commit: core.serialization.string().optional(),
});

export declare namespace PromptVersionRetrieveDetail {
    export interface Raw {
        name: string;
        commit?: string | null;
    }
}
