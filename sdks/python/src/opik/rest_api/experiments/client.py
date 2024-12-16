# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from ..core.request_options import RequestOptions
from ..types.experiment_page_public import ExperimentPagePublic
from ..core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..types.json_node_write import JsonNodeWrite
from ..types.prompt_version_link_write import PromptVersionLinkWrite
from ..core.serialization import convert_and_respect_annotation_metadata
from ..types.experiment_item import ExperimentItem
from ..types.experiment_public import ExperimentPublic
from ..core.jsonable_encoder import jsonable_encoder
from ..errors.not_found_error import NotFoundError
from ..types.experiment_item_public import ExperimentItemPublic
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ExperimentsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def find_experiments(
        self,
        *,
        page: typing.Optional[int] = None,
        size: typing.Optional[int] = None,
        dataset_id: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        dataset_deleted: typing.Optional[bool] = None,
        prompt_id: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExperimentPagePublic:
        """
        Find experiments

        Parameters
        ----------
        page : typing.Optional[int]

        size : typing.Optional[int]

        dataset_id : typing.Optional[str]

        name : typing.Optional[str]

        dataset_deleted : typing.Optional[bool]

        prompt_id : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPagePublic
            Experiments resource

        Examples
        --------
        from Opik import OpikApi

        client = OpikApi()
        client.experiments.find_experiments()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments",
            method="GET",
            params={
                "page": page,
                "size": size,
                "datasetId": dataset_id,
                "name": name,
                "dataset_deleted": dataset_deleted,
                "prompt_id": prompt_id,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ExperimentPagePublic,
                    parse_obj_as(
                        type_=ExperimentPagePublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_experiment(
        self,
        *,
        dataset_name: str,
        id: typing.Optional[str] = OMIT,
        name: typing.Optional[str] = OMIT,
        metadata: typing.Optional[JsonNodeWrite] = OMIT,
        prompt_version: typing.Optional[PromptVersionLinkWrite] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Create experiment

        Parameters
        ----------
        dataset_name : str

        id : typing.Optional[str]

        name : typing.Optional[str]

        metadata : typing.Optional[JsonNodeWrite]

        prompt_version : typing.Optional[PromptVersionLinkWrite]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from Opik import OpikApi

        client = OpikApi()
        client.experiments.create_experiment(
            dataset_name="dataset_name",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments",
            method="POST",
            json={
                "id": id,
                "dataset_name": dataset_name,
                "name": name,
                "metadata": metadata,
                "prompt_version": convert_and_respect_annotation_metadata(
                    object_=prompt_version,
                    annotation=PromptVersionLinkWrite,
                    direction="write",
                ),
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_experiment_items(
        self,
        *,
        experiment_items: typing.Sequence[ExperimentItem],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Create experiment items

        Parameters
        ----------
        experiment_items : typing.Sequence[ExperimentItem]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from Opik import ExperimentItem, OpikApi

        client = OpikApi()
        client.experiments.create_experiment_items(
            experiment_items=[
                ExperimentItem(
                    experiment_id="experiment_id",
                    dataset_item_id="dataset_item_id",
                    trace_id="trace_id",
                )
            ],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments/items",
            method="POST",
            json={
                "experiment_items": convert_and_respect_annotation_metadata(
                    object_=experiment_items,
                    annotation=typing.Sequence[ExperimentItem],
                    direction="write",
                ),
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_experiment_items(
        self,
        *,
        ids: typing.Sequence[str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete experiment items

        Parameters
        ----------
        ids : typing.Sequence[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from Opik import OpikApi

        client = OpikApi()
        client.experiments.delete_experiment_items(
            ids=["ids"],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments/items/delete",
            method="POST",
            json={
                "ids": ids,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_experiments_by_id(
        self,
        *,
        ids: typing.Sequence[str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete experiments by id

        Parameters
        ----------
        ids : typing.Sequence[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from Opik import OpikApi

        client = OpikApi()
        client.experiments.delete_experiments_by_id(
            ids=["ids"],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments/delete",
            method="POST",
            json={
                "ids": ids,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def find_feedback_score_names(
        self,
        *,
        experiment_ids: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[str]:
        """
        Find Feedback Score names

        Parameters
        ----------
        experiment_ids : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[str]
            Feedback Scores resource

        Examples
        --------
        from Opik import OpikApi

        client = OpikApi()
        client.experiments.find_feedback_score_names()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments/feedback-scores/names",
            method="GET",
            params={
                "experiment_ids": experiment_ids,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[str],
                    parse_obj_as(
                        type_=typing.List[str],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_experiment_by_id(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentPublic:
        """
        Get experiment by id

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPublic
            Experiment resource

        Examples
        --------
        from Opik import OpikApi

        client = OpikApi()
        client.experiments.get_experiment_by_id(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/private/experiments/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ExperimentPublic,
                    parse_obj_as(
                        type_=ExperimentPublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_experiment_by_name(
        self, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentPublic:
        """
        Get experiment by name

        Parameters
        ----------
        name : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPublic
            Experiments resource

        Examples
        --------
        from Opik import OpikApi

        client = OpikApi()
        client.experiments.get_experiment_by_name(
            name="name",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/private/experiments/retrieve",
            method="POST",
            json={
                "name": name,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ExperimentPublic,
                    parse_obj_as(
                        type_=ExperimentPublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_experiment_item_by_id(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentItemPublic:
        """
        Get experiment item by id

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentItemPublic
            Experiment item resource

        Examples
        --------
        from Opik import OpikApi

        client = OpikApi()
        client.experiments.get_experiment_item_by_id(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/private/experiments/items/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ExperimentItemPublic,
                    parse_obj_as(
                        type_=ExperimentItemPublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def stream_experiment_items(
        self,
        *,
        experiment_name: str,
        limit: typing.Optional[int] = OMIT,
        last_retrieved_id: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[bytes]:
        """
        Stream experiment items

        Parameters
        ----------
        experiment_name : str

        limit : typing.Optional[int]

        last_retrieved_id : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.

        Yields
        ------
        typing.Iterator[bytes]
            Experiment items stream or error during process
        """
        with self._client_wrapper.httpx_client.stream(
            "v1/private/experiments/items/stream",
            method="POST",
            json={
                "experiment_name": experiment_name,
                "limit": limit,
                "last_retrieved_id": last_retrieved_id,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _chunk_size = (
                        request_options.get("chunk_size", None)
                        if request_options is not None
                        else None
                    )
                    for _chunk in _response.iter_bytes(chunk_size=_chunk_size):
                        yield _chunk
                    return
                _response.read()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncExperimentsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def find_experiments(
        self,
        *,
        page: typing.Optional[int] = None,
        size: typing.Optional[int] = None,
        dataset_id: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        dataset_deleted: typing.Optional[bool] = None,
        prompt_id: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExperimentPagePublic:
        """
        Find experiments

        Parameters
        ----------
        page : typing.Optional[int]

        size : typing.Optional[int]

        dataset_id : typing.Optional[str]

        name : typing.Optional[str]

        dataset_deleted : typing.Optional[bool]

        prompt_id : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPagePublic
            Experiments resource

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.find_experiments()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments",
            method="GET",
            params={
                "page": page,
                "size": size,
                "datasetId": dataset_id,
                "name": name,
                "dataset_deleted": dataset_deleted,
                "prompt_id": prompt_id,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ExperimentPagePublic,
                    parse_obj_as(
                        type_=ExperimentPagePublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_experiment(
        self,
        *,
        dataset_name: str,
        id: typing.Optional[str] = OMIT,
        name: typing.Optional[str] = OMIT,
        metadata: typing.Optional[JsonNodeWrite] = OMIT,
        prompt_version: typing.Optional[PromptVersionLinkWrite] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Create experiment

        Parameters
        ----------
        dataset_name : str

        id : typing.Optional[str]

        name : typing.Optional[str]

        metadata : typing.Optional[JsonNodeWrite]

        prompt_version : typing.Optional[PromptVersionLinkWrite]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.create_experiment(
                dataset_name="dataset_name",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments",
            method="POST",
            json={
                "id": id,
                "dataset_name": dataset_name,
                "name": name,
                "metadata": metadata,
                "prompt_version": convert_and_respect_annotation_metadata(
                    object_=prompt_version,
                    annotation=PromptVersionLinkWrite,
                    direction="write",
                ),
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_experiment_items(
        self,
        *,
        experiment_items: typing.Sequence[ExperimentItem],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Create experiment items

        Parameters
        ----------
        experiment_items : typing.Sequence[ExperimentItem]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi, ExperimentItem

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.create_experiment_items(
                experiment_items=[
                    ExperimentItem(
                        experiment_id="experiment_id",
                        dataset_item_id="dataset_item_id",
                        trace_id="trace_id",
                    )
                ],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments/items",
            method="POST",
            json={
                "experiment_items": convert_and_respect_annotation_metadata(
                    object_=experiment_items,
                    annotation=typing.Sequence[ExperimentItem],
                    direction="write",
                ),
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_experiment_items(
        self,
        *,
        ids: typing.Sequence[str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete experiment items

        Parameters
        ----------
        ids : typing.Sequence[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.delete_experiment_items(
                ids=["ids"],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments/items/delete",
            method="POST",
            json={
                "ids": ids,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_experiments_by_id(
        self,
        *,
        ids: typing.Sequence[str],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> None:
        """
        Delete experiments by id

        Parameters
        ----------
        ids : typing.Sequence[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.delete_experiments_by_id(
                ids=["ids"],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments/delete",
            method="POST",
            json={
                "ids": ids,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def find_feedback_score_names(
        self,
        *,
        experiment_ids: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[str]:
        """
        Find Feedback Score names

        Parameters
        ----------
        experiment_ids : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[str]
            Feedback Scores resource

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.find_feedback_score_names()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments/feedback-scores/names",
            method="GET",
            params={
                "experiment_ids": experiment_ids,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[str],
                    parse_obj_as(
                        type_=typing.List[str],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_experiment_by_id(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentPublic:
        """
        Get experiment by id

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPublic
            Experiment resource

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.get_experiment_by_id(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/private/experiments/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ExperimentPublic,
                    parse_obj_as(
                        type_=ExperimentPublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_experiment_by_name(
        self, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentPublic:
        """
        Get experiment by name

        Parameters
        ----------
        name : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentPublic
            Experiments resource

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.get_experiment_by_name(
                name="name",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/private/experiments/retrieve",
            method="POST",
            json={
                "name": name,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ExperimentPublic,
                    parse_obj_as(
                        type_=ExperimentPublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_experiment_item_by_id(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExperimentItemPublic:
        """
        Get experiment item by id

        Parameters
        ----------
        id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExperimentItemPublic
            Experiment item resource

        Examples
        --------
        import asyncio

        from Opik import AsyncOpikApi

        client = AsyncOpikApi()


        async def main() -> None:
            await client.experiments.get_experiment_item_by_id(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/private/experiments/items/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ExperimentItemPublic,
                    parse_obj_as(
                        type_=ExperimentItemPublic,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def stream_experiment_items(
        self,
        *,
        experiment_name: str,
        limit: typing.Optional[int] = OMIT,
        last_retrieved_id: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[bytes]:
        """
        Stream experiment items

        Parameters
        ----------
        experiment_name : str

        limit : typing.Optional[int]

        last_retrieved_id : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.

        Yields
        ------
        typing.AsyncIterator[bytes]
            Experiment items stream or error during process
        """
        async with self._client_wrapper.httpx_client.stream(
            "v1/private/experiments/items/stream",
            method="POST",
            json={
                "experiment_name": experiment_name,
                "limit": limit,
                "last_retrieved_id": last_retrieved_id,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _chunk_size = (
                        request_options.get("chunk_size", None)
                        if request_options is not None
                        else None
                    )
                    async for _chunk in _response.aiter_bytes(chunk_size=_chunk_size):
                        yield _chunk
                    return
                await _response.aread()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)
