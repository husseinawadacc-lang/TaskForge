"use client"

type Task = {
  id: number
  title: string
  status: string
}

type Props = {
  task: Task
  onDelete: (id: number) => void
  onStatusChange: (id: number, status: string) => void
}

export default function TaskCard({ task, onDelete, onStatusChange }: Props) {
  return (
    <div className="bg-white p-4 rounded-2xl shadow hover:shadow-lg transition border border-gray-200">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold text-gray-800">{task.title}</h2>

        <span
          className={`text-xs px-3 py-1 rounded-full font-medium ${
            task.status === "Done"
              ? "bg-green-100 text-green-600"
              : "bg-yellow-100 text-yellow-600"

            }`}
            >
            {task.status}
            </span>
            </div>
            <div className="flex justify-between item-center">

        <select
          value={task.status}
          onChange={(e) =>
            onStatusChange(task.id, e.target.value)
          }
          className="text-sm border px-2 py-1 rounded-lg"
        >

          <option>Pending</option>
          <option>In Progress</option>
          <option>Done</option>
        </select>
        <button
          onClick={() => onDelete(task.id)}
          className="text-red-500  text-sm hover:underline"
        >
          Delete
        </button>

      <p className="text-sm mt-2">
        Status:

      </p>
    </div>
    </div>
  )}