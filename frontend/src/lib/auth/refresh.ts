import type { AxiosError, AxiosInstance } from "axios"

import { addToQueue, processQueue } from "./queue"

let isRefreshing = false

export const handleTokenRefresh = (
  error: AxiosError,
  client: AxiosInstance,
  onUnauthenticated: () => void
): Promise<unknown> => {
  const original = error.config!

  // Prevent infinite loop: refresh endpoint itself returned 401
  if (original.url?.includes("/auth/refresh")) {
    onUnauthenticated()
    return Promise.reject(error)
  }

  if (isRefreshing) {
    // Queue callers while refresh is in-flight
    return new Promise((resolve, reject) => {
      addToQueue({ resolve, reject })
    }).then(() => client(original))
  }

  isRefreshing = true

  return client
    .post("/auth/refresh")
    .then(() => {
      processQueue(null) // resume queued requests
      return client(original) // retry the original
    })
    .catch((err) => {
      processQueue(err) // reject all queued
      onUnauthenticated()
      return Promise.reject(err)
    })
    .finally(() => {
      isRefreshing = false
    })
}
