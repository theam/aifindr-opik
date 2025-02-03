/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";
import { NumericalFeedbackDetailCreate } from "./NumericalFeedbackDetailCreate";

export const NumericalFeedbackDefinitionCreate: core.serialization.ObjectSchema<
    serializers.NumericalFeedbackDefinitionCreate.Raw,
    OpikApi.NumericalFeedbackDefinitionCreate
> = core.serialization.object({
    details: NumericalFeedbackDetailCreate.optional(),
});

export declare namespace NumericalFeedbackDefinitionCreate {
    export interface Raw {
        details?: NumericalFeedbackDetailCreate.Raw | null;
    }
}
