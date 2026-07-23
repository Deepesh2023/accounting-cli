import { createFileRoute } from '@tanstack/solid-router'

export const Route = createFileRoute('/outstanding')({ component: Outstanding })

function Outstanding() {
  return (
    <>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-4 border-bottom">
        <h1 class="h3">Outstanding Report</h1>
      </div>
      <p class="text-muted">Outstanding report content coming soon.</p>
    </>
  )
}
