import { createFileRoute } from '@tanstack/react-router'
import { Button } from '#/components/ui/button'
import { Input } from '#/components/ui/input'
import Compare from '#/components/Compare'
import { useState } from 'react'

export const Route = createFileRoute('/compare/')({
  component: RouteComponent,
})

function RouteComponent() { 

    const [showCompare, setShowCompare] = useState(false)
    


    return (
        <main className="flex flex-col items-center gap-4 page-wrap py-12">
            <h1>Side-by-Side Comparison of two users </h1>
            <div className="flex flex-row gap-4 ">
                <Input /> 
                    vs 
                <Input />
            </div>
            <Button onClick={() => setShowCompare(true)}>Compare</Button>
            {showCompare && <Compare />}
        </main>
    )
}

