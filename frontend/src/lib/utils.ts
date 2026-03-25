import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const getTraceId = (): string =>
  typeof crypto !== "undefined"
    ? crypto.randomUUID()
    : Math.random().toString(36).slice(2)
