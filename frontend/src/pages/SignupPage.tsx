import { SignupForm } from "@/components/signup-form"
import type { SignupRequest } from "@/schemas/auth"
import { useAuth } from "@/hooks/useAuth"

function SignupPage() {
  const { signUpMutation } = useAuth()

  const handleSubmit = (data: SignupRequest) => {
    signUpMutation.mutate(data)
  }

  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <SignupForm
          submit={handleSubmit}
          loading={signUpMutation.isPending}
          error={signUpMutation.error?.message ?? null}
        />
      </div>
    </div>
  )
}

export { SignupPage }
