import type { LoginRequest, SignupRequest } from "@/schemas/auth"
import { apiClient } from "@/lib/client"
import type { UserPublic } from "@/types/user"

const authService = {
  login: (data: LoginRequest) =>
    apiClient.post<UserPublic>("/auth/login", data),
  signup: (data: SignupRequest) => apiClient.post("/auth/register", data),
  logout: () => apiClient.post("/auth/logout"),
}

export { authService }
