import { createFileRoute } from '@tanstack/solid-router'

export const Route = createFileRoute('/company')({ component: Company })

function Company() {
  return (
    <>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-4 border-bottom">
        <h1 class="h3">Company Profile</h1>
      </div>
      <p class="text-muted">Company profile content coming soon.</p>
    </>
  )
}
