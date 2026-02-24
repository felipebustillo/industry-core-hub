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
from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import Response

from tractusx_sdk.extensions.notification_api.models import (
    Notification)

from controllers.fastapi.routers.authentication.auth_api import get_authentication_dependency

router = APIRouter(
    prefix="/notifications-management",
    tags=["Notifications Management"],
    dependencies=[Depends(get_authentication_dependency())]
)

@router.post("/notifications")
async def get_all_notifications(offset: int = 0, limit: int = 10) -> List[Notification]:
    # TODO: Implement the logic to retrieve all notifications with pagination support (offset and limit) and return the list of notifications
    return NotImplementedType("Get all notifications endpoint is not implemented yet")

@router.post("/notification")
async def send_notification(notification: Notification) -> Response:
    # TODO: Implement the logic to send a notification and return the appropriate response
    return NotImplementedType("Send notification endpoint is not implemented yet")

@router.delete("/notification")
async def delete_notification(id: str) -> Response:
    # TODO: Implement the logic to delete a notification by its ID and return the appropriate response
    return NotImplementedType("Delete notification endpoint is not implemented yet")
