"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useCreateTaskFromAI } from "../hooks/useCreateTaskFromAI";

export default function CreateTaskFromAIForm() {
    const [text, setText] = useState("");
    const [projectId, setProjectId] = useState("");

    const router = useRouter();

    const {
        createTask,
        loading,
    } = useCreateTaskFromAI();

    const handleSubmit = async (
        e: React.FormEvent<HTMLFormElement>
    ) => {
        e.preventDefault();

        if (
            text.trim().length < 3 ||
            !projectId
        ) {
            return;
        }

        try {
            await createTask(
                text,
                Number(projectId)
            );

            setText("");

            router.push(
                `/dashboard/tasks?project=${projectId}`
            );

        } catch (error) {
            console.error(
                "Failed to create task:",
                error
            );
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-4"
        >
            <textarea
                value={text}
                onChange={(e) =>
                    setText(e.target.value)
                }
                placeholder="Describe the task..."
                rows={4}
                className="
                    w-full
                    border
                    rounded
                    p-3
                "
            />

            <input
                type="number"
                value={projectId}
                onChange={(e) =>
                    setProjectId(
                        e.target.value
                    )
                }
                placeholder="Project ID"
                className="
                    border
                    rounded
                    p-2
                "
            />

            <button
                type="submit"
                disabled={
                    loading ||
                    text.trim().length < 3
                }
                className="
                    px-4
                    py-2
                    bg-blue-600
                    text-white
                    rounded
                "
            >
                {loading
                    ? "Creating..."
                    : "Create Task"}
            </button>
        </form>
    );
}