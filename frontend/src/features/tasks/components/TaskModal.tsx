"use client"

type Props = {
  isOpen: boolean
  title: string
  setTitle: (value: string) => void
  onClose: () => void
  onSave: () => void
}

export default function TaskModal({
  isOpen,
  title,
  setTitle,
  onClose,
  onSave,
}: Props) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-xl w-96">
        <h2 className="text-lg font-semibold mb-4">Add Task</h2>

        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border p-2 rounded mb-4"
        />

        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-300 rounded"
          >
            Cancel
          </button>

          <button
            onClick={onSave}
            className="px-4 py-2 bg-indigo-500 text-white rounded"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  )
}