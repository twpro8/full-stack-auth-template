import type { AxiosError } from "axios"

import type { ErrorBody } from "@/types/api"

export class ApiError extends Error {
  readonly status: number
  readonly code: string
  readonly details?: unknown

  constructor(
    status: number,
    code: string,
    message: string,
    details?: unknown
  ) {
    super(message)
    this.name = "ApiError"
    this.status = status
    this.code = code
    this.details = details
  }
}

export const normaliseError = (error: AxiosError): ApiError => {
  if (!error.response) {
    // Network error / timeout
    return new ApiError(0, "NETWORK_ERROR", "Network unreachable")
  }
  const { status, data } = error.response
  const body = data as ErrorBody
  return new ApiError(
    status,
    body?.code ?? `HTTP_${status}`,
    body?.message ?? error.message,
    body?.details
  )
}
