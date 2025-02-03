/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../../../index";
import * as OpikApi from "../../../../api/index";
import * as core from "../../../../core";

export const FindFeedbackDefinitionsRequestType: core.serialization.Schema<
    serializers.FindFeedbackDefinitionsRequestType.Raw,
    OpikApi.FindFeedbackDefinitionsRequestType
> = core.serialization.enum_(["numerical", "categorical"]);

export declare namespace FindFeedbackDefinitionsRequestType {
    export type Raw = "numerical" | "categorical";
}
