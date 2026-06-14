export default function NotificationSkeleton() {

  return (

    <div className="space-y-4">

      {[1, 2, 3].map(item => (

        <div
          key={item}
          className="
            h-24
            rounded-xl
            bg-gray-200
            animate-pulse
          "
        />

      ))}

    </div>

  )
}