import type {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios"

import { getTraceId } from "@/lib/utils"

export const attachRequestInterceptor = (client: AxiosInstance) => {
  client.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      // Idempotency key for mutations
      if (["post", "put", "patch"].includes(config.method ?? "")) {
        config.headers["Idempotency-Key"] = getTraceId()
      }
      // Distributed tracing
      config.headers["X-Trace-Id"] = getTraceId()
      // Abort stale navigations via AbortController
      if (!config.signal) {
        const controller = new AbortController()
        config.signal = controller.signal
      }
      return config
    },
    (error: AxiosError) => Promise.reject(error)
  )
}
