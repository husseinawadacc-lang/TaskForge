"use client"

import { useEffect, useState } from "react"
import { createProjectAPI, getProjects,deleteProjectAPI } from "../api"
import toast from "react-hot-toast"

export type Project = {
  id: number
  name: string
}

export function useProjects() {

  const [projects, setProjects] = useState<Project[]>([])
  const [selectedProject, setSelectedProject] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProjects = async () => {
      
    
    try {
      setLoading(true)
        setError(null)
        const data = await getProjects()

        console.log("PROJECTS:", data)

        setProjects(data)

      
      } catch (err: any) {
        console.error("Projects error:", err)
        setError(err.message || "Failed to load projects")
      } finally {
        setLoading(false)
      }
    }

    fetchProjects()

  }, [])

    const createProject = async (name: string) => {
      if (!name.trim()) return
    try {
    const newProject = await createProjectAPI(name)

    // 🔥 تحديث القائمة
    setProjects((prev) => [...prev, newProject])

    // 🔥 تحديد المشروع الجديد تلقائي
    setSelectedProject(newProject.id)

  } catch (err: any) {
    console.error("Create project error:", err)
    setError(err.message || "Failed to create project")
  }
}

  const deleteProject = async (id: number) => {

  try {

    await deleteProjectAPI(id)

    const remainingProjects = projects.filter(
      (project) => project.id !== id
    )

    setProjects(remainingProjects)

    // لو المشروع المحذوف هو المختار
    if (selectedProject === id) {

      if (remainingProjects.length > 0) {
        setSelectedProject(
          remainingProjects[0].id
        )
      } else {
        setSelectedProject(null)
      }
    }

    toast.success("Project Deleted 🗑")
  }catch (err: any) {

  console.error(
    "Delete project error:",
    err
  )

  toast.error(
    err.message === "Project has tasks"
      ? "Delete all tasks before deleting this project."
      : err.message || "Delete failed"
  )
}
  }
  return {
    projects,
    selectedProject,
    setSelectedProject,
    loading,
    error,
    createProject,
    deleteProject
  }
}