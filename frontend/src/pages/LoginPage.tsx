import type { LoginRequest } from "@/schemas/auth.ts"
import { LoginForm } from "@/components/login-form.tsx"
import { useState } from "react"

const LoginPage = () => {
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(false)

  const handleSubmit = async (data: LoginRequest) => {
    try {
      // TODO: login, catch and set errors
      console.log(data)
    } finally {
      // suppress eslint error
      setError(null)
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <LoginForm submit={handleSubmit} loading={loading} error={error} />
      </div>
    </div>
  )
}

export default LoginPage
