import { createSignal, For, Show } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import type { StockItem } from '../lib/types'
import { stockList, setStockList, formatMoney, getNextId } from '../lib/store'

export const Route = createFileRoute('/stock')({ component: Stock })

function Stock() {
  const [showModal, setShowModal] = createSignal(false)
  const [editingId, setEditingId] = createSignal<number | null>(null)
  const [form, setForm] = createSignal({
    name: '',
    item_code: '',
    qty: 0,
    unit: '',
    price: 0,
  })

  function openNew() {
    setEditingId(null)
    setForm({ name: '', item_code: '', qty: 0, unit: '', price: 0 })
    setShowModal(true)
  }

  function openEdit(id: number) {
    const s = stockList.find((x) => x.id === id)
    if (!s) return
    setEditingId(id)
    setForm({ name: s.name, item_code: s.item_code, qty: s.qty, unit: s.unit, price: s.price })
    setShowModal(true)
  }

  function handleSave() {
    const f = form()
    if (!f.name.trim()) return
    if (editingId()) {
      setStockList((s) => s.id === editingId(), 'name', f.name.trim())
      setStockList((s) => s.id === editingId(), 'item_code', f.item_code)
      setStockList((s) => s.id === editingId(), 'qty', f.qty)
      setStockList((s) => s.id === editingId(), 'unit', f.unit)
      setStockList((s) => s.id === editingId(), 'price', f.price)
    } else {
      setStockList(stockList.length, {
        id: getNextId(),
        name: f.name.trim(),
        item_code: f.item_code,
        qty: f.qty,
        unit: f.unit,
        price: f.price,
      })
    }
    setShowModal(false)
  }

  function handleDelete(id: number) {
    if (!confirm('Delete this item?')) return
    setStockList(stockList.filter((s) => s.id !== id))
  }

  const totalValue = (s: StockItem) => s.qty * s.price

  return (
    <div class="space-y-6">
      <div class="border-0 shadow-sm rounded-lg overflow-hidden">
        <div class="bg-white px-4 py-3 flex items-center justify-between">
          <h5 class="mb-0 font-bold text-gray-700">Stock Inventory</h5>
          <button
            onClick={openNew}
            class="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-3 py-1.5 rounded transition-colors"
          >
            + Add Stock
          </button>
        </div>
        <div class="px-4 py-2 text-sm text-blue-700 bg-blue-50 border border-blue-200 rounded mx-3 mb-2">
          <strong>Tip:</strong> Click Edit to modify a stock item.
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="py-3 pl-4 text-left" style="width:50px">#</th>
                <th class="py-3 text-left">Item Code</th>
                <th class="py-3 text-left">Name</th>
                <th class="py-3 text-right">Qty</th>
                <th class="py-3 text-left">Unit</th>
                <th class="py-3 text-right">Price (₹)</th>
                <th class="py-3 text-right">Total Value (₹)</th>
                <th class="py-3 pr-4 text-center" style="width:120px">Actions</th>
              </tr>
            </thead>
            <tbody>
              <For each={stockList}>
                {(s, i) => (
                  <tr class="border-b border-gray-200 hover:bg-gray-50">
                    <td class="py-3 pl-4">{i() + 1}</td>
                    <td class="py-3">{s.item_code || '-'}</td>
                    <td class="py-3 font-medium">{s.name}</td>
                    <td class="py-3 text-right">{s.qty}</td>
                    <td class="py-3">{s.unit || '-'}</td>
                    <td class="py-3 text-right">₹{formatMoney(s.price)}</td>
                    <td class="py-3 text-right font-bold">₹{formatMoney(totalValue(s))}</td>
                    <td class="py-3 pr-4 text-center">
                      <button
                        onClick={() => openEdit(s.id)}
                        class="text-blue-600 hover:text-blue-800 underline text-xs mr-2"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(s.id)}
                        class="text-red-600 hover:text-red-800 underline text-xs"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                )}
              </For>
              <For each={stockList.length === 0 ? [true] : []}>
                {() => (
                  <tr>
                    <td colspan="8" class="text-center text-gray-500 py-8">
                      No stock items added yet.
                    </td>
                  </tr>
                )}
              </For>
            </tbody>
          </table>
        </div>
      </div>

      <Show when={showModal()}>
        <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40" onClick={() => setShowModal(false)}>
          <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4" onClick={(e) => e.stopPropagation()}>
            <div class="px-4 py-3 border-b border-gray-200">
              <h5 class="mb-0 font-bold text-gray-700">{editingId() !== null ? 'Edit Stock' : 'Stock Details'}</h5>
            </div>
            <div class="p-4">
              <div class="mb-3">
                <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={form().name}
                  onInput={(e) => setForm((prev) => ({ ...prev, name: e.currentTarget.value }))}
                  class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="block text-sm font-medium text-gray-700 mb-1">Item Code</label>
                <input
                  type="text"
                  value={form().item_code}
                  onInput={(e) => setForm((prev) => ({ ...prev, item_code: e.currentTarget.value }))}
                  class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  placeholder="Optional"
                />
              </div>
              <div class="flex gap-3">
                <div class="w-1/3 mb-3">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Qty</label>
                  <input
                    type="number"
                    min="0"
                    value={form().qty}
                    onInput={(e) => setForm((prev) => ({ ...prev, qty: parseFloat(e.currentTarget.value) || 0 }))}
                    class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                    required
                  />
                </div>
                <div class="w-1/3 mb-3">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Unit</label>
                  <input
                    type="text"
                    value={form().unit}
                    onInput={(e) => setForm((prev) => ({ ...prev, unit: e.currentTarget.value }))}
                    class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                    placeholder="Optional"
                  />
                </div>
                <div class="w-1/3 mb-3">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Price</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={form().price}
                    onInput={(e) => setForm((prev) => ({ ...prev, price: parseFloat(e.currentTarget.value) || 0 }))}
                    class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                    required
                  />
                </div>
              </div>
              <div class="text-right mt-3 flex gap-2 justify-end">
                <button
                  onClick={() => setShowModal(false)}
                  class="px-4 py-2 text-sm border border-gray-300 rounded hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSave}
                  class="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                >
                  {editingId() !== null ? 'Update Item' : 'Save Item'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Show>
    </div>
  )
}
