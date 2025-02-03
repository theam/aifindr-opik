/**
 * This file was auto-generated by Fern from our API Definition.
 */

import * as OpikApi from "../index";

export type FeedbackCreate = OpikApi.FeedbackCreate.Numerical | OpikApi.FeedbackCreate.Categorical;

export namespace FeedbackCreate {
    export interface Numerical extends OpikApi.NumericalFeedbackDefinitionCreate, _Base {
        type: "numerical";
    }

    export interface Categorical extends OpikApi.CategoricalFeedbackDefinitionCreate, _Base {
        type: "categorical";
    }

    export interface _Base {
        id?: string;
        name: string;
    }
}
