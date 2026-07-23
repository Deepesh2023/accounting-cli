import { For, Show, createSignal } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import {
  quotationList,
  setQuotationList,
  partyList,
  stockList,
  getNextId,
  formatMoney,
} from '../lib/store'
import type { QuotationItem } from '../lib/types'

export const Route = createFileRoute('/quotation')({ component: Quotation })

function Quotation() {
  const [showModal, setShowModal] = createSignal(false)
  const [editingId, setEditingId] = createSignal<number | null>(null)
  const [form, setForm] = createSignal({
    quote_no: 'Q' + String(Date.now()).slice(-4),
    date: new Date().toISOString().split('T')[0],
    customer_id: '',
    customer_name: '',
    phone: '',
  })
  const [items, setItems] = createSignal<QuotationItem[]>([])
  const [nextRow, setNextRow] = createSignal(0)

  const grandTotal = () =>
    items().reduce((sum, it) => {
      const base = it.qty * it.price
      return sum + base + (base * it.tax) / 100
    }, 0)

  function openAdd() {
    setEditingId(null)
    setForm({
      quote_no: 'Q' + String(Date.now()).slice(-4),
      date: new Date().toISOString().split('T')[0],
      customer_id: '',
      customer_name: '',
      phone: '',
    })
    setItems([
      { item_id: '', qty: 1, price: 0, tax: 0 },
    ])
    setNextRow(1)
    setShowModal(true)
  }

  function openEdit(q: (typeof quotationList)[number]) {
    setEditingId(q.id)
    setForm({
      quote_no: q.quote_no,
      date: q.date,
      customer_id: q.customer_id,
      customer_name: q.customer_name,
      phone: partyList.find((p) => String(p.id) === String(q.customer_id))?.phone || '',
    })
    setItems(
      q.items.length > 0 ? q.items.map((it) => ({ ...it })) : [{ item_id: '', qty: 1, price: 0, tax: 0 }],
    )
    setNextRow(q.items.length)
    setShowModal(true)
  }

  function selectCustomer(id: string) {
    const p = partyList.find((x) => String(x.id) === String(id))
    setForm({
      ...form(),
      customer_id: id,
      customer_name: p?.name || 'Walk-in',
      phone: p?.phone || '',
    })
  }

  function addRow() {
    setItems([...items(), { item_id: '', qty: 1, price: 0, tax: 0 }])
    setNextRow(nextRow() + 1)
  }

  function updateItem(idx: number, patch: Partial<QuotationItem>) {
    setItems(items().map((it, i) => (i === idx ? { ...it, ...patch } : it)))
  }

  function removeItem(idx: number) {
    setItems(items().filter((_, i) => i !== idx))
  }

  function save() {
    const f = form()
    if (!f.date) return alert('Date required.')
    if (items().length === 0 || items().every((it) => !it.item_id)) {
      return alert('Add at least one item.')
    }

    const total = grandTotal()
    const quote = {
      id: editingId() ?? getNextId(),
      quote_no: f.quote_no,
      date: f.date,
      customer_id: f.customer_id,
      customer_name: f.customer_name || 'Walk-in',
      total,
      items: items().filter((it) => it.item_id),
    }

    if (editingId() !== null) {
      const idx = quotationList.findIndex((q) => q.id === editingId())
      if (idx !== -1) setQuotationList(idx, quote)
    } else {
      setQuotationList(quotationList.length, quote)
    }

    setShowModal(false)
  }

  function removeQuote(id: number) {
    if (!confirm('Delete this quotation?')) return
    const idx = quotationList.findIndex((q) => q.id === id)
    if (idx !== -1) setQuotationList((prev) => prev.filter((_, i) => i !== idx))
  }

  return (
    <div class="space-y-6">
      <div class="border-0 shadow-sm rounded-lg overflow-hidden mt-4">
        <div class="bg-white pt-4 pb-3 px-4 flex justify-between items-center">
          <h5 class="mb-0 font-bold text-gray-600">Quotation History</h5>
          <button
            onClick={openAdd}
            class="bg-[#0d6efd] text-white text-sm px-3 py-1.5 rounded shadow-sm font-bold hover:bg-[#0b5ed7] cursor-pointer"
          >
            + Add Quotation
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="px-4 py-3 text-left">ID</th>
                <th class="py-3 text-left">Date</th>
                <th class="py-3 text-left">Customer</th>
                <th class="py-3 text-right">Total Amount</th>
                <th class="py-3 text-center" style="width: 100px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <For each={quotationList.slice().reverse()}>
                {(q) => (
                  <tr class="border-b border-gray-200 hover:bg-gray-50 cursor-pointer">
                    <td class="px-4 py-3 font-bold">{q.quote_no}</td>
                    <td class="py-3">{q.date}</td>
                    <td class="py-3">{q.customer_name}</td>
                    <td class="py-3 text-right font-bold text-[#0d6efd]">
                      ₹{formatMoney(q.total)}
                    </td>
                    <td class="py-3 text-center px-4" style="width: 100px;">
                      <div class="flex justify-center gap-1">
                        <button
                          onClick={() => openEdit(q)}
                          class="w-9 h-9 inline-flex items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 hover:-translate-y-[3px] hover:shadow-lg hover:border-transparent transition-all cursor-pointer group"
                          data-name="Edit Quotation"
                        >
                          <svg class="w-4 h-4 text-gray-600 group-hover:text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button
                          onClick={() => removeQuote(q.id)}
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
              <For each={quotationList.length === 0 ? [true] : []}>
                {() => (
                  <tr>
                    <td colspan="5" class="text-center text-gray-500 py-8">
                      No quotations yet.
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
        <div class="fixed inset-0 z-50 flex items-start justify-center bg-black/40 pt-10 overflow-y-auto">
          <div class="bg-white rounded-xl shadow-lg w-full max-w-4xl mx-4 overflow-hidden">
            <div class="bg-[#0d6efd] text-white p-4">
              <h5 class="font-bold mb-0">Create Quotation (No Accounting Impact)</h5>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-4 gap-4 mb-4">
                <div>
                  <label class="block text-gray-500 text-xs font-bold mb-1 uppercase">Quotation No</label>
                  <input
                    type="text"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 font-bold text-sm"
                    value={form().quote_no}
                    onInput={(e) => setForm({ ...form(), quote_no: e.currentTarget.value })}
                  />
                </div>
                <div>
                  <label class="block text-gray-500 text-xs font-bold mb-1 uppercase">Date</label>
                  <input
                    type="date"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                    value={form().date}
                    onInput={(e) => setForm({ ...form(), date: e.currentTarget.value })}
                  />
                </div>
                <div>
                  <label class="block text-gray-500 text-xs font-bold mb-1 uppercase">Customer Name</label>
                  <select
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                    value={form().customer_id}
                    onChange={(e) => selectCustomer(e.currentTarget.value)}
                  >
                    <option value="">Select Customer</option>
                    <For each={partyList}>
                      {(p) => <option value={p.id}>{p.name}</option>}
                    </For>
                  </select>
                </div>
                <div>
                  <label class="block text-gray-500 text-xs font-bold mb-1 uppercase">Phone No</label>
                  <input
                    type="text"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm bg-gray-100"
                    value={form().phone}
                    disabled
                  />
                </div>
              </div>

              <div class="overflow-x-auto mb-4">
                <table class="w-full text-sm">
                  <thead class="bg-gray-100 text-gray-500 uppercase text-xs">
                    <tr>
                      <th class="text-left p-2">Item Description</th>
                      <th class="text-center p-2" style="width: 100px;">Qty</th>
                      <th class="text-right p-2" style="width: 140px;">Price</th>
                      <th class="text-center p-2" style="width: 80px;">Tax %</th>
                      <th class="text-right p-2" style="width: 140px;">Total</th>
                      <th class="text-center p-2" style="width: 40px;"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <For each={items()}>
                      {(it, idx) => {
                        const base = it.qty * it.price
                        const rowTotal = base + (base * it.tax) / 100
                        return (
                          <tr class="border-b border-gray-100">
                            <td class="p-1">
                              <select
                                class="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                                value={it.item_id}
                                onChange={(e) => {
                                  const id = e.currentTarget.value
                                  const st = stockList.find((s) => String(s.id) === String(id))
                                  updateItem(idx(), {
                                    item_id: id,
                                    price: st?.price ?? it.price,
                                  })
                                }}
                              >
                                <option value="">Select Item</option>
                                <For each={stockList}>
                                  {(s) => (
                                    <option value={s.id}>
                                      {s.name} (Stock: {s.qty})
                                    </option>
                                  )}
                                </For>
                              </select>
                            </td>
                            <td class="p-1">
                              <input
                                type="number"
                                class="w-full border border-gray-300 rounded px-2 py-1 text-center text-sm"
                                value={it.qty}
                                min="1"
                                onInput={(e) =>
                                  updateItem(idx(), { qty: parseInt(e.currentTarget.value) || 0 })
                                }
                              />
                            </td>
                            <td class="p-1">
                              <input
                                type="number"
                                class="w-full border border-gray-300 rounded px-2 py-1 text-right text-sm"
                                value={it.price}
                                onInput={(e) =>
                                  updateItem(idx(), { price: parseFloat(e.currentTarget.value) || 0 })
                                }
                              />
                            </td>
                            <td class="p-1">
                              <input
                                type="number"
                                class="w-full border border-gray-300 rounded px-2 py-1 text-center text-sm"
                                value={it.tax}
                                onInput={(e) =>
                                  updateItem(idx(), { tax: parseFloat(e.currentTarget.value) || 0 })
                                }
                              />
                            </td>
                            <td class="p-1 text-right font-bold text-sm">
                              {formatMoney(rowTotal)}
                            </td>
                            <td class="p-1 text-center">
                              <button
                                onClick={() => removeItem(idx())}
                                class="text-red-500 hover:text-red-700 cursor-pointer text-sm"
                              >
                                ✕
                              </button>
                            </td>
                          </tr>
                        )
                      }}
                    </For>
                  </tbody>
                </table>
              </div>

              <div class="flex justify-between items-center mt-3">
                <button
                  onClick={addRow}
                  class="border border-[#0d6efd] text-[#0d6efd] text-sm px-4 py-1.5 rounded-lg font-bold hover:bg-[#0d6efd] hover:text-white cursor-pointer"
                >
                  + Add Row
                </button>
                <div class="text-right">
                  <span class="text-gray-500 text-xs uppercase font-bold">Grand Total</span>
                  <h2 class="mb-0 font-bold text-[#0d6efd]">₹{formatMoney(grandTotal())}</h2>
                </div>
              </div>
            </div>

            <div class="border-t border-gray-200 p-4 bg-gray-50 flex justify-end gap-3">
              <button
                onClick={() => setShowModal(false)}
                class="text-gray-500 font-bold px-4 py-2 rounded-lg hover:bg-gray-200 cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={save}
                class="bg-[#0d6efd] text-white px-5 py-2 rounded-lg font-bold shadow hover:bg-[#0b5ed7] cursor-pointer"
              >
                Save Quotation
              </button>
            </div>
          </div>
        </div>
      </Show>
    </div>
  )
}
