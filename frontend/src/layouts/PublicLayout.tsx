import { Outlet } from "@tanstack/react-router"

const PublicLayout = () => {
  // TODO: check if the user is logged in
  console.log("Public Layout")
  return <Outlet />
}

export { PublicLayout }
