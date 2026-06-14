"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"

export default function RegisterPage() {

  // 🧠 Form State
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  // ⏳ Loading State
  const [loading, setLoading] = useState(false)

  // ❌ Error State
  const [error, setError] = useState("")

  const router = useRouter()

  /*
  🔒 إذا كان المستخدم مسجل دخول بالفعل
  */
  useEffect(() => {
    const token = localStorage.getItem("token")

    if (
      token &&
      token !== "undefined" &&
      token.length > 10
    ) {
      router.replace("/dashboard/tasks")
    }
  }, [router])

  /*
  🚀 Register User
  */
  const handleRegister = async () => {

    // ✅ Basic Validation
    if (!email.trim() || !password.trim()) {
      setError("All fields are required")
      return
    }

    setLoading(true)
    setError("")

    try {

      const res = await fetch(
        "http://localhost:8001/api/v1/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            password,
          }),
        }
      )

      // ❌ Backend Error
      if (!res.ok) {
        const err = await res.json()

        throw new Error(
          err.detail || "Register failed"
        )
      }

      // ✅ Registration Success
      await res.json()

      // 🚀 Redirect to Login
      router.push("/login")

    } catch (err: any) {

      setError(
        err.message || "Registration failed"
      )

    } finally {

      setLoading(false)

    }
  }

  return (
    <div className="flex flex-col gap-4 p-6 max-w-sm mx-auto mt-20">

      <h1 className="text-2xl font-bold text-center">
        Create Account 🚀
      </h1>

      {/* 📧 Email */}
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
        className="border p-2 rounded"
      />

      {/* 🔑 Password */}
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
        className="border p-2 rounded"
      />

      {/* ❌ Error */}
      {error && (
        <p className="text-red-500 text-sm">
          {error}
        </p>
      )}

      {/* 🔘 Register Button */}
      <button
        onClick={handleRegister}
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
          ? "Creating..."
          : "Register"}
      </button>

      {/* 🔗 Login Link */}
      <p className="text-sm text-center">
        Already have an account?{" "}
        <Link
          href="/login"
          className="
            text-indigo-500
            underline
          "
        >
          Login
        </Link>
      </p>

    </div>
  )
}