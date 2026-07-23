import { createFileRoute } from '@tanstack/solid-router'

export const Route = createFileRoute('/purchases')({ component: Purchases })

function Purchases() {
  return (
    <>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-4 border-bottom">
        <h1 class="h3">Purchases</h1>
      </div>
      <p class="text-muted">Purchases dashboard content coming soon.</p>
    </>
  )
}
