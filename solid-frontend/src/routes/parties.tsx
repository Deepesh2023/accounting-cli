import { createFileRoute } from '@tanstack/solid-router'

export const Route = createFileRoute('/parties')({ component: Parties })

function Parties() {
  return (
    <>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-4 border-bottom">
        <h1 class="h3">Parties</h1>
      </div>
      <p class="text-muted">Parties content coming soon.</p>
    </>
  )
}
