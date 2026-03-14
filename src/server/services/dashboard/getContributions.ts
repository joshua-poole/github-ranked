export interface DayContributions {
  date: string
  count: number
}

const CONTRIBUTIONS_QUERY = `
  query($username: String!, $from: DateTime!, $to: DateTime!) {
    user(login: $username) {
      contributionsCollection(from: $from, to: $to) {
        contributionCalendar {
          weeks {
            contributionDays {
              date
              contributionCount
            }
          }
        }
      }
    }
  }
`

export async function getContributions(
  username: string,
): Promise<DayContributions[]> {
  const to = new Date()
  const from = new Date()
  from.setDate(to.getDate() - 90)

  const res = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'github-ranked-app',
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
    },
    body: JSON.stringify({
      query: CONTRIBUTIONS_QUERY,
      variables: {
        username,
        from: from.toISOString(),
        to: to.toISOString(),
      },
    }),
  })

  if (!res.ok) throw new Error(`GitHub GraphQL error: ${res.status}`)

  const json = await res.json()

  if (json.errors) {
    throw new Error(`GitHub GraphQL error: ${json.errors[0]?.message}`)
  }

  const weeks =
    json.data?.user?.contributionsCollection?.contributionCalendar?.weeks ?? []

  return weeks.flatMap((week: any) =>
    week.contributionDays.map((day: any) => ({
      date: day.date,
      count: day.contributionCount,
    })),
  )
}
