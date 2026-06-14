"use client"

import { useEffect, useState } from "react"
import {
  getMembersAPI,
  addMemberAPI,
  removeMemberAPI,
} from "../api"
import toast from "react-hot-toast"

export type Member = {
  user_id: number
  role: string
}

export function useMembers(projectId: number | null) {
  const [members, setMembers] = useState<Member[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  /*
  🔥 تحميل الأعضاء
  */
  useEffect(() => {
    if (!projectId) {
      setMembers([])
      return
    }

    const fetchMembers = async () => {
      try {
        setLoading(true)
        setError(null)

        const data = await getMembersAPI(projectId)
        console.log("Members data:", data)
        /*
        الباك يرجع dict:
        {
          "1": "admin",
          "2": "member"
        }
        */
        const membersData = data.members || {}

        const list = Object.entries(membersData).map(
          ([userId, role]) => ({
            user_id: Number(userId),
            role: String(role),
          })
        )

        setMembers(list)

      } catch (err: any) {
        console.error("Members error:", err)

        setError(
          err.message || "Failed to load members"
        )
      } finally {
        setLoading(false)
      }
    }

    fetchMembers()

  }, [projectId])

  /*
  ➕ إضافة عضو
  */
  const addMember = async (
    userId: number,
    role: string
  ) => {
    if (!projectId) return

    try {
      await addMemberAPI(
        projectId,
        userId,
      )

      setMembers((prev) => [
        ...prev,
        {
          user_id: userId,
          role,
        },
      ])

      toast.success("Member Added ✅")

    } catch (err: any) {
      console.error(
        "Add member error:",
        err
      )

      toast.error(
        err.message || "Failed to add member"
      )
    }
  }

  /*
  🗑 حذف عضو
  */
  const removeMember = async (
    userId: number
  ) => {
    if (!projectId) return

    try {
      await removeMemberAPI(
        projectId,
        userId
      )

      setMembers((prev) =>
        prev.filter(
          (member) =>
            member.user_id !== userId
        )
      )

      toast.success("Member Removed 🗑")

    } catch (err: any) {
      console.error(
        "Remove member error:",
        err
      )

      toast.error(
        err.message ||
        "Failed to remove member"
      )
    }
  }

  return {
    members,
    loading,
    error,
    addMember,
    removeMember,
  }
}