import { useState } from "react"

import { SignupForm } from "@/components/signup-form"
import type { SignupRequest } from "@/schemas/auth"

function SignupPage() {
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(false)

  const handleSubmit = async (data: SignupRequest): Promise<void> => {
    setLoading(true)
    try {
      console.log(data)
    } finally {
      // TODO:  sign up, catch and set errors
      setError(null)
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <SignupForm submit={handleSubmit} error={error} loading={loading} />
      </div>
    </div>
  )
}

export { SignupPage }
