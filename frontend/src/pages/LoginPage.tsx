import type { LoginRequest } from "@/schemas/auth"
import { LoginForm } from "@/components/login-form"
import { useAuth } from "@/hooks/useAuth"

const LoginPage = () => {
  const { loginMutation } = useAuth()

  const handleSubmit = (data: LoginRequest) => {
    loginMutation.mutate(data)
  }

  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <LoginForm
          submit={handleSubmit}
          loading={loginMutation.isPending}
          error={loginMutation.error?.message ?? null}
        />
      </div>
    </div>
  )
}

export { LoginPage }
