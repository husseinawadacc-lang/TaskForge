import { useState } from "react";
import { suggestSubtasksAPI } from "../api";

const useSuggestSubtasks = () => {
    const [loading, setLoading] = useState(false);
    const [subtasks, setSubtasks] = useState<string[]>([]);
    const [error, setError] = useState<string | null>(null);

    const generateSubtasks = async (title: string) => {
        try {
            setLoading(true);
            setError(null);

            const result = await suggestSubtasksAPI(title);

            setSubtasks(result.subtasks);

            return result;
        } catch (err: any) {
            setError(
                err.message || "Failed to generate subtasks"
            );
        } finally {
            setLoading(false);
        }
    };

    return {
        generateSubtasks,
        subtasks,
        loading,
        error,
    };
};

export default useSuggestSubtasks;