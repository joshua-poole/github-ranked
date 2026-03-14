import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/about/')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    
    
    <main className="page-wrap px-4 py-12">
      <section className="island-shell rounded-2xl p-6 sm:p-8">
        <p className="island-kicker mb-2">About</p>
        <h1 className="display-title mb-3 text-4xl font-bold text-(--sea-ink) sm:text-5xl">
          Make coding feel like a game
        </h1>
        <p className="island-description text-lg text-[#a8b1bb]">
          GitRank turns your GitHub activity into a global ranking. 
          We built it to make coding more engaging — especially for developers just starting out. 
          Every commit, every repo, every contribution adds to your score and puts you on the board alongside 
          developers from around the world.
          Coding in isolation gets old fast. 
          GitRank gives your work visibility. 
          It rewards consistency, 
          encourages you to build in public, 
          and creates the kind of friendly competition that actually makes you better. 
          Whether you're a student pushing your first project 
          or a developer with years of commits behind you, 
          there's a place for everyone on the leaderboard.
        </p>
      </section>
      <section className="island-shell rounded-2xl p-6 sm:p-8 mt-8">
        todo: get real stats
        <div className="w-full grid grid-cols-3 gap-4 items-stretch">
          {[
            { value: '1,200+', label: 'Tracked Coders' },
            { value: '4.2M',   label: 'Commits Analysed' },
            { value: '190+',   label: 'Countries' },
          ].map(stat => (
            <div key={stat.label} className="bg-[#0d1117] border border-[#21262d] rounded-xl p-6 text-center">
              <div className="text-2xl font-bold text-teal-400 mb-1">{stat.value}</div>
              <div className="text-xs text-[#8b949e] uppercase tracking-wider">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>  
    </main>
    
  )
}
