import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/about/')({
  component: RouteComponent,
})

function RouteComponent() {
  return (
    
    
    <main className="page-wrap px-4 py-12">
      <section className="island-shell rounded-2xl p-6 sm:p-8">
        <p className="island-kicker mb-2">About</p>
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
