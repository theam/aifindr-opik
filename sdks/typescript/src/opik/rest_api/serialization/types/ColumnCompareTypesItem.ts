/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../index";
import * as OpikApi from "../../api/index";
import * as core from "../../core";

export const ColumnCompareTypesItem: core.serialization.Schema<
    serializers.ColumnCompareTypesItem.Raw,
    OpikApi.ColumnCompareTypesItem
> = core.serialization.enum_(["string", "number", "object", "boolean", "array", "null"]);

export declare namespace ColumnCompareTypesItem {
    export type Raw = "string" | "number" | "object" | "boolean" | "array" | "null";
}
