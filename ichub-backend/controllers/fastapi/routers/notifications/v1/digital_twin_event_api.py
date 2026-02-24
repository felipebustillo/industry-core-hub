#################################################################################
# Eclipse Tractus-X - Industry Core Hub Backend
#
# Copyright (c) 2026 LKS Next
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

from types import NotImplementedType
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from tractusx_sdk.extensions.notification_api.models import (
    Notification)

from controllers.fastapi.routers.authentication.auth_api import get_authentication_dependency

router = APIRouter(
    prefix="/digital-twin-event",
    tags=["Digital Twin Event Management"],
    dependencies=[Depends(get_authentication_dependency())]
)

@router.post("/connect-to-parent")
async def connect_to_parent(notification: Notification) -> Response:
    # TODO: Implement the logic to handle the connection to the parent endpoint and process the received notification
    return NotImplementedType("Connect to parent endpoint is not implemented yet")

@router.post("/connect-to-child")
async def connect_to_child(notification: Notification) -> Response:
    # TODO: Implement the logic to handle the connection to the child endpoint and process the received notification
    return NotImplementedType("Connect to child endpoint is not implemented yet")

@router.post("/submodel-update")
async def submodel_update(notification: Notification) -> Response:
    # TODO: Implement the logic to handle the submodel update and process the received notification
    return NotImplementedType("Submodel update endpoint is not implemented yet")

@router.post("/feedback")
async def feedback(notification: Notification) -> Response:
    # TODO: Implement the logic to handle the feedback and process the received notification
    return NotImplementedType("Feedback endpoint is not implemented yet")
