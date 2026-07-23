import { createFileRoute } from '@tanstack/solid-router'

export const Route = createFileRoute('/transactions')({ component: Transactions })

function Transactions() {
  return (
    <>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-4 border-bottom">
        <h1 class="h3">Transaction History</h1>
      </div>
      <p class="text-muted">Transaction history content coming soon.</p>
    </>
  )
}
