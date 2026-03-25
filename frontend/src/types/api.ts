import type { InternalAxiosRequestConfig } from "axios"

import { ApiError } from "@/lib/errors.ts"

/** Generic paginated list response */
export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

/** Standard error body from the API */
export interface ErrorBody {
  code: string
  message: string
  details?: unknown
}

/** Extends AxiosRequestConfig with retry metadata */
export interface RetryConfig extends InternalAxiosRequestConfig {
  _retryCount?: number
}

/** Type guard to narrow unknown → ApiError */
export const isApiError = (e: unknown): e is ApiError => e instanceof ApiError

/** Typed abort-controller helper */
export const createAbortable = <T>(fn: (signal: AbortSignal) => Promise<T>) => {
  const controller = new AbortController()
  return {
    promise: fn(controller.signal),
    abort: () => controller.abort(),
  }
}

declare module "axios" {
  interface AxiosInstance {
    get<T = unknown>(url: string, config?: AxiosRequestConfig): Promise<T>

    post<T = unknown>(
      url: string,
      data?: unknown,
      config?: AxiosRequestConfig
    ): Promise<T>

    put<T = unknown>(
      url: string,
      data?: unknown,
      config?: AxiosRequestConfig
    ): Promise<T>

    patch<T = unknown>(
      url: string,
      data?: unknown,
      config?: AxiosRequestConfig
    ): Promise<T>

    delete<T = unknown>(url: string, config?: AxiosRequestConfig): Promise<T>
  }
}
