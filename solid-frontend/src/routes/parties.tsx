import { createSignal, For, Show } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import { partyList, setPartyList, indianStates, formatMoney, getNextId } from '../lib/store'

export const Route = createFileRoute('/parties')({ component: Parties })

function Parties() {
  const [showModal, setShowModal] = createSignal(false)
  const [editingId, setEditingId] = createSignal<number | null>(null)
  const [form, setForm] = createSignal({
    name: '',
    phone: '',
    state: '',
    address: '',
    balance: 0,
    type: 'Receive' as 'Receive' | 'Pay',
  })

  function openNew() {
    setEditingId(null)
    setForm({ name: '', phone: '', state: '', address: '', balance: 0, type: 'Receive' })
    setShowModal(true)
  }

  function openEdit(id: number) {
    const p = partyList.find((x) => x.id === id)
    if (!p) return
    setEditingId(id)
    setForm({ name: p.name, phone: p.phone, state: p.state, address: p.address, balance: p.balance, type: p.type })
    setShowModal(true)
  }

  function handleSave() {
    const f = form()
    if (!f.name.trim()) return
    if (editingId()) {
      setPartyList(
        (p) => p.id === editingId(),
        'name',
        f.name.trim()
      )
      setPartyList(
        (p) => p.id === editingId(),
        'phone',
        f.phone
      )
      setPartyList(
        (p) => p.id === editingId(),
        'state',
        f.state
      )
      setPartyList(
        (p) => p.id === editingId(),
        'address',
        f.address
      )
      setPartyList(
        (p) => p.id === editingId(),
        'balance',
        f.balance
      )
      setPartyList((p) => p.id === editingId(), 'type', f.type)
    } else {
      setPartyList(partyList.length, {
        id: getNextId(),
        name: f.name.trim(),
        phone: f.phone,
        state: f.state,
        address: f.address,
        balance: f.balance,
        type: f.type,
      })
    }
    setShowModal(false)
  }

  function handleDelete(id: number) {
    if (!confirm('Delete this party?')) return
    setPartyList(partyList.filter((p) => p.id !== id))
  }

  return (
    <div class="space-y-6">
      <div class="border-0 shadow-sm rounded-lg overflow-hidden">
        <div class="bg-white px-4 py-3 flex items-center justify-between">
          <h5 class="mb-0 font-bold text-gray-700">Parties (Debtors & Creditors)</h5>
          <button
            onClick={openNew}
            class="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-3 py-1.5 rounded transition-colors"
          >
            + Add Party
          </button>
        </div>
        <div class="px-4 py-2 text-sm text-blue-700 bg-blue-50 border border-blue-200 rounded mx-3 mb-2">
          <strong>Tip:</strong> Click Edit to modify a party.
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th class="py-3 pl-4 text-left" style="width:50px">#</th>
                <th class="py-3 text-left">Name</th>
                <th class="py-3 text-left">Phone</th>
                <th class="py-3 text-left">State</th>
                <th class="py-3 text-left">Type</th>
                <th class="py-3 text-right">Balance (₹)</th>
                <th class="py-3 pr-4 text-center" style="width:120px">Actions</th>
              </tr>
            </thead>
            <tbody>
              <For each={partyList}>
                {(p, i) => (
                  <tr class="border-b border-gray-200 hover:bg-gray-50">
                    <td class="py-3 pl-4">{i() + 1}</td>
                    <td class="py-3 font-medium">{p.name}</td>
                    <td class="py-3">{p.phone || '-'}</td>
                    <td class="py-3">{p.state || '-'}</td>
                    <td class="py-3">
                      <Show
                        when={p.type === 'Receive'}
                        fallback={
                          <span class="inline-block px-2 py-0.5 rounded text-xs font-bold text-red-700 bg-red-100">
                            Pay (Creditor)
                          </span>
                        }
                      >
                        <span class="inline-block px-2 py-0.5 rounded text-xs font-bold text-green-700 bg-green-100">
                          Receive (Debtor)
                        </span>
                      </Show>
                    </td>
                    <td class="py-3 text-right font-bold">₹{formatMoney(p.balance)}</td>
                    <td class="py-3 pr-4 text-center">
                      <button
                        onClick={() => openEdit(p.id)}
                        class="text-blue-600 hover:text-blue-800 underline text-xs mr-2"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(p.id)}
                        class="text-red-600 hover:text-red-800 underline text-xs"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                )}
              </For>
              <For each={partyList.length === 0 ? [true] : []}>
                {() => (
                  <tr>
                    <td colspan="7" class="text-center text-gray-500 py-8">
                      No parties added yet.
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
              <h5 class="mb-0 font-bold text-gray-700">{editingId() !== null ? 'Edit Party' : 'Party Details'}</h5>
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
              <div class="flex gap-3">
                <div class="w-1/2 mb-3">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    type="text"
                    value={form().phone}
                    onInput={(e) => setForm((prev) => ({ ...prev, phone: e.currentTarget.value.replace(/[^0-9]/g, '') }))}
                    class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                    maxLength={10}
                  />
                </div>
                <div class="w-1/2 mb-3">
                  <label class="block text-sm font-medium text-gray-700 mb-1">State</label>
                  <select
                    value={form().state}
                    onChange={(e) => setForm((prev) => ({ ...prev, state: e.currentTarget.value }))}
                    class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  >
                    <For each={indianStates}>
                      {(s) => <option value={s === 'Select State' ? '' : s}>{s}</option>}
                    </For>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <input
                  type="text"
                  value={form().address}
                  onInput={(e) => setForm((prev) => ({ ...prev, address: e.currentTarget.value }))}
                  class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                />
              </div>
              <div class="flex gap-3">
                <div class="w-1/2 mb-3">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Opening Balance (₹)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={form().balance}
                    onInput={(e) => setForm((prev) => ({ ...prev, balance: parseFloat(e.currentTarget.value) || 0 }))}
                    class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                    required
                  />
                </div>
                <div class="w-1/2 mb-3 flex items-end pb-1">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
                    <div class="flex gap-4">
                      <label class="flex items-center gap-1 text-sm cursor-pointer">
                        <input
                          type="radio"
                          name="pt_type"
                          checked={form().type === 'Receive'}
                          onChange={() => setForm((prev) => ({ ...prev, type: 'Receive' }))}
                          class="accent-green-600"
                        />
                        <span class="text-green-600 font-medium">Receive</span>
                      </label>
                      <label class="flex items-center gap-1 text-sm cursor-pointer">
                        <input
                          type="radio"
                          name="pt_type"
                          checked={form().type === 'Pay'}
                          onChange={() => setForm((prev) => ({ ...prev, type: 'Pay' }))}
                          class="accent-red-600"
                        />
                        <span class="text-red-600 font-medium">Pay</span>
                      </label>
                    </div>
                  </div>
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
                  {editingId() !== null ? 'Update Party' : 'Save Party'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Show>
    </div>
  )
}
