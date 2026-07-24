import { createSignal, For, Show } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import { createForm } from '@tanstack/solid-form'
import { formatMoney, stockList, setStockList, persistState } from '../lib/store'
import { useStock, useCreateStock, useUpdateStock, useDeleteStock } from '../lib/api/useStock'
import type { components } from '../lib/api/schema'

type ProductResponse = components['schemas']['ProductResponse']
type ProductCreate = components['schemas']['ProductCreate']

export const Route = createFileRoute('/stock')({ component: Stock })

function Stock() {
  const [showModal, setShowModal] = createSignal(false)
  const [editingId, setEditingId] = createSignal<string | null>(null)

  const stockQuery = useStock()
  const createStock = useCreateStock()
  const updateStock = useUpdateStock()
  const deleteStock = useDeleteStock()

  const form = createForm(() => ({
    defaultValues: {
      name: '',
      selling_price: 0,
      quantity: 0,
      gst_rate: 0,
      hsn_code: '',
    } as ProductCreate,
  }))

  function openNew() {
    setEditingId(null)
    form.reset()
    setShowModal(true)
  }

  function openEdit(id: string) {
    const s = stockQuery.data?.find((x) => x.product_id === id)
    if (!s) return
    setEditingId(id)
    form.setFieldValue('name', s.name)
    form.setFieldValue('selling_price', Number(s.selling_price))
    form.setFieldValue('quantity', s.quantity)
    form.setFieldValue('gst_rate', Number(s.gst_rate))
    form.setFieldValue('hsn_code', s.hsn_code)
    setShowModal(true)
  }

  function handleSave() {
    const vals = form.state.values
    if (!vals.name.trim()) return
    if (editingId()) {
      updateStock.mutateAsync({
        name: vals.name.trim(),
        selling_price: vals.selling_price,
        quantity: vals.quantity,
        gst_rate: vals.gst_rate,
        hsn_code: vals.hsn_code,
        product_id: editingId()!,
      }).then((res) => {
        const idx = stockList.findIndex((s) => s.product_id === editingId())
        if (idx !== -1) setStockList(idx, res)
        persistState()
      })
    } else {
      createStock.mutateAsync({
        name: vals.name.trim(),
        selling_price: vals.selling_price,
        quantity: vals.quantity,
        gst_rate: vals.gst_rate,
        hsn_code: vals.hsn_code,
      }).then((res) => {
        setStockList(stockList.length, res)
        persistState()
      })
    }
    setShowModal(false)
  }

  function handleDelete(id: string) {
    if (!confirm('Delete this item?')) return
    deleteStock.mutateAsync(id).then(() => {
      setStockList(stockList.filter((s) => s.product_id !== id))
      persistState()
    })
  }

  const totalValue = (s: ProductResponse) => s.quantity * Number(s.selling_price)

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
        <Show when={stockQuery.isLoading}>
          <div class="px-4 py-8 text-center text-gray-500">Loading stock...</div>
        </Show>
        <Show when={stockQuery.isError}>
          <div class="px-4 py-8 text-center text-red-600">
            Failed to load stock: {stockQuery.error?.message}
          </div>
        </Show>
        <Show when={stockQuery.isSuccess}>
          <div class="px-4 py-2 text-sm text-blue-700 bg-blue-50 border border-blue-200 rounded mx-3 mb-2">
            <strong>Tip:</strong> Click Edit to modify a stock item.
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
                <tr>
                  <th class="py-3 pl-4 text-left" style="width:50px">#</th>
                  <th class="py-3 text-left">Name</th>
                  <th class="py-3 text-right">Quantity</th>
                  <th class="py-3 text-right">Selling Price (₹)</th>
                  <th class="py-3 text-right">GST Rate (%)</th>
                  <th class="py-3 text-left">HSN Code</th>
                  <th class="py-3 text-right">Total Value (₹)</th>
                  <th class="py-3 pr-4 text-center" style="width:120px">Actions</th>
                </tr>
              </thead>
              <tbody>
                <For each={stockQuery.data}>
                  {(s, i) => (
                    <tr class="border-b border-gray-200 hover:bg-gray-50">
                      <td class="py-3 pl-4">{i() + 1}</td>
                      <td class="py-3 font-medium">{s.name}</td>
                      <td class="py-3 text-right">{s.quantity}</td>
                      <td class="py-3 text-right">₹{formatMoney(Number(s.selling_price))}</td>
                      <td class="py-3 text-right">{s.gst_rate}%</td>
                      <td class="py-3">{s.hsn_code || '-'}</td>
                      <td class="py-3 text-right font-bold">₹{formatMoney(totalValue(s))}</td>
                      <td class="py-3 pr-4 text-center">
                        <button
                          onClick={() => openEdit(s.product_id)}
                          class="text-blue-600 hover:text-blue-800 underline text-xs mr-2"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(s.product_id)}
                          class="text-red-600 hover:text-red-800 underline text-xs"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  )}
                </For>
                <For each={(!stockQuery.data || stockQuery.data.length === 0) ? [true] : []}>
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
        </Show>
      </div>

      <Show when={showModal()}>
        <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40" onClick={() => setShowModal(false)}>
          <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4" onClick={(e) => e.stopPropagation()}>
            <div class="px-4 py-3 border-b border-gray-200">
              <h5 class="mb-0 font-bold text-gray-700">{editingId() !== null ? 'Edit Stock' : 'Stock Details'}</h5>
            </div>
            <div class="p-4">
              <form.Field name="name">
                {(field) => {
                  const f = field()
                  return (
                    <div class="mb-3">
                      <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
                      <input
                        type="text"
                        value={f.state.value}
                        onInput={(e) => f.handleChange(e.currentTarget.value)}
                        class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                        required
                      />
                    </div>
                  )
                }}
              </form.Field>
              <div class="flex gap-3">
                <form.Field name="selling_price">
                  {(field) => {
                    const f = field()
                    return (
                      <div class="w-1/3 mb-3">
                        <label class="block text-sm font-medium text-gray-700 mb-1">Selling Price</label>
                        <input
                          type="number"
                          step="0.01"
                          min="0"
                          value={f.state.value}
                          onInput={(e) => f.handleChange(parseFloat(e.currentTarget.value) || 0)}
                          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                          required
                        />
                      </div>
                    )
                  }}
                </form.Field>
                <form.Field name="quantity">
                  {(field) => {
                    const f = field()
                    return (
                      <div class="w-1/3 mb-3">
                        <label class="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                        <input
                          type="number"
                          min="0"
                          value={f.state.value}
                          onInput={(e) => f.handleChange(parseInt(e.currentTarget.value) || 0)}
                          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                          required
                        />
                      </div>
                    )
                  }}
                </form.Field>
                <form.Field name="gst_rate">
                  {(field) => {
                    const f = field()
                    return (
                      <div class="w-1/3 mb-3">
                        <label class="block text-sm font-medium text-gray-700 mb-1">GST Rate (%)</label>
                        <input
                          type="number"
                          step="0.01"
                          min="0"
                          value={f.state.value}
                          onInput={(e) => f.handleChange(parseFloat(e.currentTarget.value) || 0)}
                          class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                        />
                      </div>
                    )
                  }}
                </form.Field>
              </div>
              <form.Field name="hsn_code">
                {(field) => {
                  const f = field()
                  return (
                    <div class="mb-3">
                      <label class="block text-sm font-medium text-gray-700 mb-1">HSN Code</label>
                      <input
                        type="text"
                        value={f.state.value}
                        onInput={(e) => f.handleChange(e.currentTarget.value)}
                        class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                        placeholder="Optional"
                      />
                    </div>
                  )
                }}
              </form.Field>
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
