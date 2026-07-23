import { createFileRoute } from '@tanstack/solid-router'

export const Route = createFileRoute('/stock')({ component: Stock })

function Stock() {
  return (
    <>
      <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-4 border-bottom">
        <h1 class="h3">Stock Inventory</h1>
      </div>
      <p class="text-muted">Stock inventory content coming soon.</p>
    </>
  )
}
