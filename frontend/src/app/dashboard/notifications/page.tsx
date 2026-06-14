"use client"

import NotificationEmpty from "@/features/notifications/components/NotificationEmpty"
import NotificationList from "@/features/notifications/components/NotificationList"
import NotificationSkeleton from "@/features/notifications/components/NotificationSkeleton"

import { useNotifications } from "@/features/notifications/hooks/useNotifications"

export default function NotificationsPage() {

  const {
    notifications,
    loading,
    error,
    unreadCount,
    markAsRead,
  } = useNotifications()

  /*
  ⏳ Loading UI
  */
  if (loading) {
    return (
      <div className="p-6">

        <h1 className="text-3xl font-bold mb-6">
          Notifications
        </h1>

        <NotificationSkeleton />

      </div>
    )
  }

  /*
  ❌ Error UI
  */
  if (error) {
    return (
      <div className="p-6">

        <h1 className="text-3xl font-bold mb-6">
          Notifications
        </h1>

        <p className="text-red-500">
          {error}
        </p>

      </div>
    )
  }

  return (

    <div className="p-6">

      {/* 🔔 Header */}
      <div className="flex justify-between items-center mb-6">

        <div>

          <h1 className="text-3xl font-bold">
            Notifications
          </h1>

          <p className="text-gray-500 text-sm">
            Stay updated with recent activity.
          </p>

        </div>

        {/* 🔴 Unread Badge */}
        <div
          className="
            bg-indigo-500
            text-white
            px-4
            py-2
            rounded-full
            text-sm
          "
        >
          Unread: {unreadCount}
        </div>

      </div>

      {/* 📭 Empty State */}
      {notifications.length === 0 ? (

        <NotificationEmpty />

      ) : (

        <NotificationList
          notifications={notifications}
          onMarkAsRead={markAsRead}
        />

      )}

    </div>

  )
}