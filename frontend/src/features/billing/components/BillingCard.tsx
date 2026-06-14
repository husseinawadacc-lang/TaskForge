type Props = {
  plan: string
  status: string
  expiresAt: string | null
}

export default function BillingCard({
  plan,
  status,
  expiresAt,
}: Props) {
  return (
    <div className="bg-white rounded-xl shadow p-6 space-y-3">

      <h2 className="text-xl font-bold">
        Current Subscription
      </h2>

      <div>
        <p className="text-sm text-gray-500">
          Plan
        </p>

        <p className="font-medium">
          {plan}
        </p>
      </div>

      <div>
        <p className="text-sm text-gray-500">
          Status
        </p>

        <p className="font-medium">
          {status}
        </p>
      </div>

      <div>
        <p className="text-sm text-gray-500">
          Expires At
        </p>

        <p className="font-medium">
          {expiresAt || "Never"}
        </p>
      </div>

    </div>
  )
}