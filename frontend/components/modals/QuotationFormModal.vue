<script setup lang="ts">
const store = useQuotationsStore()
const partiesStore = usePartiesStore()
const stockStore = useStockStore()

const open = ref(false)
const activeTab = ref('details')
const form = reactive({
  partyId: '',
  quotationNo: '',
  date: new Date().toISOString().split('T')[0],
  phone: '',
  notes: '',
  terms: '1. Quotation valid for 15 days.\n2. 50% advance along with Purchase Order.',
})

interface QuoteRow {
  id: string
  productId: string
  name: string
  quantity: number
  unitPrice: number
  gstRate: number
}

const rows = ref<QuoteRow[]>([])

const partyOptions = computed(() =>
  partiesStore.parties.map(p => ({ label: p.name, value: p.id }))
)

const totals = computed(() => {
  let total = 0
  const items = rows.value.map(r => {
    const rowTotal = r.quantity * r.unitPrice
    total += rowTotal
    return { ...r, totalPrice: rowTotal }
  })
  return { items, totalAmount: total }
})

function addRow() {
  rows.value.push({
    id: crypto.randomUUID(),
    productId: '',
    name: '',
    quantity: 1,
    unitPrice: 0,
    gstRate: 0,
  })
}

function removeRow(id: string) {
  rows.value = rows.value.filter(r => r.id !== id)
}

function onProductSelect(row: QuoteRow, productId: string) {
  const product = stockStore.get(productId)
  if (product) {
    row.productId = productId
    row.name = product.name
    row.unitPrice = product.price
    row.gstRate = product.gstRate
  }
}

function openCreate() {
  rows.value = []
  form.partyId = ''
  form.quotationNo = `Q-${Date.now().toString(36).toUpperCase()}`
  form.date = new Date().toISOString().split('T')[0]
  form.phone = ''
  form.notes = ''
  form.terms = '1. Quotation valid for 15 days.\n2. 50% advance along with Purchase Order.'
  activeTab.value = 'details'
  addRow()
  open.value = true
}

function submit() {
  const quotation = {
    id: crypto.randomUUID(),
    date: form.date,
    partyId: form.partyId,
    partyName: partiesStore.get(form.partyId)?.name || 'Walk-in',
    items: totals.value.items.map(item => ({
      id: crypto.randomUUID(),
      productId: item.productId,
      name: item.name,
      quantity: item.quantity,
      unitPrice: item.unitPrice,
      totalPrice: item.unitPrice * item.quantity,
    })),
    totalAmount: totals.value.totalAmount,
    status: 'Draft',
    notes: form.notes,
  }
  store.add(quotation)
  open.value = false
}

defineExpose({ openCreate })
</script>

<template>
  <UModal v-model:open="open" size="xl" title="New Quotation">
    <template #body>
      <div class="flex gap-4 border-b border-gray-200 dark:border-gray-700 mb-4">
        <button
          :class="['pb-2 text-sm font-medium border-b-2 transition-colors', activeTab === 'details' ? 'border-primary text-primary' : 'border-transparent text-gray-500']"
          @click="activeTab = 'details'"
        >Quotation Details</button>
        <button
          :class="['pb-2 text-sm font-medium border-b-2 transition-colors', activeTab === 'terms' ? 'border-primary text-primary' : 'border-transparent text-gray-500']"
          @click="activeTab = 'terms'"
        >Terms & Conditions</button>
      </div>

      <div v-if="activeTab === 'details'" class="space-y-4">
        <div class="grid grid-cols-4 gap-4">
          <UFormField label="Quotation No">
            <UInput v-model="form.quotationNo" class="w-full" />
          </UFormField>
          <UFormField label="Date">
            <UInput v-model="form.date" type="date" class="w-full" />
          </UFormField>
          <UFormField label="Customer">
            <USelect v-model="form.partyId" :items="partyOptions" placeholder="Select customer" class="w-full" />
          </UFormField>
          <UFormField label="Phone">
            <UInput v-model="form.phone" class="w-full" />
          </UFormField>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 dark:bg-gray-900 text-xs text-gray-500 uppercase">
              <tr>
                <th class="text-left px-3 py-2">Item</th>
                <th class="text-center px-3 py-2">Qty</th>
                <th class="text-right px-3 py-2">Price</th>
                <th class="text-right px-3 py-2">Total</th>
                <th class="text-center px-2 py-2"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in rows" :key="row.id" class="border-t border-gray-100 dark:border-gray-700">
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
                  <UInput v-model="row.unitPrice" type="number" min="0" step="0.01" size="sm" class="w-24 text-right" />
                </td>
                <td class="px-3 py-1.5 text-right font-medium">
                  ₹ {{ (row.quantity * row.unitPrice).toFixed(2) }}
                </td>
                <td class="px-2 py-1.5 text-center">
                  <UButton icon="i-heroicons-x-mark" color="red" variant="ghost" size="2xs" @click="removeRow(row.id)" />
                </td>
              </tr>
            </tbody>
          </table>
          <UButton label="+ Add Row" color="gray" variant="ghost" class="w-full py-2" @click="addRow" />
        </div>

        <div class="text-right">
          <p class="text-sm text-gray-500">Grand Total</p>
          <p class="text-2xl font-bold text-primary">₹ {{ totals.totalAmount.toFixed(2) }}</p>
        </div>
      </div>

      <div v-else>
        <UFormField label="Terms & Conditions">
          <UTextarea v-model="form.terms" rows="8" class="w-full" />
        </UFormField>
        <UFormField label="Notes" class="mt-4">
          <UTextarea v-model="form.notes" rows="3" class="w-full" />
        </UFormField>
      </div>
    </template>
    <template #footer>
      <UButton label="Cancel" variant="ghost" color="gray" @click="open = false" />
      <UButton label="Save Quotation" color="primary" @click="submit" />
    </template>
  </UModal>
</template>
