import { Navigate, Outlet } from "@tanstack/react-router"
import { useAuth } from "@/hooks/useAuth"
import { ROUTES } from "@/app/routes"

const ProtectedLayout = () => {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) return null
  if (!isAuthenticated) return <Navigate to={ROUTES.LOGIN} />

  return <Outlet />
}

export { ProtectedLayout }
