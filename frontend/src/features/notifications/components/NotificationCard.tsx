type Props = {
  title: string
  message: string
  isRead: boolean
  onMarkAsRead: () => void
}

export default function NotificationCard({
  title,
  message,
  isRead,
  onMarkAsRead,
}: Props) {

  return (

    <div
      className={`
        p-4
        rounded-xl
        shadow
        border
        bg-white
        flex
        justify-between
        items-center
        ${
          !isRead
            ? "border-indigo-500"
            : "border-gray-200"
        }
      `}
    >

      <div>

        <h3 className="font-semibold">
          {title}
        </h3>

        <p className="text-sm text-gray-500">
          {message}
        </p>

      </div>

      {!isRead && (

        <button
          onClick={onMarkAsRead}
          className="
            px-3
            py-1
            text-sm
            bg-indigo-500
            text-white
            rounded
            hover:bg-indigo-600
          "
        >
          Mark as Read
        </button>

      )}

    </div>

  )
}