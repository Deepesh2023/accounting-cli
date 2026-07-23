import { For, createMemo } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import { transactions, expenseList, formatMoney } from '../lib/store'

export const Route = createFileRoute('/transactions')({ component: Transactions })

function getModeBalance(mode: string) {
  let bal = 0
  for (const t of transactions) {
    if (t.payment_mode === mode) {
      if (t.type === 'Sale' || t.type === 'Income' || t.type === 'Capital') bal += t.amount
      else if (t.type === 'Purchase' || t.type === 'Expense' || t.type === 'Asset') bal -= t.amount
    }
  }
  for (const e of expenseList) {
    if (e.paid_by === mode) bal -= e.amount
  }
  return bal
}

function Transactions() {
  const cashBalance = createMemo(() => getModeBalance('Cash'))
  const bankBalance = createMemo(() => getModeBalance('Bank'))

  return (
    <div class="space-y-6">
      <div class="flex items-stretch mt-4 gap-4">
        <div class="w-1/2">
          <div class="bg-[#0dcaf0] text-white border-0 shadow-sm rounded-xl h-full">
            <div class="p-4">
              <p class="uppercase font-bold mb-1 tracking-wider text-[0.85em]">
                Cash Balance
              </p>
              <h3 class="mb-0 font-bold text-2xl">₹{formatMoney(cashBalance())}</h3>
            </div>
          </div>
        </div>
        <div class="w-1/2">
          <div class="bg-[#0d6efd] text-white border-0 shadow-sm rounded-xl h-full">
            <div class="p-4">
              <p class="uppercase font-bold mb-1 tracking-wider text-[0.85em]">
                Bank Balance
              </p>
              <h3 class="mb-0 font-bold text-2xl">₹{formatMoney(bankBalance())}</h3>
            </div>
          </div>
        </div>
      </div>

      <div class="border-0 shadow-sm rounded-lg overflow-hidden">
        <div class="bg-white pt-4 pb-3 px-4">
          <h5 class="mb-0 font-bold text-gray-600">Transaction History</h5>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="py-3 pl-4 text-left">#</th>
                <th class="py-3 text-left">Date</th>
                <th class="py-3 text-left">Particulars</th>
                <th class="py-3 text-left">Type</th>
                <th class="py-3 text-left">Payment Mode</th>
                <th class="py-3 pr-4 text-right">Amount (₹)</th>
              </tr>
            </thead>
            <tbody>
              <For each={transactions.slice().reverse()}>
                {(t, i) => {
                  const modeColor =
                    t.payment_mode === 'Cash' || t.payment_mode === 'Bank'
                      ? 'text-green-600'
                      : 'text-yellow-600'
                  return (
                    <tr class="border-b border-gray-200 hover:bg-gray-50 cursor-pointer">
                      <td class="py-3 pl-4">{transactions.length - i()}</td>
                      <td class="py-3">{t.date}</td>
                      <td class="py-3">{t.particulars}</td>
                      <td class="py-3">
                        <span class="inline-block px-2 py-0.5 rounded text-xs font-bold text-white bg-gray-500">
                          {t.type}
                        </span>
                      </td>
                      <td class="py-3">
                        <span class={`inline-block px-2 py-0.5 rounded text-xs font-bold bg-gray-100 ${modeColor}`}>
                          {t.payment_mode}
                        </span>
                      </td>
                      <td class="py-3 pr-4 text-right font-bold">
                        ₹{formatMoney(t.amount)}
                      </td>
                    </tr>
                  )
                }}
              </For>
              <For each={transactions.length === 0 ? [true] : []}>
                {() => (
                  <tr>
                    <td colspan="6" class="text-center text-gray-500 py-8">
                      No transactions yet.
                    </td>
                  </tr>
                )}
              </For>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
