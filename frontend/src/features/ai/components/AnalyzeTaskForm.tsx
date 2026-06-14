"use client";

import { FormEvent, useState } from "react";
import { useAnalyzeTask } from "../hooks/useAnalyzeTask";

export default function AnalyzeTaskForm() {
    const [taskDescription, setTaskDescription] = useState("");

    const {
        analyzeTask,
        analysis,
        loading,
        error,
    } = useAnalyzeTask();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();

        if (!taskDescription.trim()) return;

        await analyzeTask(taskDescription);
    };

    return (
        <div className="space-y-4 rounded-lg border p-6">
            <h2 className="text-xl font-semibold">
                Analyze Task
            </h2>

            <form
                onSubmit={handleSubmit}
                className="space-y-4"
            >
                <textarea
                    value={taskDescription}
                    onChange={(e) =>
                        setTaskDescription(e.target.value)
                    }
                    placeholder="Describe your task..."
                    className="w-full rounded border p-3"
                    rows={4}
                />

                <button
                    type="submit"
                    disabled={loading}
                    className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
                >
                    {loading
                        ? "Analyzing..."
                        : "Analyze"}
                </button>
            </form>

            {error && (
                <p className="text-red-500">
                    {error}
                </p>
            )}

            {analysis && (
                <div className="rounded bg-gray-100 p-4">
                    <h3 className="font-medium">
                        Analysis
                    </h3>

                {analysis && (
                    <div>
                        <p>Title: {analysis.title}</p>
                        <p>Description: {analysis.description}</p>
                        <p>Priority: {analysis.priority}</p>
                    </div>
                )}           
                     </div>
            )}
        </div>
    );
}