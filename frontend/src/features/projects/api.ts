import { apiFetch } from "@/lib/api"

export const createProjectAPI = async (name: string) => {
  return apiFetch("/api/v1/projects", {
    method: "POST",
    body: JSON.stringify({ name }),
  })
}

export const getProjects = async () => {
  const data = await apiFetch("/api/v1/projects")

  return data.items || data
}

export const getProjectAPI = async (id: number) => {
  return apiFetch(`/api/v1/projects/${id}`)
}

export const deleteProjectAPI = async (id: number) => {
  return apiFetch(`/api/v1/projects/${id}`, {
    method: "DELETE",
  })
}

export const getMembersAPI = async (
  projectId: number
) => {
  return apiFetch(
    `/api/v1/projects/${projectId}/members`
  )
}

export const addMemberAPI = async (
  projectId: number,
  userId: number,
) => {
  return apiFetch(
    `/api/v1/projects/${projectId}/members?user_id=${userId}`,
    {
      method: "POST",
    }
  )
}

export const removeMemberAPI = async (
  projectId: number,
  userId: number
) => {
  return apiFetch(
    `/api/v1/projects/${projectId}/members/${userId}`,
    {
      method: "DELETE",
    }
  )
}