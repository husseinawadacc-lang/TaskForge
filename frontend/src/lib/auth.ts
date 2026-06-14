/*
🔥 تجديد access token باستخدام refresh token
*/
export const refreshAccessToken = async () => {

  // 🟢 1. نجيب refresh token
  const refresh = localStorage.getItem("refresh")

  // ❌ لو مش موجود
  if (!refresh) {
    throw new Error("SESSION EXPIRED")
  }

  try {

    // 🟢 2. نعمل request
    const res = await fetch("http://localhost:8001/api/v1/auth/refresh", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${refresh}`,
      },
      
    })

    // 🟢 3. نحول ل JSON
    const data = await res.json()

    /*
    🚨 لو فشل
    */
    if (!res.ok) {
      console.log("REFRESH ERROR:", data)

      throw new Error(
        data.detail || "Failed to refresh token"
      )
    }

    /*
    🔥 4. نحفظ access token الجديد
    */
    localStorage.setItem("token", data.access_token)

    /*
    🟡 (اختياري) لو الباك بيرجع refresh جديد
    */
    if (data.refresh_token) {
      localStorage.setItem("refresh", data.refresh_token)
    }

    /*
    ✅ 5. نرجع التوكن الجديد
    */
    return data.access_token

  } catch (error) {

    /*
    ❌ لو حصل أي error
    */
    console.error("REFRESH FAILED:", error)

    // 🧹 ننضف كل حاجة
    localStorage.removeItem("token")
    localStorage.removeItem("refresh")

    // 🔁 رجوع login
    

    throw new Error ("Session expired")
  }
}