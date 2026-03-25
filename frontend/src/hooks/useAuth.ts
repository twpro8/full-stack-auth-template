import { useNavigate } from "@tanstack/react-router"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { authService } from "@/services/auth.service"
import type { LoginRequest, SignupRequest } from "@/schemas/auth"
import { userService } from "@/services/user.service"

const useAuth = () => {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: user, isLoading } = useQuery({
    queryKey: ["users", "me"],
    queryFn: () => userService.getMe().catch(() => null),
    retry: false,
    staleTime: 5 * 60_000,
  })

  const isAuthenticated = !!user

  const loginMutation = useMutation({
    mutationFn: (data: LoginRequest) => authService.login(data),
    onSuccess: (user) => {
      queryClient.setQueryData(["users", "me"], user)
      navigate({ to: "/dashboard" })
    },
  })

  const signUpMutation = useMutation({
    mutationFn: (data: SignupRequest) => authService.signup(data),
    onSuccess: () => navigate({ to: "/login" }),
  })

  const logoutMutation = useMutation({
    mutationFn: () => authService.logout(),
    onSuccess: () => {
      queryClient.clear()
      navigate({ to: "/login" })
    },
  })

  return {
    user,
    loginMutation,
    signUpMutation,
    logoutMutation,
    isLoading,
    isAuthenticated,
  }
}

export { useAuth }
