"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import toast from "react-hot-toast"

export default function ResetPasswordPage() {

  const router = useRouter()

  const [token, setToken] = useState("")
  const [password, setPassword] = useState("")

  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {

    if (!token.trim() || !password.trim()) {
      toast.error("All fields are required")
      return
    }

    setLoading(true)

    try {

      const res = await fetch(
        "http://localhost:8001/api/v1/auth/password-reset/confirm",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            token,
            password,
          }),
        }
      )

      const data = await res.json()

      if (!res.ok) {
        throw new Error(
          data.detail || "Reset failed"
        )
      }

      toast.success(
        "Password reset successfully ✅"
      )

      router.push("/login")

    } catch (err: any) {

      toast.error(
        err.message ||
        "Failed to reset password"
      )

    } finally {

      setLoading(false)

    }
  }

  return (
    <div className="flex flex-col gap-4 p-6 max-w-sm mx-auto mt-20">

      <h1 className="text-2xl font-bold text-center">
        Reset Password
      </h1>

      <p className="text-sm text-gray-500 text-center">
        Enter the reset token and your new password.
      </p>

      <input
        type="text"
        placeholder="Reset Token"
        value={token}
        onChange={(e) =>
          setToken(e.target.value)
        }
        className="border p-2 rounded"
      />

      <input
        type="password"
        placeholder="New Password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
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
          ? "Resetting..."
          : "Reset Password"}
      </button>

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