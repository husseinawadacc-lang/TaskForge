import { refreshAccessToken } from "./auth"

/*
🔥 دي الدالة الأساسية لكل API calls في المشروع
*/
export const apiFetch = async (url: string, options: any = {}) => {

  // 🟢 1. نجيب التوكن من localStorage
  let token = localStorage.getItem("token")

  // 🟢 2. نعمل request
  let res = await fetch(`http://localhost:8001${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json", // مهم لأي POST
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  })

  /*
  🚨 3. لو التوكن انتهى (401)
  */
  if (res.status === 401) {

  try {

    token = await refreshAccessToken()

    res = await fetch(
      `http://localhost:8001${url}`,
      {
        ...options,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          ...options.headers,
        },
      }
    )

  } catch (err) {

    if (
      err instanceof Error &&
      err.message === "SESSION_EXPIRED"
    ) {

      localStorage.removeItem("token")
      localStorage.removeItem("refresh")

      window.location.href = "/login"
    }

    throw err
  }
}

/*
🟢 4. نحول response إلى JSON إذا وجد
*/
let data = null
if (res.status !== 204) { // 204 No Content
  const text = await res.text()
  if (text) {
  data = JSON.parse(text)}}
/*
🚨 5. error handling موحد
*/
if (!res.ok) {
  console.log("API ERROR:", data)
  throw new Error(
    data?.detail?.[0]?.msg ||
    data?.detail ||
    "Request failed")}
/*
✅ 6. نرجع data مباشرة
*/
return data}