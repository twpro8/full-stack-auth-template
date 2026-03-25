import axios, { type AxiosInstance } from "axios"

import { attachRequestInterceptor } from "@/lib/interceptors/request"
import { attachResponseInterceptor } from "@/lib/interceptors/response"
import { router } from "@/app/router"

export const createApiClient = (
  onUnauthenticated: () => void
): AxiosInstance => {
  const client = axios.create({
    baseURL: `${import.meta.env.VITE_API_BASE_URL}/api/v1`,
    timeout: 10_000, // 10 s global timeout
    withCredentials: true, // send HTTP-only cookies
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-Client-Version": import.meta.env.VITE_APP_VERSION,
    },
  })

  attachRequestInterceptor(client)
  attachResponseInterceptor(client, onUnauthenticated)

  return client
}

// Singleton — import this everywhere
export const apiClient = createApiClient(() => {
  router.navigate({ to: "/login" })
})
