export async function getUserIcon(username: string): Promise<string> {
  const res = await fetch(`https://api.github.com/users/${username}`, {
    headers: {
      Accept: 'application/vnd.github+json',
      'User-Agent': 'github-ranked-app',
      ...(process.env.GITHUB_TOKEN && {
        Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
      }),
    },
  })

  if (!res.ok) {
    throw new Error(`Failed to fetch GitHub user: ${res.status}`)
  }

  const user = await res.json()
  return user.avatar_url as string
}
