from fastapi import APIRouter, Depends, HTTPException
from typing import List

from modules.notifications.schemas.notification_schema import NotificationOut
from modules.notifications.dependencies import get_notification_service
from modules.notifications.service.notification_service import NotificationService

from api.deps.auth_dep import get_current_user


router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[NotificationOut])
def get_notifications(
    current_user=Depends(get_current_user),
    notification_service: NotificationService = Depends(get_notification_service),
):
    return notification_service.get_user_notifications(user_id=current_user.id)

@router.patch("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    current_user=Depends(get_current_user),
    notification_service: NotificationService = Depends(get_notification_service),
):
    success = notification_service.mark_as_read(
        notification_id=notification_id,
        user_id=current_user.id,
    )

    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")

    return {"message": "Notification marked as read"}

@router.get("/unread-count")
def get_unread_count(
    current_user=Depends(get_current_user),
    notification_service: NotificationService = Depends(get_notification_service),
):
    count = notification_service.get_unread_count(user_id=current_user.id)
    return {"unread_count": count}