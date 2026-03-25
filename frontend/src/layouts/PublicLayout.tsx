import { Navigate, Outlet } from "@tanstack/react-router"
import { useAuth } from "@/hooks/useAuth"
import { ROUTES } from "@/app/routes"

const PublicLayout = () => {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) return null
  if (isAuthenticated) return <Navigate to={ROUTES.DASHBOARD} />

  return <Outlet />
}

export { PublicLayout }
