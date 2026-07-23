<script setup lang="ts">
const purchasesStore = usePurchasesStore()
const partiesStore = usePartiesStore()
const stockStore = useStockStore()
const { computeRow, computeGrandTotal } = useAccounting()

const open = ref(false)
const editingId = ref<string | null>(null)
const activeTab = ref('details')
const isCredit = ref(true)

const form = reactive({
  partyId: '',
  billNo: '',
  date: new Date().toISOString().split('T')[0],
  dueDate: '',
  state: 'Karnataka',
  phone: '',
  address: '',
  roundOff: false,
  taxInclusive: false,
  paidAmount: 0,
  terms: '1. Goods subject to quality check.\n2. Payment within 30 days of invoice.',
})

interface PurchaseRow {
  id: string
  productId: string
  name: string
  quantity: number
  price: number
  discountPerc: number
  gstRate: number
}

const rows = ref<PurchaseRow[]>([])

const partyOptions = computed(() =>
  partiesStore.parties.filter(p => p.type === 'CREDITOR').map(p => ({ label: `${p.name} (₹${p.balance})`, value: p.id }))
)

const selectedParty = computed(() => partiesStore.get(form.partyId))

const totals = computed(() => {
  const items = rows.value.map(r => {
    const interstate = form.state !== '' && form.state !== 'Karnataka'
    return computeRow({
      price: r.price,
      quantity: r.quantity,
      gstRate: r.gstRate,
      discountPerc: r.discountPerc || undefined,
      interstate,
      taxInclusive: form.taxInclusive,
    })
  })
  const totalTaxable = items.reduce((s, i) => s + i.taxableAmount, 0)
  const totalTax = items.reduce((s, i) => s + i.taxAmount, 0)
  const grandTotal = computeGrandTotal(totalTaxable, totalTax, form.roundOff)
  const balance = Math.max(0, grandTotal - form.paidAmount)
  return {
    items: rows.value.map((r, i) => ({ ...r, ...items[i] })),
    totalTaxable,
    totalTax,
    grandTotal,
    balance,
  }
})

function addRow() {
  rows.value.push({
    id: crypto.randomUUID(),
    productId: '',
    name: '',
    quantity: 1,
    price: 0,
    discountPerc: 0,
    gstRate: 0,
  })
}

function removeRow(id: string) {
  rows.value = rows.value.filter(r => r.id !== id)
}

function onProductSelect(row: PurchaseRow, productId: string) {
  const product = stockStore.get(productId)
  if (product) {
    row.productId = productId
    row.name = product.name
    row.price = product.price
    row.gstRate = product.gstRate
  }
}

function openCreate() {
  editingId.value = null
  rows.value = []
  form.partyId = ''
  form.billNo = `BILL-${Date.now().toString(36).toUpperCase()}`
  form.date = new Date().toISOString().split('T')[0]
  form.dueDate = ''
  form.state = 'Karnataka'
  form.phone = ''
  form.address = ''
  form.roundOff = false
  form.taxInclusive = false
  form.paidAmount = 0
  form.terms = '1. Goods subject to quality check.\n2. Payment within 30 days of invoice.'
  isCredit.value = true
  activeTab.value = 'details'
  addRow()
  open.value = true
}

function submit() {
  const purchaseItems = totals.value.items.map(item => ({
    id: crypto.randomUUID(),
    productId: item.productId,
    name: item.name,
    quantity: item.quantity,
    price: item.price,
    discountAmount: item.discountAmount,
    taxableAmount: item.taxableAmount,
    taxAmount: item.taxAmount,
    cgst: item.cgst,
    sgst: item.sgst,
    igst: item.igst,
    rowTotal: item.rowTotal,
  }))

  const purchase = {
    id: editingId.value || crypto.randomUUID(),
    date: form.date,
    dueDate: form.dueDate,
    partyId: form.partyId,
    partyName: selectedParty.value?.name || 'Cash Purchase',
    items: purchaseItems,
    totalTaxable: totals.value.totalTaxable,
    totalTax: totals.value.totalTax,
    grandTotal: totals.value.grandTotal,
    paidAmount: isCredit.value ? form.paidAmount : totals.value.grandTotal,
    balanceAmount: isCredit.value ? totals.value.balance : 0,
    roundOff: form.roundOff,
    taxInclusive: form.taxInclusive,
  }

  if (editingId.value) {
    purchasesStore.update(editingId.value, purchase)
  } else {
    purchasesStore.add(purchase)
  }
  open.value = false
}

defineExpose({ openCreate })
</script>

