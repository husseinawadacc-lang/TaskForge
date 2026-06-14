export type Notification = {
  id: number
  title: string
  message: string
  type: string
  is_read: boolean
  created_at: string
}

export type UnreadCountResponse = {
  unread_count: number
}