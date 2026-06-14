import { apiFetch } from "@/lib/api"
import {
  BillingInfo,
  CheckoutResponse,
  BillingActionResponse,
} from "./types"

export const getBillingAPI = async (): Promise<BillingInfo> => {
  return await apiFetch("/api/v1/billing")
}

export const createCheckoutAPI = async (planId: number): Promise<CheckoutResponse> => {
  return await apiFetch(
    `/api/v1/billing/checkout?plan_id=${planId}`, {
    method: "POST",
  })
}

export const upgradePlanAPI = async (planId: number): Promise<BillingActionResponse> => {
  return await apiFetch(`/api/v1/billing/upgrade?plan_id=${planId}`, {
    method: "POST",
  })
}

export const downgradePlanAPI = async (planId: number): Promise<BillingActionResponse> => {
  return await apiFetch(`/api/v1/billing/downgrade?plan_id=${planId}`, {
    method: "POST",
  })
}

export const cancelSubscriptionAPI = async (): Promise<BillingActionResponse> => {
  return await apiFetch("/api/v1/billing/cancel", {
    method: "POST",
  })
}