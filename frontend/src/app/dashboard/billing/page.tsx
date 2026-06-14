"use client"

import toast from "react-hot-toast"

import BillingCard from "@/features/billing/components/BillingCard"
import BillingActions from "@/features/billing/components/BillingAction"
import BillingSkeleton from "@/features/billing/components/BillingSkeleton"

import { useBilling } from "@/features/billing/hooks/useBilling"

export default function BillingPage() {

  const {
    billing,
    loading,
    error,

    upgradePlan,
    downgradePlan,
    cancelSubscription,
    createCheckout,

  } = useBilling()

  const handleUpgrade = async () => {

    try {

      const result = await upgradePlan()

      toast.success(
        result.message || "Plan upgraded"
      )

    } catch (err: any) {

      toast.error(
        err.message || "Upgrade failed"
      )
    }
  }

  const handleDowngrade = async () => {

    try {

      const result = await downgradePlan()

      toast.success(
        result.message || "Plan downgraded"
      )

    } catch (err: any) {

      toast.error(
        err.message || "Downgrade failed"
      )
    }
  }

  const handleCancel = async () => {

    try {

      const result = await cancelSubscription()

      toast.success(
        result.message || "Subscription cancelled"
      )

    } catch (err: any) {

      toast.error(
        err.message || "Cancellation failed"
      )
    }
  }

  const handleCheckout = async () => {

    try {

      const result = await createCheckout(2) // Example plan ID

      if (result.checkout_url) {

        window.location.href =
          result.checkout_url
      }

    } catch (err: any) {

      toast.error(
        err.message || "Checkout failed"
      )
    }
  }

  if (loading) {

    return (
      <div className="p-6">
        <BillingSkeleton />
      </div>
    )
  }

  if (error) {

    return (
      <div className="p-6 text-red-500">
        {error}
      </div>
    )
  }

  return (

    <div className="p-6 max-w-4xl space-y-6">

      <h1 className="text-3xl font-bold">
        Billing
      </h1>

      {billing && (

        <BillingCard
          plan={billing.plan}
          status={billing.status}
          expiresAt={billing.expires_at}
        />
      )}

      <BillingActions
        onUpgrade={handleUpgrade}
        onDowngrade={handleDowngrade}
        onCancel={handleCancel}
        onCheckout={handleCheckout}
      />

    </div>
  )
}