"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import toast from "react-hot-toast"
import Link from "next/link"  
export default function LoginPage() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const router = useRouter()
  
  const handleLogin = async () => {
    console.log("LOGIN CLICKED")
    console.log({email, password})
    const res = await fetch("http://localhost:8001/api/v1/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })

    const data = await res.json()
    if (!res.ok) {
  console.log("Login failed", data)

  const message = Array.isArray(data.detail)
    ? data.detail[0]?.msg
    : data.detail

  toast.error(message || "Login failed")

  return
}
    // 🔥 التخزين هنا
    localStorage.setItem("token", data.access_token)
    localStorage.setItem("refresh", data.refresh_token)
    // document.cookie = `token=${data.access_token}; path=/`
    // document.cookie = `refresh=${data.refresh_token}; path=/`
    // 🚀 تحويل
    router.push("/dashboard/tasks")
  }
  useEffect(() => {
    const token = localStorage.getItem("token")
    if (token && token !== "undefined") {
      if (token.length > 10) 
        router.replace("/dashboard/tasks")
      
    }
  }, [])

  return (
    <div className="flex flex-col gap-4 p-6 max-w-sm mx-auto mt-20">

      <h1 className="text-2xl font-bold text-center">Login</h1>

      <input
  type="email"
  placeholder="Email"
  value={email}
  onChange={(e) => {
    console.log("EMAIL:", e.target.value)
    setEmail(e.target.value)
  }}
  className="border p-2 rounded"
/>

<input
  type="password"
  placeholder="Password"
  value={password}
  onChange={(e) => {
    console.log("PASSWORD:", e.target.value)
    setPassword(e.target.value)
  }}
  className="border p-2 rounded"
/>

      <button
        onClick={handleLogin}
        className="bg-indigo-500 text-white p-2 rounded"
      >
        Login
      </button>

      <p className="text-sm text-center">
      <Link
        href="/forgot-password"
        className="text-indigo-500 underline"
      >
        Forgot Password?
      </Link>
    </p>
      <Link
        href="/register"
        className="text-sm text-gray-500 mt-2"
      >
        Don't have an account? Register
      </Link>
    </div>
  )
}
