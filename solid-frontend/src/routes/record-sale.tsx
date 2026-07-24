import { createMemo, For, Show, onMount, createEffect } from 'solid-js'
import { createFileRoute, Link, useNavigate } from '@tanstack/solid-router'
import { createForm } from '@tanstack/solid-form'
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

type SaleFormValues = {
  mode: 'Credit' | 'Cash'
  customerId: string
  phone: string
  address: string
  custState: string
  invNo: string
  date: string
  dueDate: string
  roundOff: boolean
  paid: number
  terms: string
  priceType: 'Without Tax' | 'With Tax'
  rows: SaleRow[]
  editingId: number | undefined
}

function defaultValues(edit?: number): SaleFormValues {
  return {
    mode: 'Credit',
    customerId: '',
    phone: '',
    address: '',
    custState: '',
    invNo: generateInvoiceNo(),
    date: new Date().toISOString().split('T')[0],
    dueDate: '',
    roundOff: false,
    paid: 0,
    terms: 'Goods once sold will not be taken back.',
    priceType: 'Without Tax',
    rows: [emptyRow()],
    editingId: edit,
  }
}

export const Route = createFileRoute('/record-sale')({
  validateSearch: (search: Record<string, string | undefined>) => ({
    edit: search.edit ? Number(search.edit) : undefined,
  }),
  component: NewSale,
})

