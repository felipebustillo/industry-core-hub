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
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

from uuid import UUID
from typing import List, Optional

from tractusx_sdk.extensions.notification_api.models import Notification

from managers.config.log_manager import LoggingManager
from managers.metadata_database.manager import RepositoryManagerFactory
from models.metadata_database.notification.models import NotificationStatus, NotificationDirection, NotificationEntity

logger = LoggingManager.get_logger(__name__)

class NotificationsManagementService():
    """
    Service class for managing notifications.
    """

    def create_notification(self, notification: Notification, direction: NotificationDirection) -> NotificationEntity:
        """
        Create a new notification in the system.
        """
        status: NotificationStatus
        if direction == NotificationDirection.INCOMING:
            logger.info(f"Creating incoming notification with ID: {notification.header.message_id}")
            status = NotificationStatus.RECEIVED
        elif direction == NotificationDirection.OUTGOING:
            logger.info(f"Creating outgoing notification with ID: {notification.header.message_id}")
            status = NotificationStatus.PENDING
        
        with RepositoryManagerFactory().create() as repos:

            notification_data = repos.notification_repository.create_new(
                notification=notification,
                direction=direction,
                status=status
            )
            return notification_data

    def update_notification_status(self, message_id: UUID, new_status: NotificationStatus) -> Optional[NotificationEntity]:
        """
        Update the status of an existing notification identified by its message_id.
        """
        with RepositoryManagerFactory().create() as repos:
            db_obj = repos.notification_repository.update_status(message_id=message_id, new_status=new_status)
            return db_obj
        
    def get_all_notifications(self, bpn: str, status: Optional[NotificationStatus] = None, offset: int = 0, limit: int = 100) -> List[NotificationEntity]:
        """
        Retrieve all notifications from the database, optionally filtered by BPN and status, with pagination support.
        """
        with RepositoryManagerFactory().create() as repos:
            notifications = repos.notification_repository.find_by_bpn(bpn=bpn, status=status, offset=offset, limit=limit)
            return notifications
        
    def delete_notification(self, message_id: UUID) -> bool:
        """
        Delete a notification from the database by its message_id.
        """
        with RepositoryManagerFactory().create() as repos:
            success = repos.notification_repository.delete_by_message_id(message_id=message_id)
            return success
