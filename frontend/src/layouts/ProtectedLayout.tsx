import { Outlet } from "@tanstack/react-router"

const ProtectedLayout = () => {
  // TODO: check if the user is logged in
  console.log("Protected Layout")
  return <Outlet />
}

export { ProtectedLayout }
