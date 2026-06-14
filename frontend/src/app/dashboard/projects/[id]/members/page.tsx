"use client"

import { useParams } from "next/navigation"
import { useState } from "react"
import { useMembers } from "@/features/projects/hooks/useMembers"

export default function MembersPage() {
  const params = useParams()

  const projectId = Number(params.id)

  const {
    members,
    loading,
    error,
    addMember,
    removeMember,
  } = useMembers(projectId)

  const [userId, setUserId] = useState("")
  const [role, setRole] = useState("member")

  const handleAdd = async () => {
    if (!userId) return

    await addMember(
      Number(userId),
      role
    )

    setUserId("")
    setRole("member")
  }

  if (loading) {
    return <p>Loading members...</p>
  }

  return (
    <div className="p-6">

      <h1 className="text-2xl font-bold mb-6">
        Project Members 👥
      </h1>

      {error && (
        <p className="text-red-500 mb-4">
          {error}
        </p>
      )}

      {/* Add Member */}
      <div className="flex gap-2 mb-6">

        <input
          type="number"
          placeholder="User ID"
          value={userId}
          onChange={(e) =>
            setUserId(e.target.value)
          }
          className="border p-2 rounded"
        />

        <select
          value={role}
          onChange={(e) =>
            setRole(e.target.value)
          }
          className="border p-2 rounded"
        >
          <option value="admin">
            admin
          </option>

          <option value="member">
            member
          </option>

          <option value="viewer">
            viewer
          </option>
        </select>

        <button
          onClick={handleAdd}
          className="
            bg-indigo-500
            text-white
            px-4
            py-2
            rounded
          "
        >
          Add Member
        </button>

      </div>

      {/* Members List */}
      <div className="space-y-3">

        {members.map((member) => (

          <div
            key={member.user_id}
            className="
              flex
              justify-between
              items-center
              p-4
              bg-white
              rounded-xl
              shadow
            "
          >
            <div>
              <p>
                User #{member.user_id}
              </p>

              <p className="text-sm text-gray-500">
                {member.role}
              </p>
            </div>

            <button
              onClick={() =>
                removeMember(
                  member.user_id
                )
              }
              className="
                text-red-500
                hover:underline
              "
            >
              Remove
            </button>

          </div>

        ))}

      </div>

    </div>
  )
}