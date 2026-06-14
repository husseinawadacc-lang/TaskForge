export type BillingInfo = {
  plan: string
  status: string
  expires_at: string | null
}

export type CheckoutResponse = {
  checkout_url: string
}

export type BillingActionResponse = {
  message: string
}