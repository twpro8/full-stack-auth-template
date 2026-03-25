import type { AxiosError, AxiosInstance } from "axios"

import type { RetryConfig } from "@/types/api"

const MAX_RETRIES = 3
const BASE_DELAY = 1000

export const retryAfterBackoff = (error: AxiosError, client: AxiosInstance) => {
  const config = error.config as RetryConfig
  config._retryCount = (config._retryCount ?? 0) + 1

  if (config._retryCount > MAX_RETRIES) {
    return Promise.reject(error)
  }

  // Respect Retry-After header if present
  const retryAfter = error.response?.headers["retry-after"]
  const delay = retryAfter
    ? Number(retryAfter) * 1000
    : BASE_DELAY * 2 ** (config._retryCount - 1) // exponential

  return new Promise((resolve) =>
    setTimeout(() => resolve(client(config)), delay)
  )
}
