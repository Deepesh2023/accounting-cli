import { For, createMemo } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import {
  transactions,
  partyList,
  setTransactions,
  setPartyList,
  formatMoney,
} from '../lib/store'

export const Route = createFileRoute('/outstanding')({ component: Outstanding })

interface OutstandingEntry {
  id: number
  type: 'Sale' | 'Purchase'
  ref: string
  date: string
  partyId: string
  total: number
  balance: number
  dueDate: string | null
}

function Outstanding() {
  const entries = createMemo<OutstandingEntry[]>(() => {
    const result: OutstandingEntry[] = []
    for (const t of transactions) {
      if (
        t.type === 'Sale' &&
        t.sale_details &&
        t.sale_details.balance_amount > 0
      ) {
        result.push({
          id: t.id,
          type: 'Sale',
          ref: t.sale_details.invoice_no,
          date: t.date,
          partyId: t.sale_details.customer_id,
          total: t.amount,
          balance: t.sale_details.balance_amount,
          dueDate: t.sale_details.due_date || null,
        })
      }
      if (
        t.type === 'Purchase' &&
        t.purchase_details &&
        t.purchase_details.balance_amount > 0
      ) {
        result.push({
          id: t.id,
          type: 'Purchase',
          ref: t.purchase_details.bill_no,
          date: t.date,
          partyId: t.purchase_details.supplier_id,
          total: t.amount,
          balance: t.purchase_details.balance_amount,
          dueDate: t.purchase_details.due_date || null,
        })
      }
    }
    return result
  })

  function settle(id: number) {
    const t = transactions.find((x) => x.id === id)
    if (!t) return

    const details =
      t.type === 'Sale' ? t.sale_details : t.purchase_details
    if (!details) return

    const currentBal = details.balance_amount
    const input = window.prompt(
      `Enter amount to settle (Max outstanding: ₹${formatMoney(currentBal)}):`,
      String(currentBal),
    )
    if (input === null) return

    const settleAmt = parseFloat(input)
    if (isNaN(settleAmt) || settleAmt <= 0) {
      alert('Invalid amount entered.')
      return
    }
    if (settleAmt > currentBal) {
      alert('Cannot settle more than the outstanding balance.')
      return
    }

    const idx = transactions.findIndex((x) => x.id === id)
    if (idx === -1) return

    const newPaid = details.paid_amount + settleAmt
    const newBal = details.balance_amount - settleAmt
    const newStatus: 'Paid' | 'Partial' | 'Unpaid' =
      newBal === 0 ? 'Paid' : 'Partial'

    if (t.type === 'Sale') {
      const sd = t.sale_details!
      setTransactions(idx, 'sale_details', {
        ...sd,
        paid_amount: newPaid,
        balance_amount: newBal,
        payment_status: newStatus,
      })

      if (sd.customer_id) {
        const pIdx = partyList.findIndex(
          (x) => String(x.id) === String(sd.customer_id),
        )
        if (pIdx !== -1) {
          const party = partyList[pIdx]
          const signedBal =
            (party.type === 'Receive' ? 1 : -1) * party.balance
          const newSigned = signedBal - settleAmt
          setPartyList(pIdx, {
            balance: Math.abs(newSigned),
            type: newSigned >= 0 ? 'Receive' : 'Pay',
          })
        }
      }
    } else if (t.type === 'Purchase') {
      const pd = t.purchase_details!
      setTransactions(idx, 'purchase_details', {
        ...pd,
        paid_amount: newPaid,
        balance_amount: newBal,
        payment_status: newStatus,
      })

      if (pd.supplier_id) {
        const pIdx = partyList.findIndex(
          (x) => String(x.id) === String(pd.supplier_id),
        )
        if (pIdx !== -1) {
          const party = partyList[pIdx]
          const signedBal =
            (party.type === 'Receive' ? 1 : -1) * party.balance
          const newSigned = signedBal + settleAmt
          setPartyList(pIdx, {
            balance: Math.abs(newSigned),
            type: newSigned >= 0 ? 'Receive' : 'Pay',
          })
        }
      }
    }
  }

  return (
    <div class="space-y-6">
      <div class="border-0 shadow-sm rounded-lg overflow-hidden mt-4">
        <div class="bg-white pt-4 pb-3 px-4">
          <h5 class="mb-0 font-bold text-red-500">Outstanding & Due Report</h5>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="px-4 py-3 text-left">Ref No</th>
                <th class="py-3 text-left">Date</th>
                <th class="py-3 text-left">Party</th>
                <th class="py-3 text-left">Type</th>
                <th class="py-3 text-right">Total Amount (₹)</th>
                <th class="py-3 text-right">Balance Due (₹)</th>
                <th class="py-3 text-left">Due Date</th>
                <th class="py-3 text-left">Overdue Status</th>
                <th class="px-4 py-3 text-center" style="width: 100px;">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <For each={entries()}>
                {(o) => {
                  const party = partyList.find(
                    (p) => String(p.id) === String(o.partyId),
                  )
                  const partyName = party ? party.name : 'Unknown'
                  const isRec = o.type === 'Sale'

                  let overdueText = <span class="text-green-600">Not Due</span>
                  if (o.dueDate) {
                    const due = new Date(o.dueDate)
                    const diff = new Date().getTime() - due.getTime()
                    if (diff > 0) {
                      const days = Math.floor(
                        diff / (1000 * 60 * 60 * 24),
                      )
                      overdueText = (
                        <span class="inline-block px-2 py-0.5 rounded text-xs font-bold text-white bg-red-500">
                          {days} days overdue
                        </span>
                      )
                    }
                  }

                  return (
                    <tr class="border-b border-gray-200 hover:bg-gray-50">
                      <td class="px-4 py-3 font-bold">{o.ref}</td>
                      <td class="py-3">{o.date}</td>
                      <td class="py-3">{partyName}</td>
                      <td class="py-3">
                        <span
                          class={`inline-block px-2 py-0.5 rounded text-xs font-bold text-white ${
                            isRec ? 'bg-green-500' : 'bg-yellow-500 text-gray-900'
                          }`}
                        >
                          {isRec ? 'Receivable' : 'Payable'}
                        </span>
                      </td>
                      <td class="py-3 text-right">{formatMoney(o.total)}</td>
                      <td class="py-3 text-right font-bold text-red-500">
                        {formatMoney(o.balance)}
                      </td>
                      <td class="py-3">{o.dueDate || '-'}</td>
                      <td class="py-3">{overdueText}</td>
                      <td class="py-3 text-center px-4" style="width: 100px;">
                        <button
                          onClick={() => settle(o.id)}
                          class="border border-[#0d6efd] text-[#0d6efd] text-xs px-3 py-1 rounded font-bold hover:bg-[#0d6efd] hover:text-white cursor-pointer"
                        >
                          Settle
                        </button>
                      </td>
                    </tr>
                  )
                }}
              </For>
              <For each={entries().length === 0 ? [true] : []}>
                {() => (
                  <tr>
                    <td colspan="9" class="text-center text-gray-500 py-8">
                      No outstanding records found.
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
