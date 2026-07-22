<script setup lang="ts">
import type { QuotationResponse, QuotationCreate, QuotationItemInput, PartyResponse, ProductResponse } from '~/lib/api/client'

definePageMeta({ title: 'Quotations' })

const quotations = ref<QuotationResponse[]>([])
const parties = ref<PartyResponse[]>([])
const products = ref<ProductResponse[]>([])
const loading = ref(false)
const showModal = ref(false)
const editing = ref<string | null>(null)

const form = ref<{
  party_id: string, status: string, notes: string,
  items: (QuotationItemInput & { row_total?: number })[],
}>({ party_id: '', status: 'Draft', notes: '', items: [] })

onMounted(loadAll)

async function loadAll() {
  loading.value = true
  try {
    const [q, p, pr] = await Promise.all([
      api().listQuotations(), api().listParties(), api().listProducts(),
    ])
    quotations.value = q
    parties.value = p
    products.value = pr
  } finally { loading.value = false }
}

function openAdd() {
  editing.value = null
  form.value = { party_id: '', status: 'Draft', notes: '', items: [] }
  addItem()
  showModal.value = true
}

function openEdit(q: QuotationResponse) {
  editing.value = q.quotation_id
  form.value = {
    party_id: q.party_id || '',
    status: q.status,
    notes: q.notes || '',
    items: q.items.map(i => ({
      product_id: i.product_id,
      name: i.name,
      quantity: i.quantity,
      unit_price: Number(i.unit_price),
      row_total: Number(i.total_price),
    })),
  }
  showModal.value = true
}

function addItem() {
  form.value.items.push({ product_id: '', name: '', quantity: 1, unit_price: 0, row_total: 0 })
}

function removeItem(i: number) { form.value.items.splice(i, 1) }

function onProductSelect(item: any) {
  const p = products.value.find(x => x.product_id === item.product_id)
  if (p) {
    item.name = p.name
    if (!item.unit_price) item.unit_price = Number(p.selling_price)
    calcRow(item)
  }
}

function calcRow(item: any) {
  item.row_total = item.quantity * item.unit_price
}

const grandTotal = computed(() => form.value.items.reduce((s, i) => s + (i.row_total || 0), 0))

async function save() {
  try {
    const payload: QuotationCreate = {
      party_id: form.value.party_id || undefined,
      status: form.value.status,
      notes: form.value.notes || undefined,
      items: form.value.items.map(i => ({
        product_id: i.product_id,
        name: i.name || '',
        quantity: i.quantity,
        unit_price: i.unit_price,
      })),
    }
    if (editing.value) {
      await api().updateQuotation(editing.value, payload)
    } else {
      await api().createQuotation(payload)
    }
    showModal.value = false
    await loadAll()
  } catch (e: any) { alert(e.message) }
}

async function confirmDelete(id: string) {
  if (confirm('Delete this quotation?')) {
    await api().deleteQuotation(id)
    await loadAll()
  }
}

function partyName(id: string | undefined) {
  return parties.value.find(p => p.party_id === id)?.name || 'Walk-in'
}

const currency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="m-0">Quotations</h1>
      <UButton color="primary" @click="openAdd">+ New Quotation</UButton>
    </div>

    <div class="shadow-sm rounded-lg overflow-hidden border border-gray-200 bg-white">
      <div v-if="loading" class="text-center py-4 text-gray-500">Loading...</div>
      <div v-else-if="!quotations.length" class="text-center py-4 text-gray-500">No quotations found.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">ID</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Date</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Customer</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Amount</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Status</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="q in quotations" :key="q.quotation_id" class="hover:bg-gray-50 border-b border-gray-200">
              <td class="p-3 align-middle"><code>#{{ q.quotation_id?.slice(0, 8) }}</code></td>
              <td class="p-3 align-middle">{{ q.date?.slice(0, 10) }}</td>
              <td class="p-3 align-middle">{{ partyName(q.party_id) }}</td>
              <td class="p-3 align-middle">{{ currency(q.total_amount) }}</td>
              <td class="p-3 align-middle">
                <UBadge :color="q.status === 'Accepted' ? 'success' : q.status === 'Rejected' ? 'error' : 'neutral'" variant="solid">
                  {{ q.status }}
                </UBadge>
              </td>
              <td class="p-3 align-middle whitespace-nowrap space-x-1">
                <UButton size="sm" variant="ghost" color="primary" @click="openEdit(q)">Edit</UButton>
                <UButton size="sm" variant="ghost" color="error" @click="confirmDelete(q.quotation_id)">Delete</UButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <UModal v-model:open="showModal">
      <template #title>{{ editing ? 'Edit' : 'New' }} Quotation</template>
      <div class="space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <USelect v-model="form.party_id" :items="[{label: 'Walk-in', value: ''}, ...parties.map(p => ({ label: p.name, value: p.party_id }))]" placeholder="Customer" />
          <USelect v-model="form.status" :items="['Draft', 'Sent', 'Accepted', 'Rejected']" placeholder="Status" />
        </div>

        <div class="overflow-x-auto border border-gray-200 rounded-lg">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="p-2 text-left font-semibold text-sm">Product</th>
                <th class="p-2 text-left font-semibold text-sm">Qty</th>
                <th class="p-2 text-left font-semibold text-sm">Unit Price</th>
                <th class="p-2 text-left font-semibold text-sm">Total</th>
                <th class="p-2"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, i) in form.items" :key="i" class="border-b border-gray-200">
                <td class="p-1 min-w-40">
                  <select v-model="item.product_id" class="border border-gray-300 rounded text-sm p-1 w-full" @change="onProductSelect(item)">
                    <option value="">Select</option>
                    <option v-for="p in products" :key="p.product_id" :value="p.product_id">{{ p.name }}</option>
                  </select>
                </td>
                <td class="p-1">
                  <input v-model.number="item.quantity" type="number" class="border border-gray-300 rounded text-sm p-1 w-[70px]" @input="calcRow(item)" />
                </td>
                <td class="p-1">
                  <input v-model.number="item.unit_price" type="number" step="0.01" class="border border-gray-300 rounded text-sm p-1 w-[100px]" @input="calcRow(item)" />
                </td>
                <td class="p-1 text-sm whitespace-nowrap">{{ currency(item.row_total || 0) }}</td>
                <td class="p-1">
                  <UButton size="2xs" color="error" variant="ghost" @click="removeItem(i)">×</UButton>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <UButton size="sm" variant="outline" color="primary" @click="addItem">+ Add Item</UButton>

        <UTextarea v-model="form.notes" placeholder="Notes" :rows="2" />

        <hr class="border-gray-200" />
        <div class="text-right font-bold">Grand Total: {{ currency(grandTotal) }}</div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton color="neutral" variant="ghost" @click="showModal = false">Cancel</UButton>
          <UButton color="primary" @click="save">Save Quotation</UButton>
        </div>
      </template>
    </UModal>
  </div>
</template>
