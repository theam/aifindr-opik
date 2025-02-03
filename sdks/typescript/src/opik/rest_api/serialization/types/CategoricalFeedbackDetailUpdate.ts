/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";

export const CategoricalFeedbackDetailUpdate: core.serialization.ObjectSchema<
    serializers.CategoricalFeedbackDetailUpdate.Raw,
    OpikApi.CategoricalFeedbackDetailUpdate
> = core.serialization.object({
    categories: core.serialization.record(core.serialization.string(), core.serialization.number()),
});

export declare namespace CategoricalFeedbackDetailUpdate {
    export interface Raw {
        categories: Record<string, number>;
    }
}
