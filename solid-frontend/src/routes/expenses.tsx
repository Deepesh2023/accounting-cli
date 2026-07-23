import { For, Show, createSignal } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import {
  expenseList,
  setExpenseList,
  getNextId,
  formatMoney,
} from '../lib/store'
import type { Expense } from '../lib/types'

export const Route = createFileRoute('/expenses')({ component: Expenses })

const categories = [
  'Rent', 'Utilities', 'Salary', 'Marketing',
  'Office Supplies', 'Travel', 'Other',
]

function Expenses() {
  const [showModal, setShowModal] = createSignal(false)
  const [editingId, setEditingId] = createSignal<number | null>(null)
  const [form, setForm] = createSignal({
    date: new Date().toISOString().split('T')[0],
    category: 'Rent',
    paid_by: 'Cash',
    amount: '',
    notes: '',
  })

  function openAdd() {
    setEditingId(null)
    setForm({
      date: new Date().toISOString().split('T')[0],
      category: 'Rent',
      paid_by: 'Cash',
      amount: '',
      notes: '',
    })
    setShowModal(true)
  }

  function openEdit(e: Expense) {
    setEditingId(e.id)
    setForm({
      date: e.date,
      category: e.category,
      paid_by: e.paid_by,
      amount: String(e.amount),
      notes: e.notes,
    })
    setShowModal(true)
  }

  function save() {
    const f = form()
    if (!f.date || !f.amount || parseFloat(f.amount) <= 0) {
      alert('Valid date and amount required.')
      return
    }

    const amount = parseFloat(f.amount)

    if (editingId() !== null) {
      const idx = expenseList.findIndex((e) => e.id === editingId())
      if (idx !== -1) {
        setExpenseList(idx, {
          ...expenseList[idx],
          date: f.date,
          category: f.category,
          paid_by: f.paid_by,
          amount,
          notes: f.notes,
        })
      }
    } else {
      setExpenseList(expenseList.length, {
        id: getNextId(),
        date: f.date,
        category: f.category,
        paid_by: f.paid_by,
        amount,
        notes: f.notes,
      })
    }

    setShowModal(false)
  }

  function remove(id: number) {
    if (!confirm('Delete this expense?')) return
    const idx = expenseList.findIndex((e) => e.id === id)
    if (idx !== -1) setExpenseList((prev) => prev.filter((_, i) => i !== idx))
  }

  return (
    <div class="space-y-6">
      <div class="border-0 shadow-sm rounded-lg overflow-hidden mt-4">
        <div class="bg-white pt-4 pb-3 px-4 flex justify-between items-center">
          <h5 class="mb-0 font-bold text-gray-600">Expenses</h5>
          <button
            onClick={openAdd}
            class="bg-[#0d6efd] text-white text-sm px-3 py-1.5 rounded shadow-sm font-bold hover:bg-[#0b5ed7] cursor-pointer"
          >
            + Add Expense
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="px-4 py-3 text-left">Date</th>
                <th class="py-3 text-left">Category</th>
                <th class="py-3 text-left">Paid By</th>
                <th class="py-3 text-left">Notes</th>
                <th class="py-3 text-right">Amount (₹)</th>
                <th class="px-4 py-3 text-center" style="width: 100px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <For each={expenseList.slice().reverse()}>
                {(e) => (
                  <tr class="border-b border-gray-200 hover:bg-gray-50">
                    <td class="px-4 py-3">{e.date}</td>
                    <td class="py-3">
                      <span class="inline-block px-2 py-0.5 rounded text-xs font-bold text-white bg-gray-500">
                        {e.category}
                      </span>
                    </td>
                    <td class="py-3">{e.paid_by}</td>
                    <td class="py-3 text-gray-500">{e.notes || '-'}</td>
                    <td class="py-3 text-right font-bold text-red-500">
                      {formatMoney(e.amount)}
                    </td>
                    <td class="py-3 text-center px-4" style="width: 100px;">
                      <div class="flex justify-center gap-1">
                        <button
                          onClick={() => openEdit(e)}
                          class="w-9 h-9 inline-flex items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 hover:-translate-y-[3px] hover:shadow-lg hover:border-transparent transition-all cursor-pointer group"
                          data-name="Edit"
                        >
                          <svg class="w-4 h-4 text-gray-600 group-hover:text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button
                          onClick={() => remove(e.id)}
                          class="w-9 h-9 inline-flex items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 hover:-translate-y-[3px] hover:shadow-lg hover:border-transparent transition-all cursor-pointer group"
                          data-name="Delete"
                        >
                          <svg class="w-4 h-4 text-gray-600 group-hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                )}
              </For>
              <For each={expenseList.length === 0 ? [true] : []}>
                {() => (
                  <tr>
                    <td colspan="6" class="text-center text-gray-500 py-8">
                      No expenses recorded yet.
                    </td>
                  </tr>
                )}
              </For>
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      <Show when={showModal()}>
        <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div class="bg-white rounded-xl shadow-lg w-full max-w-md mx-4 overflow-hidden">
            <div class="bg-gray-50 border-0 py-3 px-4">
              <h5 class="font-bold mb-0">{editingId() !== null ? 'Edit' : 'Add'} Expense</h5>
            </div>
            <div class="p-4 space-y-4">
              <div>
                <label class="block text-gray-500 text-xs font-bold mb-1">Date</label>
                <input
                  type="date"
                  class="w-full border border-gray-300 rounded px-3 py-2"
                  value={form().date}
                  onInput={(e) => setForm({ ...form(), date: e.currentTarget.value })}
                />
              </div>
              <div>
                <label class="block text-gray-500 text-xs font-bold mb-1">Category</label>
                <select
                  class="w-full border border-gray-300 rounded px-3 py-2"
                  value={form().category}
                  onChange={(e) => setForm({ ...form(), category: e.currentTarget.value })}
                >
                  <For each={categories}>
                    {(c) => <option value={c}>{c}</option>}
                  </For>
                </select>
              </div>
              <div>
                <label class="block text-gray-500 text-xs font-bold mb-1">Paid By</label>
                <select
                  class="w-full border border-gray-300 rounded px-3 py-2"
                  value={form().paid_by}
                  onChange={(e) => setForm({ ...form(), paid_by: e.currentTarget.value })}
                >
                  <option value="Cash">Cash</option>
                  <option value="Bank">Bank</option>
                </select>
              </div>
              <div>
                <label class="block text-gray-500 text-xs font-bold mb-1">Amount (₹)</label>
                <input
                  type="number"
                  class="w-full border border-gray-300 rounded px-3 py-2"
                  placeholder="0.00"
                  value={form().amount}
                  onInput={(e) => setForm({ ...form(), amount: e.currentTarget.value })}
                />
              </div>
              <div>
                <label class="block text-gray-500 text-xs font-bold mb-1">Notes</label>
                <textarea
                  class="w-full border border-gray-300 rounded px-3 py-2"
                  rows="2"
                  placeholder="Optional notes..."
                  value={form().notes}
                  onInput={(e) => setForm({ ...form(), notes: e.currentTarget.value })}
                />
              </div>
              <button
                onClick={save}
                class="w-full bg-[#0d6efd] text-white py-2 rounded shadow-sm font-bold hover:bg-[#0b5ed7] cursor-pointer"
              >
                Save Expense
              </button>
            </div>
          </div>
        </div>
      </Show>
    </div>
  )
}
