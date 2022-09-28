#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
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
"""Zen Server AWS Terraform deployer implementation."""

import os
from pathlib import Path
from typing import ClassVar, List, Optional, Tuple, Type, cast

from zenml.enums import ServerProviderType
from zenml.logger import get_logger
from zenml.zen_server.deploy.deployment import ServerDeploymentConfig
from zenml.zen_server.deploy.terraform.providers.terraform_provider import (
    TerraformServerProvider,
)
from zenml.zen_server.deploy.terraform.terraform_zen_server import (
    TerraformServerDeploymentConfig,
)

logger = get_logger(__name__)


class AWSServerDeploymentConfig(TerraformServerDeploymentConfig):
    """AWS server deployment configuration.

    Attributes:
    """
    region: str = "eu-west-1"
    rds_db_username: str = "admin"
    rds_db_password: str = ""
    create_rds: bool = True
    db_name: str = "zenmlserver"
    db_type: str = "mysql"
    db_version: str = "8.0.28"
    db_instance_class: str = "db.t3.micro"
    db_allocated_storage: int = 5


class AWSServerProvider(TerraformServerProvider):
    """AWS ZenML server provider."""

    TYPE: ClassVar[ServerProviderType] = ServerProviderType.AWS
    CONFIG_TYPE: ClassVar[
        Type[TerraformServerDeploymentConfig]
    ] = AWSServerDeploymentConfig


AWSServerProvider.register_as_provider()
