export interface UserStats {
  followers: number
  following: number
  publicRepos: number
  accountCreatedAt: string
  bio: string | null
  location: string | null
  company: string | null
  website: string | null
  totalStars: number
  totalForks: number
  topLanguage: string | null
  mostStarredRepo: { name: string; stars: number } | null
}
