"use client"

import { useRouter } from "next/navigation"
import { useEffect } from "react"

export default function DashboardPage() {

  const router = useRouter()

  const handleLogout =()=> {
    alert("Logging out...")
    console.log("Logging out...")
    localStorage.removeItem("token")
    localStorage.removeItem("refresh")
    // document.cookie = "token=; path=/; max-age=0"
    // document.cookie = "refresh=; path=/; max-age=0"
    router.replace ("/login")
  }


  useEffect(() => {
    const token = localStorage.getItem("token")

    if (!token || token === "undefined" || token.length < 10){
      
      router.replace("/login")
    }
  }, [])


  return (
    <div className="p-6">

      <div className="flex justify-between mb-6">
        <h1 className="text-2xl font-bold">Dashboard 🚀</h1>

        <button
          onClick={handleLogout }
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Logout
        </button>
      </div>

      <p className="text-gray-500">
        Welcome to your dashboard 👋
      </p>

    </div>
  )
}