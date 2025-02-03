/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";

export const PercentageValuesPublic: core.serialization.ObjectSchema<
    serializers.PercentageValuesPublic.Raw,
    OpikApi.PercentageValuesPublic
> = core.serialization.object({
    p50: core.serialization.number().optional(),
    p90: core.serialization.number().optional(),
    p99: core.serialization.number().optional(),
});

export declare namespace PercentageValuesPublic {
    export interface Raw {
        p50?: number | null;
        p90?: number | null;
        p99?: number | null;
    }
}
