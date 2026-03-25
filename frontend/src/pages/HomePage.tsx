import dayjs from "dayjs"
import { useAuth } from "@/hooks/useAuth"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldLabel, FieldSeparator } from "@/components/ui/field"

const HomePage = () => {
  const { user, logoutMutation } = useAuth()
  return (
    <div className="flex min-h-svh w-full flex-col items-center justify-center gap-3 p-6 md:p-10">
      <div>Welcome to my website!👋</div>
      <Card className="w-full max-w-xs">
        <CardHeader>
          <CardTitle>User Info</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          <Field className="flex flex-row justify-between">
            <FieldLabel>ID:</FieldLabel>
            <span className="flex justify-end">{user?.id}</span>
          </Field>
          <Field className="flex flex-row justify-between">
            <FieldLabel>Full Name:</FieldLabel>
            <span className="flex justify-end">{user?.full_name}</span>
          </Field>
          <Field className="flex flex-row justify-between">
            <FieldLabel>Email:</FieldLabel>
            <span className="flex justify-end">{user?.email}</span>
          </Field>
          <Field className="flex flex-row justify-between">
            <FieldLabel>Registered:</FieldLabel>
            <span className="flex justify-end">
              {user?.created_at
                ? dayjs(user.created_at).format("D MMMM YYYY")
                : "—"}
            </span>
          </Field>
          <FieldSeparator />
          <Field>
            <Button
              variant="destructive"
              size="sm"
              className="w-full"
              onClick={() => {
                logoutMutation.mutate()
              }}
            >
              Logout
            </Button>
          </Field>
        </CardContent>
      </Card>
    </div>
  )
}

export { HomePage }
