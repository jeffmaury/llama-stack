# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import Literal, Optional, Protocol, Union

from typing_extensions import Annotated

from llama_models.llama3.api.datatypes import *  # noqa: F403
from llama_models.schema_utils import json_schema_type, webmethod


@json_schema_type
class ModelCandidate(BaseModel):
    type: Literal["model"] = "model"
    model: str
    sampling_params: SamplingParams
    system_message: Optional[SystemMessage] = None


@json_schema_type
class AgentCandidate(BaseModel):
    type: Literal["agent"] = "agent"
    config: AgentConfig


EvalCandidate = Annotated[
    Union[ModelCandidate, AgentCandidate], Field(discriminator="type")
]


@json_schema_type
class Job(BaseModel):
    job_id: str


class Eval(Protocol):
    @webmethod(route="/eval/evaluate_task", method="POST")
    async def evaluate_task(
        self,
        dataset_id: str,
        candidate: EvalCandidate,
    ) -> Job: ...

    @webmethod(route="/eval/job/status", method="GET")
    async def job_status(self, job_id: str) -> None: ...

    @webmethod(route="/eval/job/cancel", method="POST")
    async def job_cancel(self, job_id: str) -> None: ...

    @webmethod(route="/eval/job/result", method="GET")
    async def job_result(self, job_id: str) -> None: ...
