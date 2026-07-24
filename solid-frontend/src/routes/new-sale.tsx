import { createSignal, createMemo, For, Show, onMount } from 'solid-js'
import { createFileRoute, Link, useNavigate } from '@tanstack/solid-router'
import {
  transactions, setTransactions,
  partyList, setPartyList,
  stockList, setStockList,
  companyData,
  formatMoney, generateInvoiceNo,
  updateLedger, deleteLedgerByRef, persistState,
  indianStates,
} from '../lib/store'
import type { SaleItem } from '../lib/types'

interface SaleRow {
  key: number
  itemId: string
  qty: number
  price: number
  discPerc: number
  discAmt: number
  taxPerc: number
}

function emptyRow(): SaleRow {
  return { key: Date.now() + Math.random(), itemId: '', qty: 1, price: 0, discPerc: 0, discAmt: 0, taxPerc: 0 }
}

export const Route = createFileRoute('/new-sale')({
  validateSearch: (search: Record<string, string | undefined>) => ({
    edit: search.edit ? Number(search.edit) : undefined,
  }),
  component: NewSale,
})

function NewSale() {
  const navigate = useNavigate()
  const search = Route.useSearch()

  const [mode, setMode] = createSignal<'Credit' | 'Cash'>('Credit')
  const [customerId, setCustomerId] = createSignal('')
  const [phone, setPhone] = createSignal('')
  const [address, setAddress] = createSignal('')
  const [custState, setCustState] = createSignal('')
  const [invNo, setInvNo] = createSignal(generateInvoiceNo())
  const [date, setDate] = createSignal(new Date().toISOString().split('T')[0])
  const [dueDate, setDueDate] = createSignal('')
  const [roundOff, setRoundOff] = createSignal(false)
  const [paid, setPaid] = createSignal(0)
  const [terms, setTerms] = createSignal('Goods once sold will not be taken back.')
  const [rows, setRows] = createSignal<SaleRow[]>([emptyRow()])
  const [editingId, setEditingId] = createSignal<number | null>(null)
  const [priceType, setPriceType] = createSignal<'Without Tax' | 'With Tax'>('Without Tax')
  const [saving, setSaving] = createSignal(false)

  const customer = createMemo(() => partyList.find((p) => String(p.id) === String(customerId())))

  function selectCustomer(id: string) {
    setCustomerId(id)
    const p = partyList.find((x) => String(x.id) === String(id))
    if (p) {
      if (!editingId()) {
        setPhone(p.phone || '')
        setAddress(p.address || '')
        setCustState(p.state || '')
      }
    } else {
      if (!editingId()) {
        setPhone('')
        setAddress('')
        setCustState('')
      }
    }
  }

  const sortedStock = createMemo(() => [...stockList].sort((a, b) => a.name.localeCompare(b.name)))

  const itemTotals = createMemo(() =>
    rows().map((row) => {
      const gross = row.qty * row.price
      const discAmt = row.discAmt
      const taxable = Math.max(0, gross - discAmt)
      let taxAmt: number
      let baseTaxable = taxable
      if (priceType() === 'With Tax') {
        const base = taxable / (1 + row.taxPerc / 100)
        taxAmt = taxable - base
        baseTaxable = base
      } else {
        taxAmt = taxable * (row.taxPerc / 100)
      }
      return { gross, discAmt, taxable: baseTaxable, taxAmt, rowTotal: baseTaxable + taxAmt }
    }),
  )

  const grandTotal = createMemo(() => {
    let total = itemTotals().reduce((sum, it) => sum + it.rowTotal, 0)
    if (roundOff()) total = Math.round(total)
    return total
  })

  const balance = createMemo(() => {
    if (mode() === 'Cash') return 0
    return Math.max(0, grandTotal() - paid())
  })

  const isInterstate = createMemo(() => {
    const coState = companyData.state
    const cs = custState()
    return !!(coState && cs && coState !== cs)
  })

  function addRow() {
    setRows([...rows(), emptyRow()])
  }

  function removeRow(idx: number) {
    const r = rows()
    if (r.length <= 1) return
    setRows(r.filter((_, i) => i !== idx))
  }

  function updateRow(idx: number, patch: Partial<SaleRow>) {
    setRows(rows().map((r, i) => (i === idx ? { ...r, ...patch } : r)))
  }

  function onItemSelect(idx: number, itemId: string) {
    const st = stockList.find((s) => String(s.id) === String(itemId))
    const patch: Partial<SaleRow> = { itemId }
    if (st) {
      patch.price = st.price
    }
    updateRow(idx, patch)
  }

  function onDiscPercChange(idx: number, perc: number) {
    const row = rows()[idx]
    const gross = row.qty * row.price
    const discAmt = gross * (perc / 100)
    updateRow(idx, { discPerc: perc, discAmt })
  }

  function onDiscAmtChange(idx: number, amt: number) {
    const row = rows()[idx]
    const gross = row.qty * row.price
    const discPerc = gross > 0 ? (amt / gross) * 100 : 0
    updateRow(idx, { discAmt: amt, discPerc })
  }

  function setPaidAmount(val: number) {
    if (mode() === 'Credit') {
      setPaid(val)
    }
  }

  function setModeWithReset(m: 'Credit' | 'Cash') {
    setMode(m)
    if (m === 'Cash') {
      setPaid(grandTotal())
      setDueDate('')
    }
  }

  function handleSave() {
    if (saving()) return
    setSaving(true)

    for (const row of rows()) {
      if (!row.itemId) continue
      const st = stockList.find((s) => String(s.id) === String(row.itemId))
      if (st) {
        let available = st.qty
        if (editingId()) {
          const oldT = transactions.find((t) => t.id === editingId())
          if (oldT?.sale_details) {
            const oldItem = oldT.sale_details.items.find((it) => it.item_id === row.itemId)
            if (oldItem) available += oldItem.qty
          }
        }
        if (available < row.qty) {
          alert(`Insufficient stock for ${st.name}. Available: ${available}`)
          setSaving(false)
          return
        }
      }
    }

    if (grandTotal() <= 0) {
      alert('Total amount cannot be zero.')
      setSaving(false)
      return
    }

    if (mode() === 'Credit' && !customerId()) {
      alert('Credit sale requires a customer to be selected.')
      setSaving(false)
      return
    }

    const total = grandTotal()
    const paidAmt = mode() === 'Cash' ? total : paid()
    const bal = mode() === 'Cash' ? 0 : Math.max(0, total - paidAmt)
    const paymentStatus = bal === 0 ? 'Paid' : paidAmt > 0 ? 'Partial' : 'Unpaid'
    const custId = customerId()
    const custName = customer()?.name || 'Walk-in'

    const editId = editingId()
    if (editId) {
      const oldT = transactions.find((t) => t.id === editId)
      if (oldT && oldT.sale_details) {
        const sd = oldT.sale_details
        if (oldT.payment_mode === 'Credit' && sd.customer_id) {
          const oldParty = partyList.find((p) => String(p.id) === String(sd.customer_id))
          if (oldParty) {
            let signedBal = (oldParty.type === 'Receive' ? 1 : -1) * oldParty.balance
            signedBal -= sd.balance_amount
            setPartyList(
              (p) => String(p.id) === String(oldParty.id),
              'balance',
              Math.abs(signedBal),
            )
            setPartyList(
              (p) => String(p.id) === String(oldParty.id),
              'type',
              signedBal >= 0 ? 'Receive' : 'Pay',
            )
          }
        }
        for (const oldItem of sd.items) {
          const st = stockList.find((s) => String(s.id) === String(oldItem.item_id))
          if (st) {
            const idx = stockList.indexOf(st)
            if (idx !== -1) setStockList(idx, 'qty', st.qty + oldItem.qty)
          }
        }
      }
      deleteLedgerByRef(editId)
      setTransactions((prev) => prev.filter((t) => t.id !== editId))
    }

    if (custId) {
      const p = partyList.find((x) => String(x.id) === String(custId))
      if (p) {
        const idx = partyList.indexOf(p)
        setPartyList(idx, 'phone', phone())
        setPartyList(idx, 'address', address())
      }
    }

    const itemsData: SaleItem[] = []
    for (let i = 0; i < rows().length; i++) {
      const row = rows()[i]
      if (!row.itemId) continue
      const tot = itemTotals()[i]
      const st = stockList.find((s) => String(s.id) === String(row.itemId))
      if (st) {
        const stkIdx = stockList.indexOf(st)
        if (stkIdx !== -1) setStockList(stkIdx, 'qty', st.qty - row.qty)
      }
      itemsData.push({
        item_id: row.itemId,
        name: stockList.find((s) => String(s.id) === String(row.itemId))?.name || '',
        qty: row.qty,
        unit: stockList.find((s) => String(s.id) === String(row.itemId))?.unit || '',
        price: row.price,
        disc_perc: row.discPerc,
        disc_amt: row.discAmt,
        tax_perc: row.taxPerc,
        tax_amt: tot.taxAmt,
        total: tot.rowTotal,
      })
    }

    if (custId && mode() === 'Credit') {
      const p = partyList.find((x) => String(x.id) === String(custId))
      if (p) {
        const pIdx = partyList.indexOf(p)
        let signedBal = (p.type === 'Receive' ? 1 : -1) * p.balance
        signedBal += bal
        setPartyList(pIdx, 'balance', Math.abs(signedBal))
        setPartyList(pIdx, 'type', signedBal >= 0 ? 'Receive' : 'Pay')
      }
    }

    const id = editingId() || Date.now()
    const t = {
      id,
      date: date(),
      particulars: `${invNo()} - Sale to ${custName}`,
      type: 'Sale' as const,
      payment_mode: mode() === 'Credit' ? 'Credit' as const : 'Cash' as const,
      amount: total,
      sale_details: {
        customer_id: custId || '',
        invoice_no: invNo(),
        phone: phone(),
        address: address(),
        state_of_supply: custState(),
        due_date: dueDate(),
        items: itemsData,
        paid_amount: paidAmt,
        balance_amount: bal,
        payment_status: paymentStatus as 'Paid' | 'Partial' | 'Unpaid',
        is_roundoff: roundOff(),
        price_type: priceType(),
        terms: terms(),
      },
    }

    setTransactions(transactions.length, t)

    if (mode() === 'Credit' && custId) {
      updateLedger(date(), custId, 'DR', total, id, 'Sales: ' + invNo())
      updateLedger(date(), 'Sales', 'CR', total, id, 'Sales to ' + custName)
      if (paidAmt > 0) {
        updateLedger(date(), 'Cash', 'DR', paidAmt, id, 'Receipt against ' + invNo())
        updateLedger(date(), custId, 'CR', paidAmt, id, 'Payment Receipt')
      }
    } else {
      updateLedger(date(), 'Cash', 'DR', total, id, 'Cash Sales: ' + invNo())
      updateLedger(date(), 'Sales', 'CR', total, id, 'Cash Sales')
    }

    persistState()
    navigate({ to: '/sales' })
  }

  onMount(() => {
    const editId = search().edit
    if (editId) {
      const t = transactions.find((x) => x.id === editId)
      if (t?.sale_details) {
        const d = t.sale_details
        setEditingId(editId)
        setMode(t.payment_mode === 'Credit' ? 'Credit' : 'Cash')
        selectCustomer(d.customer_id || '')
        setPhone(d.phone || '')
        setAddress(d.address || '')
        setCustState(d.state_of_supply || '')
        setInvNo(d.invoice_no)
        setDate(t.date)
        setDueDate(d.due_date || '')
        setRoundOff(!!d.is_roundoff)
        setPaid(d.paid_amount || 0)
        setTerms(d.terms || '')
        setPriceType((d.price_type as 'Without Tax' | 'With Tax') || 'Without Tax')
        if (d.items.length > 0) {
          setRows(
            d.items.map((it) => ({
              key: Date.now() + Math.random(),
              itemId: it.item_id,
              qty: it.qty,
              price: it.price,
              discPerc: it.disc_perc,
              discAmt: it.disc_amt,
              taxPerc: it.tax_perc,
            })),
          )
        }
      }
    }
  })

  return (
    <div class="space-y-4">
      <div class="flex items-center gap-3">
        <Link
          to="/sales"
          class="inline-flex items-center justify-center w-9 h-9 rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-gray-100 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </Link>
        <h4 class="font-bold mb-0">{editingId() ? 'Edit Sale' : 'New Sale'}</h4>
      </div>

      <div class="flex gap-6">
        <div class="w-[58%] space-y-4">
          <div class="bg-white rounded-xl shadow-sm border-0 p-4">
            <div class="flex items-center justify-between mb-4">
              <div class="flex gap-2">
                <button
                  class={`px-4 py-1.5 rounded-lg text-sm font-bold transition-colors cursor-pointer ${mode() === 'Credit' ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-600'}`}
                  onClick={() => setModeWithReset('Credit')}
                >
                  Credit
                </button>
                <button
                  class={`px-4 py-1.5 rounded-lg text-sm font-bold transition-colors cursor-pointer ${mode() === 'Cash' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-600'}`}
                  onClick={() => setModeWithReset('Cash')}
                >
                  Cash
                </button>
              </div>
              <div class="flex items-center gap-2">
                <label class="text-xs text-gray-500 font-bold">Price Type</label>
                <select
                  class="border border-gray-300 rounded px-2 py-1 text-sm"
                  value={priceType()}
                  onChange={(e) => setPriceType(e.currentTarget.value as 'Without Tax' | 'With Tax')}
                >
                  <option value="Without Tax">Without Tax</option>
                  <option value="With Tax">With Tax</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label class="block text-xs text-gray-500 font-bold mb-1">Customer</label>
                <div class="flex gap-1">
                  <select
                    class="flex-1 border border-gray-300 rounded px-2 py-1.5 text-sm"
                    value={customerId()}
                    onChange={(e) => selectCustomer(e.currentTarget.value)}
                  >
                    <option value="">Walk-in Customer</option>
                    <For each={partyList}>
                      {(p) => <option value={p.id}>{p.name}</option>}
                    </For>
                  </select>
                </div>
                <Show when={customer()}>
                  <div class="mt-1 text-xs">
                    {customer()!.type === 'Receive' ? (
                      <span class="text-green-600">Balance: ₹{formatMoney(customer()!.balance)} (To Receive)</span>
                    ) : (
                      <span class="text-red-600">Balance: ₹{formatMoney(customer()!.balance)} (To Pay)</span>
                    )}
                  </div>
                </Show>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs text-gray-500 font-bold mb-1">Invoice No</label>
                  <input
                    type="text"
                    class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm font-bold"
                    value={invNo()}
                    onInput={(e) => setInvNo(e.currentTarget.value)}
                  />
                </div>
                <div>
                  <label class="block text-xs text-gray-500 font-bold mb-1">Date</label>
                  <input
                    type="date"
                    class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                    value={date()}
                    onInput={(e) => setDate(e.currentTarget.value)}
                  />
                </div>
              </div>
              <div>
                <label class="block text-xs text-gray-500 font-bold mb-1">Phone</label>
                <input
                  type="text"
                  class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                  value={phone()}
                  onInput={(e) => setPhone(e.currentTarget.value)}
                />
              </div>
              <div>
                <label class="block text-xs text-gray-500 font-bold mb-1">State of Supply</label>
                <select
                  class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                  value={custState()}
                  onChange={(e) => setCustState(e.currentTarget.value)}
                >
                  <option value="">Select State</option>
                  <For each={indianStates.filter((s) => s !== 'Select State')}>
                    {(s) => <option value={s}>{s}</option>}
                  </For>
                </select>
              </div>
              <div class="col-span-2">
                <label class="block text-xs text-gray-500 font-bold mb-1">Address</label>
                <input
                  type="text"
                  class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                  value={address()}
                  onInput={(e) => setAddress(e.currentTarget.value)}
                />
              </div>
              <Show when={mode() === 'Credit'}>
                <div>
                  <label class="block text-xs text-gray-500 font-bold mb-1">Due Date</label>
                  <input
                    type="date"
                    class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                    value={dueDate()}
                    onInput={(e) => setDueDate(e.currentTarget.value)}
                  />
                </div>
              </Show>
            </div>

            <div>
              <div class="flex items-center justify-between mb-2">
                <h6 class="font-bold text-sm mb-0">Invoice Items</h6>
                <button
                  onClick={addRow}
                  class="border border-blue-600 text-blue-600 text-xs px-3 py-1 rounded font-bold hover:bg-blue-600 hover:text-white transition-colors cursor-pointer"
                >
                  + Add Row
                </button>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-sm">
                  <thead class="bg-gray-100 text-gray-500 uppercase text-[0.65rem]">
                    <tr>
                      <th class="p-1.5 text-left" style="width:30px">#</th>
                      <th class="p-1.5 text-left" style="width:160px">Item</th>
                      <th class="p-1.5 text-center" style="width:50px">Qty</th>
                      <th class="p-1.5 text-center" style="width:40px">Unit</th>
                      <th class="p-1.5 text-right" style="width:80px">Price</th>
                      <th class="p-1.5 text-right" style="width:60px">Disc %</th>
                      <th class="p-1.5 text-right" style="width:65px">Disc Amt</th>
                      <th class="p-1.5 text-center" style="width:55px">Tax %</th>
                      <th class="p-1.5 text-right" style="width:80px">Total</th>
                      <th class="p-1.5 text-center" style="width:28px"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <For each={rows()}>
                      {(row, idx) => {
                        const st = stockList.find((s) => String(s.id) === String(row.itemId))
                        const badge = st ? { qty: st.qty, unit: st.unit || '' } : null
                        const tot = itemTotals()[idx()]
                        return (
                          <tr class="border-b border-gray-100 align-top">
                            <td class="p-1 text-center text-muted font-bold text-xs pt-2.5">{idx() + 1}</td>
                            <td class="p-1">
                              <select
                                class="w-full border border-gray-300 rounded px-1.5 py-1 text-xs"
                                value={row.itemId}
                                onChange={(e) => onItemSelect(idx(), e.currentTarget.value)}
                              >
                                <option value="">Select Item</option>
                                <For each={sortedStock()}>
                                  {(s) => (
                                    <option value={s.id}>
                                      {s.name} (Stock: {s.qty})
                                    </option>
                                  )}
                                </For>
                              </select>
                              <Show when={badge}>
                                <div class="mt-0.5">
                                  <span
                                    class={`inline-block text-[0.6rem] px-1.5 py-0.5 rounded font-bold ${
                                      badge!.qty <= 0
                                        ? 'bg-red-100 text-red-700'
                                        : 'bg-green-100 text-green-700'
                                    }`}
                                  >
                                    Stock: {badge!.qty} {badge!.unit}
                                  </span>
                                </div>
                              </Show>
                            </td>
                            <td class="p-1">
                              <input
                                type="number"
                                class="w-full border border-gray-300 rounded px-1.5 py-1 text-xs text-center"
                                value={row.qty}
                                min="1"
                                onInput={(e) => updateRow(idx(), { qty: parseInt(e.currentTarget.value) || 0 })}
                              />
                            </td>
                            <td class="p-1 text-center text-xs pt-2.5 text-gray-500">
                              {st?.unit || '-'}
                            </td>
                            <td class="p-1">
                              <input
                                type="number"
                                class="w-full border border-gray-300 rounded px-1.5 py-1 text-xs text-right"
                                value={row.price}
                                step="0.01"
                                onInput={(e) => updateRow(idx(), { price: parseFloat(e.currentTarget.value) || 0 })}
                              />
                            </td>
                            <td class="p-1">
                              <input
                                type="number"
                                class="w-full border border-gray-300 rounded px-1.5 py-1 text-xs text-right"
                                value={row.discPerc}
                                step="0.01"
                                onInput={(e) => onDiscPercChange(idx(), parseFloat(e.currentTarget.value) || 0)}
                              />
                            </td>
                            <td class="p-1">
                              <input
                                type="number"
                                class="w-full border border-gray-300 rounded px-1.5 py-1 text-xs text-right"
                                value={row.discAmt}
                                step="0.01"
                                onInput={(e) => onDiscAmtChange(idx(), parseFloat(e.currentTarget.value) || 0)}
                              />
                            </td>
                            <td class="p-1">
                              <select
                                class="w-full border border-gray-300 rounded px-1.5 py-1 text-xs"
                                value={row.taxPerc}
                                onChange={(e) => updateRow(idx(), { taxPerc: parseFloat(e.currentTarget.value) || 0 })}
                              >
                                <option value="0">0%</option>
                                <option value="5">5%</option>
                                <option value="12">12%</option>
                                <option value="18">18%</option>
                                <option value="28">28%</option>
                              </select>
                            </td>
                            <td class="p-1 text-right font-bold text-xs pt-2.5">
                              ₹{formatMoney(tot.rowTotal)}
                            </td>
                            <td class="p-1 text-center pt-2">
                              <button
                                onClick={() => removeRow(idx())}
                                class="text-red-500 hover:text-red-700 cursor-pointer text-xs"
                              >
                                <svg class="w-3.5 h-3.5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                              </button>
                            </td>
                          </tr>
                        )
                      }}
                    </For>
                    <For each={rows().length === 0 ? [true] : []}>
                      {() => (
                        <tr>
                          <td colspan="10" class="text-center text-gray-400 py-6 text-xs">
                            No items added. Click "+ Add Row" to add items.
                          </td>
                        </tr>
                      )}
                    </For>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm border-0 p-4">
            <div class="flex justify-between items-center">
              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input
                    type="checkbox"
                    checked={roundOff()}
                    onChange={(e) => setRoundOff(e.currentTarget.checked)}
                    class="accent-blue-600"
                  />
                  <span class="text-gray-700">Round off to nearest integer</span>
                </label>
              </div>
              <div class="text-right">
                <div class="flex items-center gap-4">
                  <Show when={mode() === 'Credit'}>
                    <div>
                      <label class="block text-xs text-gray-500 font-bold mb-1">Paid Amount (₹)</label>
                      <input
                        type="number"
                        class="w-32 border border-gray-300 rounded px-2 py-1.5 text-sm text-right"
                        value={paid()}
                        step="0.01"
                        onInput={(e) => setPaidAmount(parseFloat(e.currentTarget.value) || 0)}
                      />
                    </div>
                  </Show>
                  <div>
                    <label class="block text-xs text-gray-500 font-bold mb-1">Grand Total</label>
                    <h3 class="mb-0 font-bold text-blue-600 text-2xl">₹{formatMoney(grandTotal())}</h3>
                  </div>
                  <Show when={mode() === 'Credit'}>
                    <div>
                      <label class="block text-xs text-gray-500 font-bold mb-1">Balance</label>
                      <h4 class={`mb-0 font-bold text-lg ${balance() > 0 ? 'text-red-500' : 'text-green-600'}`}>
                        ₹{formatMoney(balance())}
                      </h4>
                    </div>
                  </Show>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm border-0 p-4">
            <label class="block text-xs text-gray-500 font-bold mb-1 uppercase">Terms & Conditions</label>
            <textarea
              class="w-full border border-gray-300 rounded px-3 py-2 text-sm"
              rows="2"
              value={terms()}
              onInput={(e) => setTerms(e.currentTarget.value)}
            />
            <div class="flex justify-end gap-3 mt-3">
              <Link
                to="/sales"
                class="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-bold"
              >
                Cancel
              </Link>
              <button
                onClick={handleSave}
                disabled={saving()}
                class="px-6 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-bold disabled:opacity-50 cursor-pointer"
              >
                {saving() ? 'Saving...' : editingId() ? 'Update Sale' : 'Save Sale'}
              </button>
            </div>
          </div>
        </div>

        <div class="flex-1">
          <div class="bg-white rounded-xl shadow-sm border-0 p-5 sticky top-4">
            <div id="invoice-preview">
              <Show
                when={rows().some((r) => r.itemId)}
                fallback={
                  <div class="text-center text-gray-400 py-16 text-sm">
                    Add items to generate invoice preview
                  </div>
                }
              >
                <div class="border-bottom pb-4 mb-4" style="border-bottom: 1px solid #e5e7eb;">
                  <div class="d-flex justify-between align-items-start" style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="display: flex; gap: 0.75rem;">
                      <Show when={companyData.logo}>
                        <div>
                          <img src={companyData.logo} style="height: 60px; object-fit: contain;" />
                        </div>
                      </Show>
                      <div>
                        <h2 class="fw-bold mb-0 text-primary" style="font-weight: 700; margin-bottom: 0; color: #0d6efd;">
                          {companyData.name || 'PRINTOS'}
                        </h2>
                        <p class="text-muted m-0 small" style="color: #6c757d; margin: 0; font-size: 0.8rem;">
                          {companyData.address || '-'}
                        </p>
                        <p class="text-muted m-0 small" style="color: #6c757d; margin: 0; font-size: 0.8rem;">
                          Phone: {companyData.phone || '-'} | Email: {companyData.email || '-'}
                        </p>
                        <p class="text-muted m-0 small fw-bold" style="color: #6c757d; margin: 0; font-size: 0.8rem; font-weight: 700;">
                          GSTIN: {companyData.gstin || '-'}
                        </p>
                      </div>
                    </div>
                    <div class="text-end" style="text-align: right;">
                      <h1 class="fw-bold text-primary" style="font-weight: 700; color: #0d6efd; font-size: 1.5rem; margin-bottom: 0;">
                        {mode() === 'Credit' ? 'CREDIT INVOICE' : 'CASH INVOICE'}
                      </h1>
                      <p class="m-0 text-muted small" style="margin: 0; color: #6c757d; font-size: 0.75rem;">
                        Original for Recipient
                      </p>
                    </div>
                  </div>
                </div>

                <div style="display: flex; margin-bottom: 1rem;">
                  <div style="flex: 1;">
                    <p class="text-muted text-uppercase mb-1 small fw-bold" style="color: #6c757d; text-transform: uppercase; margin-bottom: 0.25rem; font-size: 0.75rem; font-weight: 700;">
                      Bill To:
                    </p>
                    <h5 class="fw-bold mb-1" style="font-weight: 700; margin-bottom: 0.25rem;">
                      {customer()?.name || 'Walk-in Customer'}
                    </h5>
                    <p class="m-0 text-muted small" style="margin: 0; color: #6c757d; font-size: 0.75rem;">
                      {address() || '-'}
                    </p>
                    <p class="m-0 text-muted small" style="margin: 0; color: #6c757d; font-size: 0.75rem;">
                      Phone: {phone() || '-'}
                    </p>
                    <p class="m-0 text-muted small" style="margin: 0; color: #6c757d; font-size: 0.75rem;">
                      State: {custState() || '-'}
                    </p>
                  </div>
                  <div class="text-end" style="text-align: right;">
                    <p class="small" style="font-size: 0.8rem; margin-bottom: 0.25rem;">
                      <strong>Invoice No:</strong> {invNo()}
                    </p>
                    <p class="small" style="font-size: 0.8rem; margin-bottom: 0.25rem;">
                      <strong>Date:</strong> {date()}
                    </p>
                  </div>
                </div>

                <table class="w-full text-sm" style="border-collapse: collapse; width: 100%; font-size: 0.75rem; margin-bottom: 1rem;">
                  <thead>
                    <tr style="background-color: #f8f9fa;">
                      <th style="padding: 0.375rem; text-align: center; width: 5%;">#</th>
                      <th style="padding: 0.375rem; text-align: left; width: 45%;">Item Description</th>
                      <th style="padding: 0.375rem; text-align: center; width: 10%;">Qty</th>
                      <th style="padding: 0.375rem; text-align: right; width: 20%;">Price</th>
                      <th style="padding: 0.375rem; text-align: right; width: 20%;">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    <For each={rows().filter((r) => r.itemId)}>
                      {(row, idx) => {
                        const st = stockList.find((s) => String(s.id) === String(row.itemId))
                        const itemName = st?.name || ''
                        const realIdx = rows().indexOf(row)
                        const tot = itemTotals()[realIdx]
                        return (
                          <tr style="border-bottom: 1px solid #f0f0f0;">
                            <td style="padding: 0.375rem; text-align: center;">{idx() + 1}</td>
                            <td style="padding: 0.375rem;">
                              <div style="font-weight: 600;">{itemName}</div>
                              <div style="color: #6c757d; font-size: 0.6rem;">
                                {isInterstate()
                                  ? `IGST ${row.taxPerc}%`
                                  : `CGST ${row.taxPerc / 2}% | SGST ${row.taxPerc / 2}%`
                                }
                              </div>
                            </td>
                            <td style="padding: 0.375rem; text-align: center;">{row.qty}</td>
                            <td style="padding: 0.375rem; text-align: right;">₹{formatMoney(row.price)}</td>
                            <td style="padding: 0.375rem; text-align: right; font-weight: 700;">
                              ₹{formatMoney(tot.rowTotal)}
                            </td>
                          </tr>
                        )
                      }}
                    </For>
                  </tbody>
                </table>

                <div style="display: flex; margin-top: auto;">
                  <div style="flex: 1; padding: 0.5rem; background-color: #f8f9fa; border-radius: 0.375rem; font-size: 0.65rem;">
                    <p style="font-weight: 700; margin-bottom: 0.25rem;">Terms & Conditions:</p>
                    <ul style="padding-left: 1rem; margin-bottom: 0;">
                      <For each={terms().split('\n').filter((l) => l.trim())}>
                        {(line) => <li>{line}</li>}
                      </For>
                    </ul>
                  </div>
                  <div style="flex: 0 0 auto; margin-left: 0.75rem;">
                    <div style="display: flex; gap: 0.75rem;">
                      <Show when={companyData.qr}>
                        <div style="width: 70px;">
                          <img src={companyData.qr} style="width: 100%;" />
                          <p style="text-align: center; font-size: 0.5rem; margin-top: 0.25rem;">Scan to Pay</p>
                        </div>
                      </Show>
                      <div>
                        <table style="border-collapse: collapse; font-size: 0.7rem;">
                          <tr>
                            <td style="padding: 0.15rem 0.5rem; color: #6c757d;">Taxable</td>
                            <td style="padding: 0.15rem 0.5rem; text-align: right;">
                              ₹{formatMoney(itemTotals().reduce((s, t) => s + t.taxable, 0))}
                            </td>
                          </tr>
                          <Show
                            when={isInterstate()}
                            fallback={
                              <>
                                <tr>
                                  <td style="padding: 0.15rem 0.5rem; color: #6c757d;">CGST</td>
                                  <td style="padding: 0.15rem 0.5rem; text-align: right;">
                                    ₹{formatMoney(itemTotals().reduce((s, t) => s + t.taxAmt / 2, 0))}
                                  </td>
                                </tr>
                                <tr>
                                  <td style="padding: 0.15rem 0.5rem; color: #6c757d;">SGST</td>
                                  <td style="padding: 0.15rem 0.5rem; text-align: right;">
                                    ₹{formatMoney(itemTotals().reduce((s, t) => s + t.taxAmt / 2, 0))}
                                  </td>
                                </tr>
                              </>
                            }
                          >
                            <tr>
                              <td style="padding: 0.15rem 0.5rem; color: #6c757d;">IGST</td>
                              <td style="padding: 0.15rem 0.5rem; text-align: right;">
                                ₹{formatMoney(itemTotals().reduce((s, t) => s + t.taxAmt, 0))}
                              </td>
                            </tr>
                          </Show>
                          <tr style="border-top: 1px solid #dee2e6;">
                            <td style="padding: 0.3rem 0.5rem; font-weight: 700; font-size: 0.9rem;">
                              Grand Total
                            </td>
                            <td style="padding: 0.3rem 0.5rem; text-align: right; font-weight: 700; font-size: 0.9rem; color: #0d6efd;">
                              ₹{formatMoney(grandTotal())}
                            </td>
                          </tr>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>

                <div
                  style="margin-top: 2rem; text-align: center; color: #6c757d; border-top: 1px dashed #ccc; padding-top: 0.75rem; font-size: 0.6rem;"
                >
                  This is a computer generated invoice and does not require signature.
                </div>
              </Show>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
