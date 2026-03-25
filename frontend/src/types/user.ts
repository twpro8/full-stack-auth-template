interface UserPublic {
  id: number
  full_name: string
  email: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
}

export type { UserPublic }
