/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";

export const FeedbackScoreSource: core.serialization.Schema<
    serializers.FeedbackScoreSource.Raw,
    OpikApi.FeedbackScoreSource
> = core.serialization.enum_(["ui", "sdk", "online_scoring"]);

export declare namespace FeedbackScoreSource {
    export type Raw = "ui" | "sdk" | "online_scoring";
}
