"use client"

import { useEffect, useState } from "react"

import {
  getBillingAPI,
  createCheckoutAPI,
  upgradePlanAPI,
  downgradePlanAPI,
  cancelSubscriptionAPI,
} from "../api"

import { BillingInfo } from "../types"

export function useBilling() {

  const [billing, setBilling] =
    useState<BillingInfo | null>(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState("")

  const fetchBilling = async () => {

    try {

      const data =
        await getBillingAPI()

      setBilling(data)

    } catch (err: any) {

      setError(
        err.message ||
        "Failed to load billing"
      )

    } finally {

      setLoading(false)

    }
  }

  useEffect(() => {

    fetchBilling()

  }, [])

  const upgradePlan = async () => {

    return await upgradePlanAPI(2)

  }

  const downgradePlan = async () => {

    return await downgradePlanAPI(2)

  }

  const cancelSubscription = async () => {

    return await cancelSubscriptionAPI()

  }

  const createCheckout = async (planId: number) => {

    return await createCheckoutAPI(planId)

  }

  return {

    billing,
    loading,
    error,

    fetchBilling,

    upgradePlan,
    downgradePlan,
    cancelSubscription,
    createCheckout,
  }
}