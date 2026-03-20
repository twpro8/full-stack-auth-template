import { createBrowserRouter } from "react-router-dom"

import { ROUTES } from "@/app/routes"
import { RootLayout } from "@/layouts/RootLayout"
import { PublicLayout } from "@/layouts/PublicLayout"
import { ProtectedLayout } from "@/layouts/ProtectedLayout"
import { HomePage } from "@/pages/HomePage"
import { LoginPage } from "@/pages/LoginPage"
import { SignupPage } from "@/pages/SignupPage.tsx"

export const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      {
        element: <ProtectedLayout />,
        children: [
          {
            path: ROUTES.DASHBOARD,
            element: <HomePage />,
          },
        ],
      },
      {
        element: <PublicLayout />,
        children: [
          {
            path: ROUTES.LOGIN,
            element: <LoginPage />,
          },
          {
            path: ROUTES.SIGNUP,
            element: <SignupPage />,
          },
        ],
      },
    ],
  },
])
