import { For, Show, createSignal, createMemo } from 'solid-js'
import { createFileRoute, Link } from '@tanstack/solid-router'
import { formatMoney } from '../lib/store'
import { useSales, useDeleteSale } from '../lib/api/useSales'

export const Route = createFileRoute('/sales')({ component: Sales })

type Filters = {
  month: string
  from: string
  to: string
}

function Sales() {
  const [filters, setFilters] = createSignal<Filters>({
    month: '',
    from: '',
    to: '',
  })

  const salesQuery = useSales()
  const deleteSale = useDeleteSale()

  const filteredSales = createMemo(() => {
    let sales = [...(salesQuery.data ?? [])]
    const f = filters()
    if (f.month) sales = sales.filter((s) => s.date.startsWith(f.month))
    if (f.from) sales = sales.filter((s) => s.date >= f.from)
    if (f.to) sales = sales.filter((s) => s.date <= f.to)
    return sales
  })

  const totalSales = createMemo(() =>
    filteredSales().reduce((sum, s) => sum + Number(s.grand_total), 0),
  )

  function fmtId(id: string) {
    return 'INV-' + id.replace(/-/g, '').slice(0, 4).toUpperCase()
  }

  function custName(sale: NonNullable<typeof salesQuery.data>[number]) {
    return sale.party_id ? sale.party_id.slice(0, 8) : 'Walk-in'
  }

  return (
    <div class="space-y-6">
      <div class="flex items-stretch mt-4">
        <div class="w-1/3">
          <div class="bg-[#0d6efd] text-white border-0 shadow-md rounded-xl h-full">
            <div class="p-4">
              <p class="opacity-75 uppercase font-bold tracking-widest text-[0.8em]">
                Total Sales (All Time)
              </p>
              <h2 class="mb-0 font-bold mt-2 text-2xl">
                ₹{formatMoney(totalSales())}
              </h2>
            </div>
          </div>
        </div>
        <div class="w-2/3 flex justify-end items-center">
          <Link
            to="/record-sale"
            search={{ edit: undefined }}
            class="inline-block bg-[#0d6efd] text-white text-lg px-4 py-2.5 rounded-lg shadow font-bold hover:bg-[#0b5ed7] cursor-pointer"
          >
            + Record Sales
          </Link>
        </div>
      </div>

      <div class="border-0 shadow-sm rounded-lg overflow-hidden">
        <div class="bg-white pt-4 pb-3 px-4">
          <div class="flex justify-between items-center mb-3">
            <h5 class="mb-0 font-bold text-gray-600">Recent Sales History</h5>
          </div>

          <div class="grid grid-cols-12 gap-2 items-end bg-gray-100 p-3 rounded-lg mb-2">
            <div class="col-span-3">
              <label class="block text-gray-500 text-xs mb-1">Month</label>
              <input
                type="month"
                class="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                value={filters().month}
                onInput={(e) => setFilters({ ...filters(), month: e.currentTarget.value })}
              />
            </div>
            <div class="col-span-4">
              <label class="block text-gray-500 text-xs mb-1">Date Range</label>
              <div class="flex gap-2">
                <input
                  type="date"
                  class="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                  value={filters().from}
                  onInput={(e) => setFilters({ ...filters(), from: e.currentTarget.value })}
                />
                <input
                  type="date"
                  class="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                  value={filters().to}
                  onInput={(e) => setFilters({ ...filters(), to: e.currentTarget.value })}
                />
              </div>
            </div>
            <div class="col-span-5 flex gap-2">
              <button
                class="w-full bg-[#0d6efd] text-white text-sm px-3 py-1.5 rounded font-bold hover:bg-[#0b5ed7] cursor-pointer"
                onClick={() => setFilters({ ...filters() })}
              >
                Filter
              </button>
              <button
                class="w-full border border-gray-400 text-gray-700 text-sm px-3 py-1.5 rounded hover:bg-gray-200 cursor-pointer"
                onClick={() => setFilters({ month: '', from: '', to: '' })}
              >
                Clear
              </button>
            </div>
          </div>
        </div>

        <Show when={salesQuery.isLoading}>
          <div class="px-4 py-8 text-center text-gray-500">Loading sales...</div>
        </Show>
        <Show when={salesQuery.isError}>
          <div class="px-4 py-8 text-center text-red-600">
            Failed to load sales: {salesQuery.error?.message}
          </div>
        </Show>
        <Show when={salesQuery.isSuccess}>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
                <tr>
                  <th class="px-4 py-3 text-left">Invoice</th>
                  <th class="py-3 text-left">Date</th>
                  <th class="py-3 text-left">Customer</th>
                  <th class="py-3 text-left">Mode</th>
                  <th class="py-3 text-left">Status</th>
                  <th class="py-3 text-right">Amount (₹)</th>
                  <th class="px-4 py-3 text-center" style="width: 150px;">Actions</th>
                </tr>
              </thead>
              <tbody>
                <For each={filteredSales().slice().reverse()}>
                  {(sale) => {
                    const paid = Number(sale.paid_amount)
                    const total = Number(sale.grand_total)
                    const mode = paid >= total ? 'Cash' : 'Credit'
                    const status = paid >= total ? 'Paid' : paid > 0 ? 'Partial' : 'Unpaid'
                    const badge =
                      status === 'Paid' ? 'bg-green-500'
                        : status === 'Partial' ? 'bg-yellow-500 text-gray-900'
                          : 'bg-red-500'

                    return (
                      <tr class="border-b border-gray-200 hover:bg-gray-50">
                        <td class="px-4 py-3 font-bold">{fmtId(sale.sale_id)}</td>
                        <td class="py-3">{sale.date.split('T')[0]}</td>
                        <td class="py-3">{custName(sale)}</td>
                        <td class="py-3">
                          <span
                            class={`inline-block px-2 py-0.5 rounded text-xs font-bold text-white ${
                              mode === 'Credit' ? 'bg-gray-500' : 'bg-green-500'
                            }`}
                          >
                            {mode}
                          </span>
                        </td>
                        <td class="py-3">
                          <span
                            class={`inline-block px-2 py-0.5 rounded text-xs font-bold text-white ${badge}`}
                          >
                            {status}
                          </span>
                        </td>
                        <td class="py-3 text-right font-bold text-[#0d6efd] px-4">
                          ₹{formatMoney(Number(sale.grand_total))}
                        </td>
                        <td class="py-3 text-center px-4" style="width: 150px;">
                          <div class="flex justify-center gap-1">
                            <Link
                              to="/record-sale"
                              search={{ edit: sale.sale_id }}
                              class="w-9 h-9 inline-flex items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 hover:-translate-y-[3px] hover:shadow-lg hover:border-transparent transition-all cursor-pointer group"
                            >
                              <svg class="w-4 h-4 text-gray-600 group-hover:text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                              </svg>
                            </Link>
                            <button
                              onClick={() => {
                                if (confirm('Delete this sale?'))
                                  deleteSale.mutateAsync(sale.sale_id)
                              }}
                              class="w-9 h-9 inline-flex items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 hover:-translate-y-[3px] hover:shadow-lg hover:border-transparent transition-all cursor-pointer group"
                            >
                              <svg class="w-4 h-4 text-gray-600 group-hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        </td>
                      </tr>
                    )
                  }}
                </For>
                <For each={filteredSales().length === 0 ? [true] : []}>
                  {() => (
                    <tr>
                      <td colspan="7" class="text-center text-gray-500 py-8">
                        No sales found.
                      </td>
                    </tr>
                  )}
                </For>
              </tbody>
            </table>
          </div>
        </Show>
      </div>
    </div>
  )
}
