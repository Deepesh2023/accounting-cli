import { createFileRoute } from '@tanstack/solid-router'

export const Route = createFileRoute('/financial-statements')({
  component: FinancialStatements,
})

function FinancialStatements() {
  return (
    <>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-4 border-bottom">
        <h1 class="h3">Financial Statements</h1>
      </div>
      <p class="text-muted">Financial statements content coming soon.</p>
    </>
  )
}
