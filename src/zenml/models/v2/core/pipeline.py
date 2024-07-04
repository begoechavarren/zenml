#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Models representing pipelines."""

from typing import TYPE_CHECKING, Any, List, Optional, Union
from uuid import UUID

from pydantic import Field

from zenml.constants import STR_FIELD_MAX_LENGTH, TEXT_FIELD_MAX_LENGTH
from zenml.enums import ExecutionStatus
from zenml.models.v2.base.base import BaseUpdate
from zenml.models.v2.base.scoped import (
    WorkspaceScopedFilter,
    WorkspaceScopedRequest,
    WorkspaceScopedResponse,
    WorkspaceScopedResponseBody,
    WorkspaceScopedResponseMetadata,
    WorkspaceScopedResponseResources,
)

if TYPE_CHECKING:
    from zenml.models.v2.core.pipeline_run import PipelineRunResponse


# ------------------ Request Model ------------------


class PipelineRequest(WorkspaceScopedRequest):
    """Request model for pipelines."""

    name: str = Field(
        title="The name of the pipeline.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    description: Optional[str] = Field(
        default=None,
        title="The description of the pipeline.",
        max_length=TEXT_FIELD_MAX_LENGTH,
    )


# ------------------ Update Model ------------------


class PipelineUpdate(BaseUpdate):
    """Update model for pipelines."""

    description: Optional[str] = Field(
        default=None,
        title="The description of the pipeline.",
        max_length=TEXT_FIELD_MAX_LENGTH,
    )


# ------------------ Response Model ------------------


class PipelineResponseBody(WorkspaceScopedResponseBody):
    """Response body for pipelines."""

    status: Optional[List[ExecutionStatus]] = Field(
        default=None, title="The status of the last 3 Pipeline Runs."
    )
    latest_run_id: Optional[UUID] = Field(
        default=None,
        title="The ID of the latest run of the pipeline namespace.",
    )
    latest_run_status: Optional[ExecutionStatus] = Field(
        default=None,
        title="The status of the latest run of the pipeline namespace.",
    )


class PipelineResponseMetadata(WorkspaceScopedResponseMetadata):
    """Response metadata for pipelines."""


class PipelineResponseResources(WorkspaceScopedResponseResources):
    """Class for all resource models associated with the pipeline entity."""


class PipelineResponse(
    WorkspaceScopedResponse[
        PipelineResponseBody,
        PipelineResponseMetadata,
        PipelineResponseResources,
    ]
):
    """Response model for pipelines."""

    name: str = Field(
        title="The name of the pipeline.",
        max_length=STR_FIELD_MAX_LENGTH,
    )

    def get_hydrated_version(self) -> "PipelineResponse":
        """Get the hydrated version of this pipeline.

        Returns:
            an instance of the same entity with the metadata field attached.
        """
        from zenml.client import Client

        return Client().zen_store.get_pipeline(self.id)

    # Helper methods
    def get_runs(self, **kwargs: Any) -> List["PipelineRunResponse"]:
        """Get runs of this pipeline.

        Can be used to fetch runs other than `self.runs` and supports
        fine-grained filtering and pagination.

        Args:
            **kwargs: Further arguments for filtering or pagination that are
                passed to `client.list_pipeline_runs()`.

        Returns:
            List of runs of this pipeline.
        """
        from zenml.client import Client

        return Client().list_pipeline_runs(pipeline_id=self.id, **kwargs).items

    @property
    def runs(self) -> List["PipelineRunResponse"]:
        """Returns the 20 most recent runs of this pipeline in descending order.

        Returns:
            The 20 most recent runs of this pipeline in descending order.
        """
        return self.get_runs()

    @property
    def num_runs(self) -> int:
        """Returns the number of runs of this pipeline.

        Returns:
            The number of runs of this pipeline.
        """
        from zenml.client import Client

        return Client().list_pipeline_runs(pipeline_id=self.id, size=1).total

    @property
    def last_run(self) -> "PipelineRunResponse":
        """Returns the last run of this pipeline.

        Returns:
            The last run of this pipeline.

        Raises:
            RuntimeError: If no runs were found for this pipeline.
        """
        runs = self.get_runs(size=1)
        if not runs:
            raise RuntimeError(
                f"No runs found for pipeline '{self.name}' with id {self.id}."
            )
        return runs[0]

    @property
    def last_successful_run(self) -> "PipelineRunResponse":
        """Returns the last successful run of this pipeline.

        Returns:
            The last successful run of this pipeline.

        Raises:
            RuntimeError: If no successful runs were found for this pipeline.
        """
        runs = self.get_runs(status=ExecutionStatus.COMPLETED, size=1)
        if not runs:
            raise RuntimeError(
                f"No successful runs found for pipeline '{self.name}' with id "
                f"{self.id}."
            )
        return runs[0]

    # Body and metadata properties
    @property
    def status(self) -> Optional[List[ExecutionStatus]]:
        """The `status` property.

        Returns:
            the value of the property.
        """
        return self.get_body().status

    @property
    def latest_run_id(self) -> Optional[UUID]:
        """The `latest_run_id` property.

        Returns:
            the value of the property.
        """
        return self.get_body().latest_run_id

    @property
    def latest_run_status(self) -> Optional[ExecutionStatus]:
        """The `latest_run_status` property.

        Returns:
            the value of the property.
        """
        return self.get_body().latest_run_status


# ------------------ Filter Model ------------------


class PipelineFilter(WorkspaceScopedFilter):
    """Pipeline filter model."""

    name: Optional[str] = Field(
        default=None,
        description="Name of the Pipeline",
    )
    workspace_id: Optional[Union[UUID, str]] = Field(
        default=None,
        description="Workspace of the Pipeline",
        union_mode="left_to_right",
    )
    user_id: Optional[Union[UUID, str]] = Field(
        default=None,
        description="User of the Pipeline",
        union_mode="left_to_right",
    )
