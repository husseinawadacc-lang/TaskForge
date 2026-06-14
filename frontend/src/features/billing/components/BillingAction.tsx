type Props = {
  onUpgrade: () => void
  onDowngrade: () => void
  onCancel: () => void
  onCheckout: () => void
}

export default function BillingActions({
  onUpgrade,
  onDowngrade,
  onCancel,
  onCheckout,
}: Props) {

  return (

    <div className="grid grid-cols-2 gap-3 mt-6">

      <button
        onClick={onCheckout}
        className="bg-indigo-500 text-white py-2 rounded-lg"
      >
        Checkout
      </button>

      <button
        onClick={onUpgrade}
        className="bg-green-500 text-white py-2 rounded-lg"
      >
        Upgrade
      </button>

      <button
        onClick={onDowngrade}
        className="bg-yellow-500 text-white py-2 rounded-lg"
      >
        Downgrade
      </button>

      <button
        onClick={onCancel}
        className="bg-red-500 text-white py-2 rounded-lg"
      >
        Cancel
      </button>

    </div>

  )
}