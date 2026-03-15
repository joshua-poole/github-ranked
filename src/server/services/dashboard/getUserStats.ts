interface RepoStats {
  totalStars: number
  totalForks: number
  topLanguage: string | null
  mostStarredRepo: { name: string; stars: number } | null
}

interface ProfileStats {
  username: string
  followers: number
  following: number
  publicRepos: number
  accountCreatedAt: string
  bio: string | null
  location: string | null
  company: string | null
  website: string | null
}

interface CommitStats {
  totalCommits: number
}
export interface UserStats extends ProfileStats, RepoStats, CommitStats {}

const headers = {
  Accept: 'application/vnd.github+json',
  'User-Agent': 'github-ranked-app',
  ...(process.env.GITHUB_TOKEN && {
    Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
  }),
}

async function fetchProfileStats(username: string): Promise<ProfileStats> {
  const res = await fetch(`https://api.github.com/users/${username}`, {
    headers,
  })
  if (!res.ok) throw new Error(`Failed to fetch profile: ${res.status}`)
  const data = await res.json()
  return {
    username: username,
    followers: data.followers,
    following: data.following,
    publicRepos: data.public_repos,
    accountCreatedAt: data.created_at,
    bio: data.bio ?? null,
    location: data.location ?? null,
    company: data.company ?? null,
    website: data.blog ?? null,
  }
}

async function fetchRepoStats(username: string): Promise<RepoStats> {
  const res = await fetch(
    `https://api.github.com/users/${username}/repos?per_page=100&sort=pushed`,
    { headers },
  )
  if (!res.ok) throw new Error(`Failed to fetch repos: ${res.status}`)
  const repos = await res.json()

  const totalStars = repos.reduce(
    (sum: number, r: any) => sum + r.stargazers_count,
    0,
  )
  const totalForks = repos.reduce(
    (sum: number, r: any) => sum + r.forks_count,
    0,
  )

  const languageCounts = repos.reduce(
    (acc: Record<string, number>, r: any) => {
      if (r.language) acc[r.language] = (acc[r.language] ?? 0) + 1
      return acc
    },
    {} as Record<string, number>,
  )

  const topLanguage =
    (Object.entries(languageCounts) as [string, number][]).sort(
      (a, b) => b[1] - a[1],
    )[0]?.[0] ?? null

  const mostStarredRepo = repos.reduce(
    (best: any, r: any) =>
      r.stargazers_count > (best?.stargazers_count ?? -1) ? r : best,
    null,
  )

  return {
    totalStars,
    totalForks,
    topLanguage,
    mostStarredRepo: mostStarredRepo
      ? { name: mostStarredRepo.name, stars: mostStarredRepo.stargazers_count }
      : null,
  }
}

async function fetchCommitStats(username: string): Promise<CommitStats> {
  const res = await fetch(
    `https://api.github.com/search/commits?q=author:${username}`,
    {
      headers: {
        ...headers,
        Accept: 'application/vnd.github.cloak-preview+json',
      },
    },
  )
  if (!res.ok) throw new Error(`Failed to fetch commits: ${res.status}`)
  const data = await res.json()
  return {
    totalCommits: data.total_count,
  }
}


export async function getUserStats(username: string): Promise<UserStats> {
  const [profile, repos, commits] = await Promise.all([
    fetchProfileStats(username),
    fetchRepoStats(username),
    fetchCommitStats(username),
  ])
  return { ...profile, ...repos, ...commits}
}
