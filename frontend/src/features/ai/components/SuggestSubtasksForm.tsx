"use client";

import { useState } from "react";
import useSuggestSubtasks from "../hooks/useSuggestSubtasks";
import AISubTasksList from "./AISubtasksList";

export default function SuggestSubTasksForm() {
    const [title, setTitle] = useState("");

    const {
        generateSubtasks,
        subtasks,
        loading,
        error,
    } = useSuggestSubtasks();

    const handleSubmit = async (
        e: React.FormEvent
    ) => {
        e.preventDefault();

        if (!title.trim()) return;

        await generateSubtasks(title);
    };

    return (
        <div>
            <h2>Suggest Subtasks</h2>

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={title}
                    onChange={(e) =>
                        setTitle(e.target.value)
                    }
                    placeholder="Task title..."
                />

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading
                        ? "Generating..."
                        : "Generate"}
                </button>
            </form>

            {error && (
                <p>{error}</p>
            )}

            {subtasks.length > 0 && (
                <AISubTasksList
                    subtasks={subtasks}
                />
            )}
        </div>
    );
}