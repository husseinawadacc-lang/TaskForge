"use client"

import { useState } from "react"
import Link from "next/link"
import toast from "react-hot-toast"

export default function ForgotPasswordPage() {

  const [email, setEmail] = useState("")

  const [loading, setLoading] = useState(false)

  const [message, setMessage] = useState("")

  const handleSubmit = async () => {

    if (!email.trim()) {
      toast.error("Email is required")
      return
    }

    setLoading(true)
    setMessage("")

    try {

      const res = await fetch(
        "http://localhost:8001/api/v1/auth/password-reset/request",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
          }),
        }
      )

      const data = await res.json()

      if (!res.ok) {
        throw new Error(
          data.detail || "Request failed"
        )
      }

      setMessage(data.message)

      toast.success(
        "Request sent successfully"
      )

    } catch (err: any) {

      toast.error(
        err.message ||
        "Failed to send request"
      )

    } finally {

      setLoading(false)

    }
  }

  return (
    <div className="flex flex-col gap-4 p-6 max-w-sm mx-auto mt-20">

      <h1 className="text-2xl font-bold text-center">
        Forgot Password
      </h1>

      <p className="text-sm text-gray-500 text-center">
        Enter your email address to receive
        a password reset link.
      </p>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
        className="border p-2 rounded"
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="
          bg-indigo-500
          text-white
          p-2
          rounded
          disabled:opacity-50
        "
      >
        {loading
          ? "Sending..."
          : "Send Reset Link"}
      </button>

      {message && (
        <p className="text-green-600 text-sm">
          {message}
        </p>
      )}

      <Link
        href="/login"
        className="
          text-center
          text-indigo-500
          underline
          text-sm
        "
      >
        Back to Login
      </Link>

    </div>
  )
}