function NewSale() {
  const navigate = useNavigate()
  const search = Route.useSearch()

  const form = createForm(() => ({
    defaultValues: defaultValues(search().edit),
    onSubmit: ({ value }: { value: SaleFormValues }) => {
      handleSave(value)
    },
  }))

  const values = () => form.store.state.values
  const rows = () => values().rows

  const sortedStock = createMemo(() => [...stockList].sort((a, b) => a.name.localeCompare(b.name)))

  const customer = createMemo(() => partyList.find((p) => String(p.id) === String(values().customerId)))

  const itemTotals = createMemo(() =>
    rows().map((row) => {
      const gross = row.qty * row.price
      const discAmt = row.discAmt
      const taxable = Math.max(0, gross - discAmt)
      let taxAmt: number
      let baseTaxable = taxable
      if (values().priceType === 'With Tax') {
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
    if (values().roundOff) total = Math.round(total)
    return total
  })

  const balance = createMemo(() => {
    if (values().mode === 'Cash') return 0
    return Math.max(0, grandTotal() - values().paid)
  })

  const isInterstate = createMemo(() => {
    const coState = companyData.state
    const cs = values().custState
    return !!(coState && cs && coState !== cs)
  })

  function selectCustomer(id: string) {
    form.setFieldValue('customerId', id)
  }

  createEffect(() => {
    const id = values().customerId
    const editId = values().editingId
    if (!id) return
    const p = partyList.find((x) => String(x.id) === String(id))
    if (p && !editId) {
      if (p.phone) form.setFieldValue('phone', p.phone)
      if (p.address) form.setFieldValue('address', p.address)
      if (p.state) form.setFieldValue('custState', p.state)
    }
  })

  function addRow() {
    form.setFieldValue('rows', [...rows(), emptyRow()])
  }

  function removeRow(idx: number) {
    const r = rows()
    if (r.length <= 1) return
    form.setFieldValue('rows', r.filter((_, i) => i !== idx))
  }

  function updateRow(idx: number, patch: Partial<SaleRow>) {
    form.setFieldValue('rows', rows().map((r, i) => (i === idx ? { ...r, ...patch } : r)))
  }

  function onItemSelect(idx: number, itemId: string) {
    const st = stockList.find((s) => String(s.id) === String(itemId))
    const patch: Partial<SaleRow> = { itemId }
    if (st) patch.price = st.price
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

  function setModeWithReset(m: 'Credit' | 'Cash') {
    form.setFieldValue('mode', m)
    if (m === 'Cash') {
      form.setFieldValue('paid', grandTotal())
      form.setFieldValue('dueDate', '')
    }
  }

  function handleSave(v: SaleFormValues) {
    for (const row of v.rows) {
      if (!row.itemId) continue
      const st = stockList.find((s) => String(s.id) === String(row.itemId))
      if (st) {
        let available = st.qty
        if (v.editingId) {
          const oldT = transactions.find((t) => t.id === v.editingId)
          if (oldT?.sale_details) {
            const oldItem = oldT.sale_details.items.find((it) => it.item_id === row.itemId)
            if (oldItem) available += oldItem.qty
          }
        }
        if (available < row.qty) {
          alert(`Insufficient stock for ${st.name}. Available: ${available}`)
          return
        }
      }
    }

    if (grandTotal() <= 0) {
      alert('Total amount cannot be zero.')
      return
    }

    if (v.mode === 'Credit' && !v.customerId) {
      alert('Credit sale requires a customer to be selected.')
      return
    }

    const total = grandTotal()
    const paidAmt = v.mode === 'Cash' ? total : v.paid
    const bal = v.mode === 'Cash' ? 0 : Math.max(0, total - paidAmt)
    const paymentStatus = bal === 0 ? 'Paid' : paidAmt > 0 ? 'Partial' : 'Unpaid'
    const custName = customer()?.name || 'Walk-in'

    if (v.editingId) {
      const oldT = transactions.find((t) => t.id === v.editingId)
      if (oldT?.sale_details) {
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
      deleteLedgerByRef(v.editingId)
      setTransactions((prev) => prev.filter((t) => t.id !== v.editingId))
    }

    if (v.customerId) {
      const p = partyList.find((x) => String(x.id) === String(v.customerId))
      if (p) {
        const idx = partyList.indexOf(p)
        setPartyList(idx, 'phone', v.phone)
        setPartyList(idx, 'address', v.address)
      }
    }

    const itemsData: SaleItem[] = []
    for (let i = 0; i < v.rows.length; i++) {
      const row = v.rows[i]
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

    if (v.customerId && v.mode === 'Credit') {
      const p = partyList.find((x) => String(x.id) === String(v.customerId))
      if (p) {
        const pIdx = partyList.indexOf(p)
        let signedBal = (p.type === 'Receive' ? 1 : -1) * p.balance
        signedBal += bal
        setPartyList(pIdx, 'balance', Math.abs(signedBal))
        setPartyList(pIdx, 'type', signedBal >= 0 ? 'Receive' : 'Pay')
      }
    }

    const id = v.editingId || Date.now()
    const t = {
      id,
      date: v.date,
      particulars: `${v.invNo} - Sale to ${custName}`,
      type: 'Sale' as const,
      payment_mode: (v.mode === 'Credit' ? 'Credit' : 'Cash') as 'Credit' | 'Cash',
      amount: total,
      sale_details: {
        customer_id: v.customerId || '',
        invoice_no: v.invNo,
        phone: v.phone,
        address: v.address,
        state_of_supply: v.custState,
        due_date: v.dueDate,
        items: itemsData,
        paid_amount: paidAmt,
        balance_amount: bal,
        payment_status: paymentStatus as 'Paid' | 'Partial' | 'Unpaid',
        is_roundoff: v.roundOff,
        price_type: v.priceType,
        terms: v.terms,
      },
    }

    setTransactions(transactions.length, t)

    if (v.mode === 'Credit' && v.customerId) {
      updateLedger(v.date, v.customerId, 'DR', total, id, 'Sales: ' + v.invNo)
      updateLedger(v.date, 'Sales', 'CR', total, id, 'Sales to ' + custName)
      if (paidAmt > 0) {
        updateLedger(v.date, 'Cash', 'DR', paidAmt, id, 'Receipt against ' + v.invNo)
        updateLedger(v.date, v.customerId, 'CR', paidAmt, id, 'Payment Receipt')
      }
    } else {
      updateLedger(v.date, 'Cash', 'DR', total, id, 'Cash Sales: ' + v.invNo)
      updateLedger(v.date, 'Sales', 'CR', total, id, 'Cash Sales')
    }

    persistState()
    navigate({ to: '/sales' })
  }

  onMount(() => {
    const editId = search().edit
    if (!editId) return
    const t = transactions.find((x) => x.id === editId)
    if (!t?.sale_details) return
    const d = t.sale_details
    form.setFieldValue('editingId', editId)
    form.setFieldValue('mode', t.payment_mode === 'Credit' ? 'Credit' : 'Cash')
    form.setFieldValue('customerId', d.customer_id || '')
    form.setFieldValue('phone', d.phone || '')
    form.setFieldValue('address', d.address || '')
    form.setFieldValue('custState', d.state_of_supply || '')
    form.setFieldValue('invNo', d.invoice_no)
    form.setFieldValue('date', t.date)
    form.setFieldValue('dueDate', d.due_date || '')
    form.setFieldValue('roundOff', !!d.is_roundoff)
    form.setFieldValue('paid', d.paid_amount || 0)
    form.setFieldValue('terms', d.terms || '')
    form.setFieldValue('priceType', (d.price_type as 'Without Tax' | 'With Tax') || 'Without Tax')
    if (d.items.length > 0) {
      form.setFieldValue(
        'rows',
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
        <h4 class="font-bold mb-0">{values().editingId ? 'Edit Sale' : 'New Sale'}</h4>
      </div>

      <div class="flex gap-6">
        <div class="w-[58%] space-y-4">
          <div class="bg-white rounded-xl shadow-sm border-0 p-4">
            <div class="flex items-center justify-between mb-4">
              <div class="flex gap-2">
                <button
                  type="button"
                  class={`px-4 py-1.5 rounded-lg text-sm font-bold transition-colors cursor-pointer ${values().mode === 'Credit' ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-600'}`}
                  onClick={() => setModeWithReset('Credit')}
                >
                  Credit
                </button>
                <button
                  type="button"
                  class={`px-4 py-1.5 rounded-lg text-sm font-bold transition-colors cursor-pointer ${values().mode === 'Cash' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-600'}`}
                  onClick={() => setModeWithReset('Cash')}
                >
                  Cash
                </button>
              </div>
              <form.Field name="priceType">
                {(field) => {
                  const f = field()
                  return (
                    <div class="flex items-center gap-2">
                      <label class="text-xs text-gray-500 font-bold">Price Type</label>
                      <select
                        class="border border-gray-300 rounded px-2 py-1 text-sm"
                        value={f.state.value}
                        onChange={(e) => f.handleChange(e.currentTarget.value as 'Without Tax' | 'With Tax')}
                      >
                        <option value="Without Tax">Without Tax</option>
                        <option value="With Tax">With Tax</option>
                      </select>
                    </div>
                  )
                }}
              </form.Field>
            </div>

            <div class="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label class="block text-xs text-gray-500 font-bold mb-1">Customer</label>
                <select
                  class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                  value={values().customerId}
                  onChange={(e) => selectCustomer(e.currentTarget.value)}
                >
                  <option value="">Walk-in Customer</option>
                  <For each={partyList}>
                    {(p) => <option value={p.id}>{p.name}</option>}
                  </For>
                </select>
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
                <form.Field name="invNo">
                  {(field) => {
                    const f = field()
                    return (
                      <div>
                        <label class="block text-xs text-gray-500 font-bold mb-1">Invoice No</label>
                        <input
                          type="text"
                          class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm font-bold"
                          value={f.state.value}
                          onInput={(e) => f.handleChange(e.currentTarget.value)}
                        />
                      </div>
                    )
                  }}
                </form.Field>
                <form.Field name="date">
                  {(field) => {
                    const f = field()
                    return (
                      <div>
                        <label class="block text-xs text-gray-500 font-bold mb-1">Date</label>
                        <input
                          type="date"
                          class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                          value={f.state.value}
                          onInput={(e) => f.handleChange(e.currentTarget.value)}
                        />
                      </div>
                    )
                  }}
                </form.Field>
              </div>
              <form.Field name="phone">
                {(field) => {
                  const f = field()
                  return (
                    <div>
                      <label class="block text-xs text-gray-500 font-bold mb-1">Phone</label>
                      <input
                        type="text"
                        class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                        value={f.state.value}
                        onInput={(e) => f.handleChange(e.currentTarget.value)}
                      />
                    </div>
                  )
                }}
              </form.Field>
              <form.Field name="custState">
                {(field) => {
                  const f = field()
                  return (
                    <div>
                      <label class="block text-xs text-gray-500 font-bold mb-1">State of Supply</label>
                      <select
                        class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                        value={f.state.value}
                        onChange={(e) => f.handleChange(e.currentTarget.value)}
                      >
                        <option value="">Select State</option>
                        <For each={indianStates.filter((s) => s !== 'Select State')}>
                          {(s) => <option value={s}>{s}</option>}
                        </For>
                      </select>
                    </div>
                  )
                }}
              </form.Field>
              <div class="col-span-2">
                <form.Field name="address">
                  {(field) => {
                    const f = field()
                    return (
                      <div>
                        <label class="block text-xs text-gray-500 font-bold mb-1">Address</label>
                        <input
                          type="text"
                          class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                          value={f.state.value}
                          onInput={(e) => f.handleChange(e.currentTarget.value)}
                        />
                      </div>
                    )
                  }}
                </form.Field>
              </div>
              <Show when={values().mode === 'Credit'}>
                <form.Field name="dueDate">
                  {(field) => {
                    const f = field()
                    return (
                      <div>
                        <label class="block text-xs text-gray-500 font-bold mb-1">Due Date</label>
                        <input
                          type="date"
                          class="w-full border border-gray-300 rounded px-2 py-1.5 text-sm"
                          value={f.state.value}
                          onInput={(e) => f.handleChange(e.currentTarget.value)}
                        />
                      </div>
                    )
                  }}
                </form.Field>
              </Show>
            </div>

            <div>
              <div class="flex items-center justify-between mb-2">
                <h6 class="font-bold text-sm mb-0">Invoice Items</h6>
                <button
                  type="button"
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
                                type="button"
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
                <form.Field name="roundOff">
                  {(field) => {
                    const f = field()
                    return (
                      <label class="flex items-center gap-2 text-sm cursor-pointer">
                        <input
                          type="checkbox"
                          checked={f.state.value}
                          onChange={(e) => f.handleChange(e.currentTarget.checked)}
                          class="accent-blue-600"
                        />
                        <span class="text-gray-700">Round off to nearest integer</span>
                      </label>
                    )
                  }}
                </form.Field>
              </div>
              <div class="text-right">
                <div class="flex items-center gap-4">
                  <Show when={values().mode === 'Credit'}>
                    <form.Field name="paid">
                      {(field) => {
                        const f = field()
                        return (
                          <div>
                            <label class="block text-xs text-gray-500 font-bold mb-1">Paid Amount (₹)</label>
                            <input
                              type="number"
                              class="w-32 border border-gray-300 rounded px-2 py-1.5 text-sm text-right"
                              value={f.state.value}
                              step="0.01"
                              onInput={(e) => f.handleChange(parseFloat(e.currentTarget.value) || 0)}
                            />
                          </div>
                        )
                      }}
                    </form.Field>
                  </Show>
                  <div>
                    <label class="block text-xs text-gray-500 font-bold mb-1">Grand Total</label>
                    <h3 class="mb-0 font-bold text-blue-600 text-2xl">₹{formatMoney(grandTotal())}</h3>
                  </div>
                  <Show when={values().mode === 'Credit'}>
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
            <form.Field name="terms">
              {(field) => {
                const f = field()
                return (
                  <>
                    <label class="block text-xs text-gray-500 font-bold mb-1 uppercase">Terms & Conditions</label>
                    <textarea
                      class="w-full border border-gray-300 rounded px-3 py-2 text-sm"
                      rows="2"
                      value={f.state.value}
                      onInput={(e) => f.handleChange(e.currentTarget.value)}
                    />
                  </>
                )
              }}
            </form.Field>
            <div class="flex justify-end gap-3 mt-3">
              <Link
                to="/sales"
                class="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-bold"
              >
                Cancel
              </Link>
              <button
                type="button"
                onClick={() => form.handleSubmit()}
                class="px-6 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-bold cursor-pointer"
              >
                {values().editingId ? 'Update Sale' : 'Save Sale'}
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
                  <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="display: flex; gap: 0.75rem;">
                      <Show when={companyData.logo}>
                        <div>
                          <img src={companyData.logo} style="height: 60px; object-fit: contain;" />
                        </div>
                      </Show>
                      <div>
                        <h2 style="font-weight: 700; margin-bottom: 0; color: #0d6efd; font-size: 1.25rem;">
                          {companyData.name || 'PRINTOS'}
                        </h2>
                        <p style="color: #6c757d; margin: 0; font-size: 0.8rem;">
                          {companyData.address || '-'}
                        </p>
                        <p style="color: #6c757d; margin: 0; font-size: 0.8rem;">
                          Phone: {companyData.phone || '-'} | Email: {companyData.email || '-'}
                        </p>
                        <p style="color: #6c757d; margin: 0; font-size: 0.8rem; font-weight: 700;">
                          GSTIN: {companyData.gstin || '-'}
                        </p>
                      </div>
                    </div>
                    <div style="text-align: right;">
                      <h1 style="font-weight: 700; color: #0d6efd; font-size: 1.5rem; margin-bottom: 0;">
                        {values().mode === 'Credit' ? 'CREDIT INVOICE' : 'CASH INVOICE'}
                      </h1>
                      <p style="margin: 0; color: #6c757d; font-size: 0.75rem;">
                        Original for Recipient
                      </p>
                    </div>
                  </div>
                </div>

                <div style="display: flex; margin-bottom: 1rem;">
                  <div style="flex: 1;">
                    <p style="color: #6c757d; text-transform: uppercase; margin-bottom: 0.25rem; font-size: 0.75rem; font-weight: 700;">
                      Bill To:
                    </p>
                    <h5 style="font-weight: 700; margin-bottom: 0.25rem;">
                      {customer()?.name || 'Walk-in Customer'}
                    </h5>
                    <p style="margin: 0; color: #6c757d; font-size: 0.75rem;">
                      {values().address || '-'}
                    </p>
                    <p style="margin: 0; color: #6c757d; font-size: 0.75rem;">
                      Phone: {values().phone || '-'}
                    </p>
                    <p style="margin: 0; color: #6c757d; font-size: 0.75rem;">
                      State: {values().custState || '-'}
                    </p>
                  </div>
                  <div style="text-align: right;">
                    <p style="font-size: 0.8rem; margin-bottom: 0.25rem;">
                      <strong>Invoice No:</strong> {values().invNo}
                    </p>
                    <p style="font-size: 0.8rem; margin-bottom: 0.25rem;">
                      <strong>Date:</strong> {values().date}
                    </p>
                  </div>
                </div>

                <table style="border-collapse: collapse; width: 100%; font-size: 0.75rem; margin-bottom: 1rem;">
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
                      <For each={values().terms.split('\n').filter((l) => l.trim())}>
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
                              ₹{formatMoney(itemTotals().reduce((s: number, t: { taxable: number }) => s + t.taxable, 0))}
                            </td>
                          </tr>
                          <Show
                            when={isInterstate()}
                            fallback={
                              <>
                                <tr>
                                  <td style="padding: 0.15rem 0.5rem; color: #6c757d;">CGST</td>
                                  <td style="padding: 0.15rem 0.5rem; text-align: right;">
                                    ₹{formatMoney(itemTotals().reduce((s: number, t: { taxAmt: number }) => s + t.taxAmt / 2, 0))}
                                  </td>
                                </tr>
                                <tr>
                                  <td style="padding: 0.15rem 0.5rem; color: #6c757d;">SGST</td>
                                  <td style="padding: 0.15rem 0.5rem; text-align: right;">
                                    ₹{formatMoney(itemTotals().reduce((s: number, t: { taxAmt: number }) => s + t.taxAmt / 2, 0))}
                                  </td>
                                </tr>
                              </>
                            }
                          >
                            <tr>
                              <td style="padding: 0.15rem 0.5rem; color: #6c757d;">IGST</td>
                              <td style="padding: 0.15rem 0.5rem; text-align: right;">
                                ₹{formatMoney(itemTotals().reduce((s: number, t: { taxAmt: number }) => s + t.taxAmt, 0))}
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
