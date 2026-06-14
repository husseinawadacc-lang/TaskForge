"use client"

import { useEffect, useState } from "react"
import { apiFetch } from "@/lib/api"
import toast from "react-hot-toast"
import { useRouter } from "next/navigation"

type User = {
  id: number
  email: string
  role: string
  is_active: boolean
  created_at: string
}

export default function ProfilePage() {

  const [user, setUser] = useState<User | null>(null)

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState("")

  const router = useRouter()
  
  useEffect(() => {

    const fetchProfile = async () => {

      try {

        const data = await apiFetch(
          "/api/v1/auth/me"
        )

        setUser(data)

      } catch (err: any) {

        setError(
          err.message || "Failed to load profile"
        )

      } finally {

        setLoading(false)

      }
    }

    fetchProfile()

  }, [])

    const handleLogout = async () => {
    try {
      await apiFetch(
        "/api/v1/auth/logout-all",
        {
          method: "POST",
        }
      )
      toast.success("Logged out of all devices")
      localStorage.removeItem("token")
      localStorage.removeItem("refresh")
      router.push("/login")
    } catch (err: any) {
      toast.error(err.message || "Failed to logout")
    }
  }

  if (loading) {
    return (
      <div className="p-6">
        Loading profile...
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
    <div className="p-6 max-w-xl">

      <h1 className="text-3xl font-bold mb-6">
        My Profile
      </h1>

      <div className="space-y-4 bg-white shadow rounded-xl p-6">

        <div>
          <p className="text-sm text-gray-500">
            User ID
          </p>

          <p className="font-medium">
            {user?.id}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Email
          </p>

          <p className="font-medium">
            {user?.email}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Role
          </p>

          <p className="font-medium">
            {user?.role}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Status
          </p>

          <p className="font-medium">
            {user?.is_active
              ? "Active ✅"
              : "Inactive ❌"}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Created At
          </p>

          <p className="font-medium">
            {user?.created_at}
          </p>
        </div>
        <button
        onClick={handleLogout}
        className="mt-4 w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition"
      >
        Logout ALL Devices
      </button>
      </div>

    </div>
  )
}