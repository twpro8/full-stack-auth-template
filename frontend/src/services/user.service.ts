import { apiClient } from "@/lib/client"
import type { UserPublic } from "@/types/user"

const userService = {
  getMe: () => apiClient.get<UserPublic>("/users/me"),
}

export { userService }
