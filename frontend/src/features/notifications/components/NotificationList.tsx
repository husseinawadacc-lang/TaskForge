import NotificationCard from "./NotificationCard"

import { Notification } from "../types"

type Props = {
  notifications: Notification[]

  onMarkAsRead: (
    notificationId: number
  ) => void
}

export default function NotificationList({
  notifications,
  onMarkAsRead,
}: Props) {

  return (

    <div className="space-y-4">

      {notifications.map(notification => (

        <NotificationCard
          key={notification.id}
          title={notification.title}
          message={notification.message}
          isRead={notification.is_read}
          onMarkAsRead={() =>
            onMarkAsRead(notification.id)
          }
        />

      ))}

    </div>

  )
}