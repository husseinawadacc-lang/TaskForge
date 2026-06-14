import AnalyzeTaskForm from "@/features/ai/components/AnalyzeTaskForm"

import CreateTaskFromAIForm from "@/features/ai/components/CreateTaskFromAIForm";

import SuggestSubTasksForm from "@/features/ai/components/SuggestSubtasksForm";


export default function AIPage() {
  return (
    <>
    <AnalyzeTaskForm/> 
    <CreateTaskFromAIForm/>
    <SuggestSubTasksForm/>
    </>
  );
}