/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../../../../index";
import * as OpikApi from "../../../../../api/index";
import * as core from "../../../../../core";

export const IdentifierPublic: core.serialization.Schema<serializers.IdentifierPublic.Raw, OpikApi.IdentifierPublic> =
    core.serialization.object({
        name: core.serialization.string(),
    });

export declare namespace IdentifierPublic {
    export interface Raw {
        name: string;
    }
}
