"use client"

import { useState } from "react"
import { useProjects } from "@/features/projects/hooks/useProjects"
import { useRouter } from "next/navigation"

export default function ProjectsPage() {
  const {
    projects,
    createProject,
    deleteProject,
    loading,
    error,}
    = useProjects()

  const [name, setName] = useState("")
  
  const router = useRouter()
  const handleCreate = async () => {
    if (!name.trim()) return
    
    await createProject(name)
    setName("")
  }

    if (loading)
      { return <p>Loading...</p>}
    if (error){
       return (<p className="text-red-500">{error}</p>)}


  
  return (
    <div>

      <h1 className="text-2xl font-bold mb-4">
        Projects 📁
      </h1>

      <p className="text-gray-500 mb-4">
        Manage your projects
      </p>

      {/* 🔥 input + button */}
      <div className="flex gap-2 mb-6">

        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Project name..."
          className="border p-2 rounded"
        />

        <button
          onClick={handleCreate}
          className="bg-indigo-500 text-white px-4 py-2 rounded
          hover:bg-indigo-600 transition"
        >
          Create Project
        </button>

      </div>
      { projects.length === 0 && (
        <p className="text-gray-500">
          No projects yet. Create one to get started!
        </p>
      ) }
      {/* 📋 عرض المشاريع */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 ">
       {projects.map((p) => (
        <div
          key={p.id}
          className="bg-white p-4 rounded-xl shadow"
        >
          <h2 className="text-lg font-semibold">
            {p.name}
          </h2>

          <p className="text-sm text-gray-500 mt-1">
            Manage tasks inside this project
          </p>

          <div className="flex gap-2 mt-4">

            <button
              onClick={() =>
                router.push(
                  `/dashboard/tasks?project=${p.id}`
                )
              }
              className="
                bg-indigo-500
                text-white
                px-3
                py-1
                rounded
              "
            >
              Tasks
            </button>

            <button
              onClick={() =>
                router.push(
                  `/dashboard/projects/${p.id}/members`
                )
              }
              className="
                bg-gray-500
                text-white
                px-3
                py-1
                rounded
              "
            >
              Members
            </button>

            <button
              onClick={() => deleteProject(p.id)}
              className="
                text-red-500
                hover:underline
              "
            >
              Delete Project
            </button>

          </div>

        </div>
      ))}
      </div>

    </div>
  )
}