<template>
  <UModal v-model:open="open" fullscreen :title="editingId ? 'Edit Purchase' : 'New Purchase'">
    <template #body>
      <div class="flex h-full">
        <div class="w-1/2 overflow-y-auto p-6 border-r border-gray-200 dark:border-gray-700">
          <div class="flex items-center gap-4 mb-6">
            <div class="bg-gray-100 dark:bg-gray-800 rounded-lg p-1 flex">
              <button
                :class="['px-4 py-1.5 rounded-md text-sm font-medium transition-colors', isCredit ? 'bg-green-600 text-white shadow-sm' : 'text-gray-500']"
                @click="isCredit = true"
              >Credit</button>
              <button
                :class="['px-4 py-1.5 rounded-md text-sm font-medium transition-colors', !isCredit ? 'bg-green-600 text-white shadow-sm' : 'text-gray-500']"
                @click="isCredit = false"
              >Cash</button>
            </div>
          </div>

          <div class="flex gap-4 border-b border-gray-200 dark:border-gray-700 mb-4">
            <button
              :class="['pb-2 text-sm font-medium border-b-2 transition-colors', activeTab === 'details' ? 'border-green-600 text-green-600' : 'border-transparent text-gray-500']"
              @click="activeTab = 'details'"
            >Purchase Details</button>
            <button
              :class="['pb-2 text-sm font-medium border-b-2 transition-colors', activeTab === 'terms' ? 'border-green-600 text-green-600' : 'border-transparent text-gray-500']"
              @click="activeTab = 'terms'"
            >Terms & Conditions</button>
          </div>

          <div v-if="activeTab === 'details'" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <UFormField label="Supplier">
                <div class="flex gap-2">
                  <USelect v-model="form.partyId" :items="partyOptions" placeholder="Select supplier" class="flex-1" />
                  <UButton icon="i-heroicons-plus" color="gray" variant="outline" size="sm" />
                </div>
              </UFormField>
              <UFormField label="Bill / Ref No">
                <UInput v-model="form.billNo" class="w-full" />
              </UFormField>
              <UFormField label="Date">
                <UInput v-model="form.date" type="date" class="w-full" />
              </UFormField>
              <UFormField label="Due Date">
                <UInput v-model="form.dueDate" type="date" class="w-full" />
              </UFormField>
              <UFormField label="State of Supply">
                <USelect v-model="form.state" :items="['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Delhi', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'West Bengal']" class="w-full" />
              </UFormField>
            </div>
            <UFormField label="Phone">
              <UInput v-model="form.phone" class="w-full" />
            </UFormField>
            <UFormField label="Address">
              <UInput v-model="form.address" class="w-full" />
            </UFormField>

            <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
              <table class="w-full text-sm">
                <thead class="bg-gray-50 dark:bg-gray-900 text-xs text-gray-500 uppercase">
                  <tr>
                    <th class="text-left px-3 py-2">#</th>
                    <th class="text-left px-3 py-2">Item</th>
                    <th class="text-center px-3 py-2">Qty</th>
                    <th class="text-right px-3 py-2">Price</th>
                    <th class="text-right px-3 py-2">Disc%</th>
                    <th class="text-center px-3 py-2">Tax%</th>
                    <th class="text-center px-2 py-2"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, i) in rows" :key="row.id" class="border-t border-gray-100 dark:border-gray-700">
                    <td class="px-3 py-1.5 text-gray-500">{{ i + 1 }}</td>
                    <td class="px-3 py-1.5">
                      <USelect
                        v-model="row.productId"
                        :items="stockStore.items.map(p => ({ label: p.name, value: p.id }))"
                        placeholder="Select"
                        size="sm"
                        @update:model-value="(val: string) => onProductSelect(row, val)"
                      />
                    </td>
                    <td class="px-3 py-1.5">
                      <UInput v-model="row.quantity" type="number" min="1" size="sm" class="w-16 text-center" />
                    </td>
                    <td class="px-3 py-1.5">
                      <UInput v-model="row.price" type="number" min="0" step="0.01" size="sm" class="w-24 text-right" />
                    </td>
                    <td class="px-3 py-1.5">
                      <UInput v-model="row.discountPerc" type="number" min="0" max="100" size="sm" class="w-16 text-right" />
                    </td>
                    <td class="px-3 py-1.5">
                      <UInput v-model="row.gstRate" type="number" min="0" step="0.1" size="sm" class="w-16 text-center" />
                    </td>
                    <td class="px-2 py-1.5 text-center">
                      <UButton icon="i-heroicons-x-mark" color="red" variant="ghost" size="2xs" @click="removeRow(row.id)" />
                    </td>
                  </tr>
                </tbody>
              </table>
              <UButton label="+ Add Row" color="gray" variant="ghost" class="w-full py-2" @click="addRow" />
            </div>

            <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Total Taxable</span>
                <span class="font-medium">₹ {{ totals.totalTaxable.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Total Tax</span>
                <span class="font-medium">₹ {{ totals.totalTax.toFixed(2) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <UCheckbox v-model="form.roundOff" label="Round Off" />
              </div>
              <div class="flex justify-between text-lg font-bold pt-2 border-t border-gray-200 dark:border-gray-600">
                <span>Grand Total</span>
                <span class="text-green-600">₹ {{ totals.grandTotal.toFixed(2) }}</span>
              </div>
              <div v-if="isCredit" class="flex justify-between items-center pt-2">
                <span class="text-gray-500">Amount Paid</span>
                <UInput v-model="form.paidAmount" type="number" min="0" step="0.01" class="w-28 text-right" />
              </div>
              <div v-if="isCredit && totals.balance > 0" class="flex justify-between text-red-600 font-semibold">
                <span>Balance</span>
                <span>₹ {{ totals.balance.toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <div v-else>
            <UFormField label="Terms & Conditions">
              <UTextarea v-model="form.terms" rows="8" class="w-full" />
            </UFormField>
          </div>
        </div>

        <div class="w-1/2 overflow-y-auto p-6 bg-gray-50 dark:bg-gray-900">
          <p class="text-xs text-gray-400 uppercase font-semibold mb-4">Voucher Preview</p>
          <InvoicePreview
            type="purchase"
            :invoice-no="form.billNo"
            :date="form.date"
            :due-date="form.dueDate"
            :party-name="selectedParty?.name || 'Cash Purchase'"
            :party-address="form.address"
            :party-phone="form.phone"
            :items="totals.items"
            :total-taxable="totals.totalTaxable"
            :total-tax="totals.totalTax"
            :grand-total="totals.grandTotal"
            :round-off="form.roundOff"
            :amount-paid="isCredit ? form.paidAmount : totals.grandTotal"
            :balance="isCredit ? totals.balance : 0"
            :terms="form.terms"
          />
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex justify-between w-full">
        <UButton label="Cancel" variant="ghost" color="gray" @click="open = false" />
        <UButton label="Save Purchase" color="green" @click="submit" />
      </div>
    </template>
  </UModal>
</template>
