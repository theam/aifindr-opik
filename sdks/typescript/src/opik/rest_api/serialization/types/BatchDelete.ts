/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";

export const BatchDelete: core.serialization.ObjectSchema<serializers.BatchDelete.Raw, OpikApi.BatchDelete> =
    core.serialization.object({
        ids: core.serialization.list(core.serialization.string()),
    });

export declare namespace BatchDelete {
    export interface Raw {
        ids: string[];
    }
}
