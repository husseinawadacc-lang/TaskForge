import { useState } from "react";
import { analyzeTaskAPI } from "../api";
import { AnalyzeTaskResponse } from "../types";

export const useAnalyzeTask = () => {
    const [loading, setLoading] = useState(false);
    const [analysis, setAnalysis] = useState<AnalyzeTaskResponse | null>(null);
    
    const [error, setError] = useState<string | null>(null);

    const analyzeTask = async (taskDescription: string) => {
        try {
            setLoading(true);
            setError(null);

            const result = await analyzeTaskAPI({
                text: taskDescription,
            });

            setAnalysis(result);

            return result;
        } catch (err: any) {
            setError(err.message || "Failed to analyze task");
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return {
        analyzeTask,
        analysis,
        loading,
        error,
    };
};