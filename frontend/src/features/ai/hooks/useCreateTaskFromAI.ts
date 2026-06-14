import { useState } from "react";
import { createTaskFromAIAPI } from "../api";

export const useCreateTaskFromAI = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const createTask = async (text: string,projectId:number) => {
        try {
            setLoading(true);
            setError(null);

            return await createTaskFromAIAPI(
                text,
                projectId,
            );
        } catch (err: any) {
            setError(err.message || "Failed to create task");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return {
        createTask,
        loading,
        error,
    };
};