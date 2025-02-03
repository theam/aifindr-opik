/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";
import { ExperimentPublic } from "./ExperimentPublic";

export const ExperimentPagePublic: core.serialization.ObjectSchema<
    serializers.ExperimentPagePublic.Raw,
    OpikApi.ExperimentPagePublic
> = core.serialization.object({
    page: core.serialization.number().optional(),
    size: core.serialization.number().optional(),
    total: core.serialization.number().optional(),
    content: core.serialization.list(ExperimentPublic).optional(),
});

export declare namespace ExperimentPagePublic {
    export interface Raw {
        page?: number | null;
        size?: number | null;
        total?: number | null;
        content?: ExperimentPublic.Raw[] | null;
    }
}
