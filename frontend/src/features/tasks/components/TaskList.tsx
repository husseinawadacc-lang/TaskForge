"use client"

import TaskCard from "./TaskCard"

type Task = {
  id: number
  title: string
  status: string
}

type Props = {
  tasks: Task[]
  onDelete: (id: number) => void
  onStatusChange: (id: number, status: string) => void
}

export default function TaskList({ tasks=[], onDelete, onStatusChange }: Props) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.isArray(tasks) && tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onDelete={onDelete}
          onStatusChange={onStatusChange}
        />
      ))}
    </div>
  )
}