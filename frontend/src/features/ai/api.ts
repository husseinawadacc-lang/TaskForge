import { apiFetch } from "@/lib/api";
import {
    AnalyzeTaskRequest,
    AnalyzeTaskResponse,
    CreateTaskFromAIRequest,
    CreateTaskFromAIResponse,
    SuggestSubtasksRequest,
    SuggestSubtasksResponse,
} from "./types";

export const analyzeTaskAPI = async (
    data: AnalyzeTaskRequest
): Promise<AnalyzeTaskResponse> => {
    return apiFetch("/api/v1/ai/analyze-task", {
        method: "POST",
        body: JSON.stringify(data),
    });
};
export const createTaskFromAIAPI = async (
    text: string,
    projectId: number
) => {
    return apiFetch(
        `/api/v1/ai/create-task-from-ai?project_id=${projectId}`,
        {
            method: "POST",
            body: JSON.stringify({
                text,
            }),
        }
    );
};

export const suggestSubtasksAPI = async (title: string) => {
    return await apiFetch("/api/v1/ai/suggest-subtasks", {
        method: "POST",
        body: JSON.stringify({
            title,
        }),
    });
};