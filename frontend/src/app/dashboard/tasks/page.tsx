"use client"

import TaskList from "@/features/tasks/components/TaskList"
import TaskModal from "@/features/tasks/components/TaskModal"
import { useProjects } from "@/features/projects/hooks/useProjects"
import { useTasks } from "@/features/tasks/hooks/useTasks"
import { useState, useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"

export default function TasksPage() {

  /*
  🧠 جايب كل logic من hook
  - tasks → البيانات
  - addTask → إضافة
  - deleteTask → حذف
  - updateStatus → تغيير الحالة
  - loading / error → حالات UI
  */
  const { projects, selectedProject,
    setSelectedProject } = useProjects()
  const searchParams = useSearchParams()
  useEffect(() => {
    const projectFromURL = searchParams.get("project")
    if (
      projectFromURL && (Number(projectFromURL))
    !== selectedProject
    ) {
      setSelectedProject(Number(projectFromURL))
    }
  }, [searchParams, selectedProject,
     setSelectedProject])
  const { 
    tasks, addTask, deleteTask,
     updateStatus, loading,
      error } = useTasks(selectedProject)

  // لو في projectId في URL، نحدده كـ selectedProject
  /*
  🟢 UI State (خاصة بالواجهة فقط)
  */
  const [title, setTitle] = useState("")        // input
  const [isOpen, setIsOpen] = useState(false)   // modal
  const [isSaving, setIsSaving] = useState(false)

  /*
  🎯 Filter + Search State
  */
  const [filter, setFilter] = useState("All")
  const [search, setSearch] = useState("")

  /*
  🚀 فلترة البيانات (UI logic)
  - filter حسب الحالة
  - search حسب العنوان
  */
  const filteredTasks = tasks.filter(task => {

    // ✅ فلترة الحالة
    const matchFilter =
      filter === "All" || task.status === filter

    // ✅ فلترة البحث
    const matchSearch =
      task.title.toLowerCase().includes(search.toLowerCase())

    return matchFilter && matchSearch
  })

  /*
  ➕ إضافة task
  */
  const handleSave = async () => {

    // ❗ validation
    if (!title.trim()) return

    setIsSaving(true)

    try {
      await addTask(title)   // API call من hook

      setTitle("")           // reset input
      setIsOpen(false)       // قفل modal

    } finally {
      setIsSaving(false)     // دايمًا يرجع false
    }
  }

console.log ("TASKS:" ,tasks)
console.log ("FILTERED TASKS:" ,filteredTasks)

  /*
  ⏳ Loading UI
  */
  if (loading) {
    return (
      <div className="space-y-4 animate-pulse p-6">
        <div className="h-12 bg-gray-200 rounded"></div>
        <div className="h-12 bg-gray-200 rounded"></div>
        <div className="h-12 bg-gray-200 rounded"></div>
      </div>
    )
  }

  /*
  ❌ Error UI
  */
  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-red-500 text-lg">{error}</p>
      </div>
    )
  }


  return (
    <>
      <div className="p-6">

        {/* 🔥 HEADER */}
        <div className="flex justify-between items-center mb-6">

          <div>
            <h1 className="text-3xl font-bold text-gray-800">
              My Tasks
            </h1>
            <p className="text-gray-500 text-sm">
              Manage your work efficiently 🚀
            </p>
          </div>

          <button
        disabled={!selectedProject}
        onClick={() => setIsOpen(true)}
        className={`px-4 py-2 rounded-lg text-white transition ${
          selectedProject
            ? "bg-indigo-500 hover:bg-indigo-600"
            : "bg-gray-400 cursor-not-allowed"
        }`}
      >
        + Add Task
      </button>
        </div>


        {/* 🔍 SEARCH */}
        <input
          type="text"
          placeholder="Search tasks..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border px-3 py-2 rounded-lg w-full mb-4"
        />


        {/* 🎯 FILTER */}
        <div className="flex gap-2 mb-6">
          {["All", "Pending", "Done"].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-1 rounded-full text-sm transition ${
                filter === f
                  ? "bg-indigo-500 text-white"
                  : "bg-gray-200 hover:bg-gray-300"
              }`}
            >
              {f}
            </button>
          ))}
        </div>


        {/* 📊 STATS */}
        <div className="grid grid-cols-3 gap-4 mb-6">

          <div className="bg-white p-4 rounded-xl shadow">
            <p className="text-sm text-gray-500">Total</p>
            <h2 className="text-xl font-bold">{tasks.length}</h2>
          </div>

          <div className="bg-white p-4 rounded-xl shadow">
            <p className="text-sm text-gray-500">Pending</p>
            <h2 className="text-xl font-bold">
              {tasks.filter(t => t.status === "Pending").length}
            </h2>
          </div>

          <div className="bg-white p-4 rounded-xl shadow">
            <p className="text-sm text-gray-500">Done</p>
            <h2 className="text-xl font-bold">
              {tasks.filter(t => t.status === "Done").length}
            </h2>
          </div>

        </div>
        {/* 🧾 project selector */}

          <select
          value={selectedProject || ""}
          onChange={(e) => setSelectedProject(
            e.target.value ? Number(e.target.value) : null
          )}
          className="mb-4 p-2 border rounded shadow-sm"
          >
          <option value="">Select project</option>


          {projects.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>

        {/* 🧾 TASK LIST */}
        {!selectedProject ? (

        <div className="text-center mt-20 text-gray-500">
          <p className="text-lg">
            Select a project first 📁
          </p>
        </div>

      ) : filteredTasks.length === 0 ? (

        <div className="text-center mt-20 text-gray-500">
          <p className="text-lg mb-2">
            No tasks found 😢
          </p>

          <p className="text-sm">
           Start by adding a new task for this project!
          </p>
        </div>

      ) : (
        
          <TaskList
            tasks={filteredTasks}
            onDelete={deleteTask}
            onStatusChange={updateStatus}
          />

        )}

      </div>


      {/* 🔥 MODAL */}
      <TaskModal
        isOpen={isOpen}
        title={title}
        setTitle={setTitle}
        onClose={() => setIsOpen(false)}
        onSave={handleSave}
        
      />
    </>
  )
}