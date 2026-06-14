"use client"

import { useEffect, useState } from "react"

import {
  getNotificationsAPI,
  getUnreadCountAPI,
  markAsReadAPI,
} from "../api"

import { Notification } from "../types"

export function useNotifications() {

  const [notifications, setNotifications] = useState<Notification[]>([])

  const [unreadCount, setUnreadCount] = useState(0)

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState<string | null>(null)

  /*
  📥 Load notifications
  */
  const fetchNotifications = async () => {

    try {

      setLoading(true)

      setError(null)

      const data = await getNotificationsAPI()

      setNotifications(data)

    } catch (err: any) {

      setError(
        err.message || "Failed to load notifications"
      )

    } finally {

      setLoading(false)

    }
  }

  /*
  🔔 Load unread count
  */
  const fetchUnreadCount = async () => {

    try {

      const data = await getUnreadCountAPI()

      setUnreadCount(data.unread_count)

    } catch (err) {

      console.error(
        "Unread count error:",
        err
      )

    }
  }

  /*
  ✅ Mark notification as read
  */
  const markAsRead = async (
    notificationId: number
  ) => {

    try {

      await markAsReadAPI(notificationId)

      setNotifications(prev =>
        prev.map(notification =>
          notification.id === notificationId
            ? {
                ...notification,
                is_read: true,
              }
            : notification
        )
      )

      setUnreadCount(prev =>
        Math.max(prev - 1, 0)
      )

    } catch (err: any) {

      setError(
        err.message ||
        "Failed to mark notification as read"
      )
    }
  }

  /*
  🚀 Initial load
  */
  useEffect(() => {

    fetchNotifications()

    fetchUnreadCount()

  }, [])

  return {

    notifications,

    unreadCount,

    loading,

    error,

    markAsRead,

    refreshNotifications:
      fetchNotifications,

    refreshUnreadCount:
      fetchUnreadCount,
  }
}