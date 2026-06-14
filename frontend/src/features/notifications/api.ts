import { apiFetch } from "@/lib/api"

export const getNotificationsAPI = async () => {
  return await apiFetch("/api/v1/notifications")
}

export const markAsReadAPI = async (
  notificationId: number
) => {
  return await apiFetch(
    `/api/v1/notifications/${notificationId}/read`,
    {
      method: "PATCH",
    }
  )
}

export const getUnreadCountAPI = async () => {
  return await apiFetch(
    "/api/v1/notifications/unread-count"
  )
}