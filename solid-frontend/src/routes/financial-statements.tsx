import { createMemo, For, Show } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import {
  transactions,
  expenseList,
  stockList,
  partyList,
  formatMoney,
} from '../lib/store'

export const Route = createFileRoute('/financial-statements')({
  component: FinancialStatements,
})

function getTTypeSum(type: string) {
  return transactions.filter((t) => t.type === type).reduce((sum, t) => sum + t.amount, 0)
}

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

function FinancialStatements() {
  const sales = createMemo(() => getTTypeSum('Sale'))
  const purchases = createMemo(() => getTTypeSum('Purchase'))
  const expenses = createMemo(() => getTTypeSum('Expense') + expenseList.reduce((sum, e) => sum + e.amount, 0))
  const incomes = createMemo(() => getTTypeSum('Income'))
  const assets = createMemo(() => getTTypeSum('Asset'))
  const capital = createMemo(() => getTTypeSum('Capital'))
  const stockValue = createMemo(() => stockList.reduce((sum, st) => sum + st.quantity * Number(st.selling_price), 0))
  const debtors = createMemo(() => partyList.filter((p) => p.type === 'Receive').reduce((s, p) => s + p.balance, 0))
  const creditors = createMemo(() => partyList.filter((p) => p.type === 'Pay').reduce((s, p) => s + p.balance, 0))
  const cashBal = createMemo(() => getModeBalance('Cash'))
  const bankBal = createMemo(() => getModeBalance('Bank'))

  const trTotalDr = createMemo(() => purchases())
  const trTotalCr = createMemo(() => sales() + stockValue())
  const grossProfit = createMemo(() => trTotalCr() - trTotalDr())
  const hasGrossProfit = createMemo(() => grossProfit() >= 0)

  const plTotalDr = createMemo(() => (hasGrossProfit() ? 0 : Math.abs(grossProfit())) + expenses())
  const plTotalCr = createMemo(() => (hasGrossProfit() ? grossProfit() : 0) + incomes())
  const netProfit = createMemo(() => plTotalCr() - plTotalDr())
  const hasNetProfit = createMemo(() => netProfit() >= 0)

  const totalLiab = createMemo(() => capital() + netProfit() + creditors())
  const totalAssets = createMemo(() => assets() + stockValue() + cashBal() + bankBal() + debtors())
  const isTallied = createMemo(() => Math.abs(totalLiab() - totalAssets()) < 0.01)

  const debtorParties = createMemo(() => partyList.filter((p) => p.type === 'Receive' && p.balance > 0))
  const creditorParties = createMemo(() => partyList.filter((p) => p.type === 'Pay' && p.balance > 0))
  const maxPartyRows = createMemo(() => Math.max(debtorParties().length, creditorParties().length))

  return (
    <div class="space-y-6">
      {/* Trading Account */}
      <div class="border-0 shadow-sm rounded-lg overflow-hidden" style="border-top: 4px solid #0d6efd">
        <div class="text-center bg-white pt-4 pb-3">
          <h4 class="mb-1 font-bold text-blue-600">Trading Account</h4>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm border-collapse">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="py-3 pl-4 text-left w-[35%]">Particulars (Expenses)</th>
                <th class="py-3 text-right w-[15%]">Amount (₹)</th>
                <th class="py-3 pl-4 text-left w-[35%]">Particulars (Incomes)</th>
                <th class="py-3 pr-4 text-right w-[15%]">Amount (₹)</th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4">Purchases</td>
                <td class="py-2 text-right">₹{formatMoney(purchases())}</td>
                <td class="py-2 pl-4">Sales</td>
                <td class="py-2 pr-4 text-right">₹{formatMoney(sales())}</td>
              </tr>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4"></td>
                <td class="py-2 text-right"></td>
                <td class="py-2 pl-4">Closing Stock (From Stock List)</td>
                <td class="py-2 pr-4 text-right">₹{formatMoney(stockValue())}</td>
              </tr>
              <Show
                when={hasGrossProfit()}
                fallback={
                  <tr class="border-b border-gray-200 text-red-600 font-bold">
                    <td class="py-2 pl-4"></td>
                    <td class="py-2 text-right"></td>
                    <td class="py-2 pl-4">Gross Loss (c/d)</td>
                    <td class="py-2 pr-4 text-right">₹{formatMoney(Math.abs(grossProfit()))}</td>
                  </tr>
                }
              >
                <tr class="border-b border-gray-200 text-green-600 font-bold">
                  <td class="py-2 pl-4">Gross Profit (c/d)</td>
                  <td class="py-2 text-right">₹{formatMoney(grossProfit())}</td>
                  <td class="py-2 pl-4"></td>
                  <td class="py-2 pr-4 text-right"></td>
                </tr>
              </Show>
              <tr class="bg-gray-100 font-bold">
                <td class="py-2 pl-4">Total</td>
                <td class="py-2 text-right border-b-2 border-gray-800">
                  ₹{formatMoney(hasGrossProfit() ? trTotalDr() + grossProfit() : trTotalDr())}
                </td>
                <td class="py-2 pl-4">Total</td>
                <td class="py-2 pr-4 text-right border-b-2 border-gray-800">
                  ₹{formatMoney(hasGrossProfit() ? trTotalCr() : trTotalCr() + Math.abs(grossProfit()))}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Profit & Loss Account */}
      <div class="border-0 shadow-sm rounded-lg overflow-hidden" style="border-top: 4px solid #198754">
        <div class="text-center bg-white pt-4 pb-3">
          <h4 class="mb-1 font-bold text-green-600">Profit & Loss Account</h4>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm border-collapse">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="py-3 pl-4 text-left w-[35%]">Particulars (Expenses)</th>
                <th class="py-3 text-right w-[15%]">Amount (₹)</th>
                <th class="py-3 pl-4 text-left w-[35%]">Particulars (Incomes)</th>
                <th class="py-3 pr-4 text-right w-[15%]">Amount (₹)</th>
              </tr>
            </thead>
            <tbody>
              <Show
                when={hasGrossProfit()}
                fallback={
                  <tr class="border-b border-gray-200 text-red-600 font-bold">
                    <td class="py-2 pl-4">Gross Loss (b/d)</td>
                    <td class="py-2 text-right">₹{formatMoney(Math.abs(grossProfit()))}</td>
                    <td class="py-2 pl-4"></td>
                    <td class="py-2 pr-4 text-right"></td>
                  </tr>
                }
              >
                <tr class="border-b border-gray-200 text-green-600 font-bold">
                  <td class="py-2 pl-4"></td>
                  <td class="py-2 text-right"></td>
                  <td class="py-2 pl-4">Gross Profit (b/d)</td>
                  <td class="py-2 pr-4 text-right">₹{formatMoney(grossProfit())}</td>
                </tr>
              </Show>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4">Expenses</td>
                <td class="py-2 text-right">₹{formatMoney(expenses())}</td>
                <td class="py-2 pl-4">Other Incomes</td>
                <td class="py-2 pr-4 text-right">₹{formatMoney(incomes())}</td>
              </tr>
              <Show
                when={hasNetProfit()}
                fallback={
                  <tr class="border-b border-gray-200 text-red-600 font-bold">
                    <td class="py-2 pl-4"></td>
                    <td class="py-2 text-right"></td>
                    <td class="py-2 pl-4">Net Loss</td>
                    <td class="py-2 pr-4 text-right">₹{formatMoney(Math.abs(netProfit()))}</td>
                  </tr>
                }
              >
                <tr class="border-b border-gray-200 text-green-600 font-bold">
                  <td class="py-2 pl-4">Net Profit</td>
                  <td class="py-2 text-right">₹{formatMoney(netProfit())}</td>
                  <td class="py-2 pl-4"></td>
                  <td class="py-2 pr-4 text-right"></td>
                </tr>
              </Show>
              <tr class="bg-gray-100 font-bold">
                <td class="py-2 pl-4">Total</td>
                <td class="py-2 text-right border-b-2 border-gray-800">
                  ₹{formatMoney(hasNetProfit() ? plTotalDr() + netProfit() : plTotalDr())}
                </td>
                <td class="py-2 pl-4">Total</td>
                <td class="py-2 pr-4 text-right border-b-2 border-gray-800">
                  ₹{formatMoney(hasNetProfit() ? plTotalCr() : plTotalCr() + Math.abs(netProfit()))}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Balance Sheet */}
      <div class="border-0 shadow-sm rounded-lg overflow-hidden" style="border-top: 4px solid #6f42c1">
        <div class="bg-white px-4 py-3 flex items-center justify-between">
          <h4 class="mb-0 font-bold" style="color: #6f42c1">Balance Sheet</h4>
          <span
            class={`inline-block px-3 py-1.5 rounded text-sm font-bold shadow-sm ${
              isTallied()
                ? 'bg-green-100 text-green-700'
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            {isTallied() ? 'Tallied ✓' : 'Not Tallied'}
          </span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm border-collapse">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="py-3 pl-4 text-left w-[35%]">Liabilities & Equity</th>
                <th class="py-3 text-right w-[15%]">Amount (₹)</th>
                <th class="py-3 pl-4 text-left w-[35%]">Assets</th>
                <th class="py-3 pr-4 text-right w-[15%]">Amount (₹)</th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4">Capital</td>
                <td class="py-2 text-right">₹{formatMoney(capital())}</td>
                <td class="py-2 pl-4">Fixed Assets</td>
                <td class="py-2 pr-4 text-right">₹{formatMoney(assets())}</td>
              </tr>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4">
                  Add: Net Profit{!hasNetProfit() ? ' (or less Loss)' : ''}
                </td>
                <td class="py-2 text-right">₹{formatMoney(netProfit())}</td>
                <td class="py-2 pl-4 font-bold">Current Assets:</td>
                <td class="py-2 pr-4 text-right"></td>
              </tr>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4 font-bold">Current Liabilities:</td>
                <td class="py-2 text-right"></td>
                <td class="py-2 pl-4 pl-6">- Stock in Hand</td>
                <td class="py-2 pr-4 text-right">₹{formatMoney(stockValue())}</td>
              </tr>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4 pl-6 font-bold">- Sundry Creditors (To Pay)</td>
                <td class="py-2 text-right font-bold">₹{formatMoney(creditors())}</td>
                <td class="py-2 pl-4 pl-6 font-bold">- Sundry Debtors (To Receive)</td>
                <td class="py-2 pr-4 text-right font-bold">₹{formatMoney(debtors())}</td>
              </tr>
              <For each={Array.from({ length: maxPartyRows() })}>
                {(_, i) => {
                  const c = creditorParties()[i()]
                  const d = debtorParties()[i()]
                  return (
                    <tr class="border-b border-gray-200 text-gray-500 text-[0.9em]">
                      <td class="py-1 pl-8">{c ? c.name : ''}</td>
                      <td class="py-1 text-right">{c ? `₹${formatMoney(c.balance)}` : ''}</td>
                      <td class="py-1 pl-8">{d ? d.name : ''}</td>
                      <td class="py-1 pr-4 text-right">{d ? `₹${formatMoney(d.balance)}` : ''}</td>
                    </tr>
                  )
                }}
              </For>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4"></td>
                <td class="py-2 text-right"></td>
                <td class="py-2 pl-4 pl-6">- Cash Balance</td>
                <td class="py-2 pr-4 text-right">₹{formatMoney(cashBal())}</td>
              </tr>
              <tr class="border-b border-gray-200">
                <td class="py-2 pl-4"></td>
                <td class="py-2 text-right"></td>
                <td class="py-2 pl-4 pl-6">- Bank Balance</td>
                <td class="py-2 pr-4 text-right">₹{formatMoney(bankBal())}</td>
              </tr>
              <tr class="bg-gray-100 font-bold text-base">
                <td class="py-3 pl-4">Total</td>
                <td class="py-3 text-right border-b-2 border-gray-800">₹{formatMoney(totalLiab())}</td>
                <td class="py-3 pl-4">Total</td>
                <td class="py-3 pr-4 text-right border-b-2 border-gray-800">₹{formatMoney(totalAssets())}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
