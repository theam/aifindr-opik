/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as serializers from "../../../../index";
import * as OpikApi from "../../../../../api/index";
import * as core from "../../../../../core";

export const DatasetItemsDelete: core.serialization.Schema<
    serializers.DatasetItemsDelete.Raw,
    OpikApi.DatasetItemsDelete
> = core.serialization.object({
    itemIds: core.serialization.property("item_ids", core.serialization.list(core.serialization.string())),
});

export declare namespace DatasetItemsDelete {
    export interface Raw {
        item_ids: string[];
    }
}
