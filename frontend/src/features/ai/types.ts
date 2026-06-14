export interface AnalyzeTaskRequest {
    text: string;
}

export interface AnalyzeTaskResponse {
    title: string;
    description: string;
    priority: string;
}

export interface CreateTaskFromAIRequest {
    prompt: string;
}

export interface CreateTaskFromAIResponse {
    text: string;
    project_id: number;
}

export interface SuggestSubtasksRequest {
    title: string;
}

export interface SuggestSubtasksResponse {
    subtasks: string[];
}