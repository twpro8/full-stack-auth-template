import type { AxiosError, AxiosInstance, AxiosResponse } from "axios"

import { handleTokenRefresh } from "@/lib/auth/refresh"
import { normaliseError } from "@/lib/errors"
import { retryAfterBackoff } from "@/lib/auth/retry"

export const attachResponseInterceptor = (
  client: AxiosInstance,
  onUnauthenticated: () => void
) => {
  client.interceptors.response.use(
    // Success: unwrap the envelope
    (res: AxiosResponse) => res.data,
    // Failure: route by status
    async (error: AxiosError) => {
      const status = error.response?.status
      if (status === 401)
        return handleTokenRefresh(error, client, onUnauthenticated)
      if (status === 403) {
        window.location.replace("/403")
        return Promise.reject(normaliseError(error)) // ← добавь return
      }
      if (status === 429) return retryAfterBackoff(error, client)
      return Promise.reject(normaliseError(error))
    }
  )
}
