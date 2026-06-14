"use client"

import { useState, useEffect } from "react"
import toast from "react-hot-toast"
import { apiFetch } from "@/lib/api"

/*
🎯 نوع البيانات للـ UI
*/
export type Task = {
  id: number
  title: string
  status: string
}

export function useTasks(projectId: number | null) {

  // 🧠 state
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  /*
  🔄 تحويل backend → frontend
  */
  const mapTask = (task: any): Task => ({
    id: task.id,
    title: task.title,
    status: task.completed ? "Done" : "Pending",
  })

  /*
  🚀 تحميل tasks حسب المشروع
  */
  useEffect(() => {

    if (!projectId) {
      setTasks([])
      setLoading(false)
      return
    }

    const fetchTasks = async () => {
      try {
        setLoading(true)
        setError(null)

        // 🔥 apiFetch بيرجع data مباشرة
        const data = await apiFetch(
          `/api/v1/tasks?project_id=${projectId}`
        )
        console.log("API Response:", projectId, 
          JSON.stringify(data, null, 2)
        )

        const list = data.items || data.tasks || data

        if (Array.isArray(list)) {
          setTasks(list.map(mapTask))
        } else {
          setTasks([])
        }

      } catch (err: any) {
        console.error("Tasks error:", err)
        setError(err.message || "Failed to load tasks")
      } finally {
        setLoading(false)
      }
    }

    fetchTasks()

  }, [projectId])

  
  const addTask = async (title: string) => {

    if (!title.trim()) {
      toast.error("Title is required")
      return
    }

    if (!projectId) {
        toast.error("Select a project first")
              return
    }

    try {
      setError(null)
      const data = await apiFetch("/api/v1/tasks", {
        method: "POST",
        body: JSON.stringify({
          title,
          project_id: projectId, // 🔥 أهم تعديل
        }),
      })

      const newTask: Task = mapTask(data)

      setTasks(prev => [...prev, newTask])

      toast.success("Task Added ✅")

    } catch (err: any) {
      toast.error(err.message || "Failed to add task ❌")
    }
  }

  /*
  🗑 حذف Task
  */
const deleteTask = async (id: number) => {
  console.log("DELETE ID:", id)
  try {
    await apiFetch(`/api/v1/tasks/${id}`, {
      method: "DELETE",
    })
    console.log("DELETE SUCCESS:", id)
    setTasks(prev => {
      console.log("BEFORE:", prev)

      const updated = prev.filter(task => task.id !== id)

      console.log("AFTER:", updated)

      return updated
    })

    toast.success("Task Deleted 🗑")
  } catch (err: any) {
    toast.error(err.message || "Delete failed")
  }
}

  /*
  🔄 تغيير الحالة
  */
  const updateStatus = async (id: number, status: string) => {
    try {

      await apiFetch(`/api/v1/tasks/${id}`, {
        method: "PUT",
        body: JSON.stringify({
          completed: status === "Done",
        }),
      })

      setTasks(prev =>
        prev.map(task =>
          task.id === id ? { ...task, status } : task
        )
      )

      toast.success("Status Updated 🔄")
    } catch (err: any) {
      toast.error(err.message || "Update failed")
    }
  }

  /*
  🎯 return
  */
  return {
    tasks,
    addTask,
    deleteTask,
    updateStatus,
    loading,
    error,
  }
}