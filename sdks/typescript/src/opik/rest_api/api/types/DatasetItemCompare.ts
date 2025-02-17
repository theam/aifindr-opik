/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as OpikApi from "../index";

export interface DatasetItemCompare {
    id?: string;
    traceId?: string;
    spanId?: string;
    source: OpikApi.DatasetItemCompareSource;
    data: OpikApi.JsonNode;
    experimentItems?: OpikApi.ExperimentItemCompare[];
    createdAt?: Date;
    lastUpdatedAt?: Date;
    createdBy?: string;
    lastUpdatedBy?: string;
}
