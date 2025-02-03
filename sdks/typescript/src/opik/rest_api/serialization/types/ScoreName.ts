/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";

export const ScoreName: core.serialization.ObjectSchema<serializers.ScoreName.Raw, OpikApi.ScoreName> =
    core.serialization.object({
        name: core.serialization.string().optional(),
    });

export declare namespace ScoreName {
    export interface Raw {
        name?: string | null;
    }
}
