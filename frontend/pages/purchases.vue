<script setup lang="ts">
import type { PurchaseResponse, PurchaseCreate, PurchaseItemInput, PartyResponse, ProductResponse } from '~/lib/api/client'

definePageMeta({ title: 'Purchases' })

const purchases = ref<PurchaseResponse[]>([])
const parties = ref<PartyResponse[]>([])
const products = ref<ProductResponse[]>([])
const loading = ref(false)
const showForm = ref(false)
const showView = ref(false)
const editing = ref<string | null>(null)
const viewing = ref<PurchaseResponse | null>(null)
const filterMonth = ref('')
const filterParty = ref('')
const activeTab = ref<'form' | 'preview'>('form')

const form = ref<{
  party_id: string, paid_amount: number, round_off: boolean, tax_inclusive: boolean,
  items: (PurchaseItemInput & { name?: string, row_total?: number })[],
}>({
  party_id: '', paid_amount: 0, round_off: false, tax_inclusive: false,
  items: [],
})

const showQuickSupplier = ref(false)
const quickSupplierForm = ref({ name: '', phone: '', state: 'Maharashtra', address: '', balance: 0, party_type: 'CREDITOR' as const })

async function loadAll() {
  loading.value = true
  try {
    const [pch, p, pr] = await Promise.all([
      api().listPurchases(), api().listParties(), api().listProducts(),
    ])
    purchases.value = pch
    parties.value = p
    products.value = pr
  } finally { loading.value = false }
}

onMounted(loadAll)

const filteredPurchases = computed(() => {
  let list = purchases.value
  if (filterMonth.value) list = list.filter(s => s.date?.startsWith(filterMonth.value))
  if (filterParty.value) list = list.filter(s => s.party_id === filterParty.value)
  return list
})

const totalPurchases = computed(() => purchases.value.reduce((sum, s) => sum + Number(s.grand_total), 0))

function openAdd() {
  editing.value = null
  form.value = { party_id: '', paid_amount: 0, round_off: false, tax_inclusive: false, items: [] }
  addItem()
  showForm.value = true
  activeTab.value = 'form'
}

async function openEdit(s: PurchaseResponse) {
  editing.value = s.purchase_id
  form.value = {
    party_id: s.party_id || '', paid_amount: Number(s.paid_amount),
    round_off: s.round_off, tax_inclusive: false,
    items: s.items.map(i => ({
      product_id: i.product_id, quantity: i.quantity,
      price: Number(i.price),
      discount_perc: 0, discount_amt: Number(i.discount_amount),
      tax_perc: 0, name: i.name, row_total: Number(i.row_total),
    })),
  }
  showForm.value = true
  activeTab.value = 'form'
}

function addItem() {
  form.value.items.push({ product_id: '', quantity: 1, price: 0, discount_perc: 0, discount_amt: 0, tax_perc: 0, name: '', row_total: 0 })
}

function removeItem(i: number) { form.value.items.splice(i, 1) }

function onProductSelect(item: any) {
  const p = products.value.find(x => x.product_id === item.product_id)
  if (p) {
    item.name = p.name
    if (!item.price) item.price = Number(p.selling_price)
    if (!item.tax_perc) item.tax_perc = Number(p.gst_rate)
    calcRow(item)
  }
}

function calcRow(item: any) {
  const total = item.quantity * item.price
  const discAmt = item.discount_perc ? total * item.discount_perc / 100 : (item.discount_amt || 0)
  const taxable = total - discAmt
  const taxAmt = item.tax_perc ? taxable * item.tax_perc / 100 : 0
  item.discount_amt = discAmt
  item.row_total = taxable + taxAmt
}

const grandTotal = computed(() => {
  const t = form.value.items.reduce((s, i) => s + (i.row_total || 0), 0)
  return form.value.round_off ? Math.round(t) : t
})

const balanceAmount = computed(() => grandTotal.value - form.value.paid_amount)

const invoicePreview = computed(() => {
  const itms = form.value.items.map(i => `
    <tr><td>${i.name || '-'}</td><td>${i.quantity}</td><td>${formatCurrency(i.price || 0)}</td><td>${formatCurrency(i.discount_amt || 0)}</td><td>${i.tax_perc || 0}%</td><td class="text-end">${formatCurrency(i.row_total || 0)}</td></tr>
  `).join('')
  return `
    <div style="padding:20px;font-family:monospace;font-size:13px">
      <h5 style="text-align:center;margin-bottom:16px;color:#198754">PURCHASE BILL</h5>
      <table style="width:100%;border-collapse:collapse">
        <thead><tr style="background:#d1e7dd"><th style="padding:6px;border:1px solid #ddd;text-align:left">Item</th><th style="padding:6px;border:1px solid #ddd">Qty</th><th style="padding:6px;border:1px solid #ddd">Price</th><th style="padding:6px;border:1px solid #ddd">Disc</th><th style="padding:6px;border:1px solid #ddd">Tax</th><th style="padding:6px;border:1px solid #ddd;text-align:right">Total</th></tr></thead>
        <tbody>${itms || '<tr><td colspan="6" style="text-align:center;color:#999;padding:12px">No items</td></tr>'}</tbody>
      </table>
      <hr style="margin:12px 0" />
      <div style="text-align:right"><strong>Grand Total: ${formatCurrency(grandTotal)}</strong></div>
      <div style="text-align:right;color:#666">Paid: ${formatCurrency(form.value.paid_amount)}</div>
      <div style="text-align:right;color:#666">Balance: ${formatCurrency(balanceAmount)}</div>
    </div>
  `
})

async function save() {
  try {
    const payload: PurchaseCreate = {
      party_id: form.value.party_id || undefined,
      items_data: form.value.items.map(i => ({
        product_id: i.product_id, quantity: i.quantity,
        price: i.price || 0,
        discount_perc: i.discount_perc, discount_amt: i.discount_amt, tax_perc: i.tax_perc,
      })),
      paid_amount: form.value.paid_amount,
      round_off: form.value.round_off,
      tax_inclusive: form.value.tax_inclusive,
    }
    if (editing.value) {
      await api().updatePurchase(editing.value, payload)
    } else {
      await api().createPurchase(payload)
    }
    showForm.value = false
    await loadAll()
  } catch (e: any) { alert(e.message) }
}

async function confirmDelete(id: string) {
  if (confirm('Delete this purchase? This will reverse stock & balance.')) {
    await api().deletePurchase(id)
    await loadAll()
  }
}

async function viewPurchase(s: PurchaseResponse) {
  viewing.value = s
  showView.value = true
}

async function createQuickSupplier() {
  try {
    const p = await api().createParty(quickSupplierForm.value)
    parties.value.push(p)
    form.value.party_id = p.party_id
    showQuickSupplier.value = false
  } catch (e: any) { alert(e.message) }
}

function partyName(id: string | undefined) {
  return parties.value.find(p => p.party_id === id)?.name || 'Walk-in'
}

function statusLabel(s: PurchaseResponse) {
  const bal = Number(s.balance_amount)
  if (bal <= 0) return { text: 'Paid', cls: 'bg-success' }
  if (Number(s.paid_amount) > 0) return { text: 'Partial', cls: 'bg-warning text-dark' }
  return { text: 'Unpaid', cls: 'bg-danger' }
}

const formatCurrency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="m-0">Purchases</h1>
      <UButton color="success" size="lg" @click="openAdd">+ Record Purchase</UButton>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-3 mb-4">
      <div class="md:col-span-4">
        <div class="bg-green-600 text-white rounded-xl p-5">
          <h6 class="opacity-80 text-xs uppercase tracking-wider mb-2">TOTAL PURCHASES</h6>
          <h2 class="font-bold text-2xl m-0">{{ formatCurrency(totalPurchases) }}</h2>
        </div>
      </div>
    </div>

    <UCard class="mb-4">
      <div class="flex flex-wrap items-end gap-3">
        <div>
          <label class="text-sm">Month</label>
          <UInput v-model="filterMonth" type="month" size="sm" />
        </div>
        <div>
          <label class="text-sm">Supplier</label>
          <USelect v-model="filterParty" :items="[{label: 'All', value: ''}, ...parties.map(p => ({label: p.name, value: p.party_id}))]" size="sm" />
        </div>
        <div>
          <UButton color="neutral" variant="outline" size="sm" @click="filterMonth='';filterParty=''">Clear</UButton>
        </div>
      </div>
    </UCard>

    <UCard>
      <div v-if="loading" class="text-center py-4 text-gray-500">Loading...</div>
      <div v-else-if="!filteredPurchases.length" class="text-center py-4 text-gray-500">No purchases found.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50">
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Bill No</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Date</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Supplier</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Status</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Amount</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in filteredPurchases" :key="s.purchase_id" class="hover:bg-gray-50 border-b border-gray-200">
              <td class="p-2"><code>#{{ s.purchase_id?.slice(0, 8) }}</code></td>
              <td class="p-2">{{ s.date?.slice(0, 10) }}</td>
              <td class="p-2">{{ partyName(s.party_id) }}</td>
              <td class="p-2">
                <UBadge :color="statusLabel(s).text === 'Paid' ? 'success' : statusLabel(s).text === 'Partial' ? 'warning' : 'error'" variant="solid">{{ statusLabel(s).text }}</UBadge>
              </td>
              <td class="p-2">{{ formatCurrency(s.grand_total) }}</td>
              <td class="p-2">
                <div class="flex gap-1">
                  <UButton size="sm" variant="ghost" color="info" @click="viewPurchase(s)">View</UButton>
                  <UButton size="sm" variant="ghost" color="primary" @click="openEdit(s)">Edit</UButton>
                  <UButton size="sm" variant="ghost" color="error" @click="confirmDelete(s.purchase_id)">Delete</UButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UCard>

    <UModal v-model:open="showForm" fullscreen>
      <template #title>{{ editing ? 'Edit' : 'Record' }} Purchase</template>

      <div class="flex gap-1 mb-3">
        <UButton :color="activeTab === 'form' ? 'primary' : 'neutral'" variant="soft" size="sm" @click="activeTab = 'form'">Form</UButton>
        <UButton :color="activeTab === 'preview' ? 'primary' : 'neutral'" variant="soft" size="sm" @click="activeTab = 'preview'">Preview</UButton>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
        <div class="md:col-span-7" :class="activeTab === 'preview' ? 'hidden md:block' : ''">
          <div class="grid grid-cols-1 sm:grid-cols-12 gap-3 mb-3">
            <div class="sm:col-span-6">
              <label class="text-sm">Supplier</label>
              <div class="flex gap-1">
                <USelect v-model="form.party_id" :items="[{label: 'Walk-in', value: ''}, ...parties.map(p => ({label: p.name, value: p.party_id}))]" class="flex-1" />
                <UButton color="neutral" variant="outline" @click="showQuickSupplier = true">+</UButton>
              </div>
            </div>
            <div class="sm:col-span-3">
              <label class="text-sm">Paid Amount</label>
              <UInput v-model.number="form.paid_amount" type="number" step="0.01" />
            </div>
            <div class="sm:col-span-3 flex items-end pb-1">
              <UCheckbox v-model="form.round_off" label="Round Off" />
            </div>
          </div>

          <div class="overflow-x-auto border border-gray-200 rounded-lg mb-2">
            <table class="w-full">
              <thead class="bg-gray-50">
                <tr>
                  <th class="p-2 text-left font-semibold text-sm">Product</th>
                  <th class="p-2 text-left font-semibold text-sm">Qty</th>
                  <th class="p-2 text-left font-semibold text-sm">Price</th>
                  <th class="p-2 text-left font-semibold text-sm">Disc%</th>
                  <th class="p-2 text-left font-semibold text-sm">Disc Amt</th>
                  <th class="p-2 text-left font-semibold text-sm">Tax%</th>
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
                    <input v-model.number="item.quantity" type="number" class="border border-gray-300 rounded text-sm p-1 w-16" @input="calcRow(item)" />
                  </td>
                  <td class="p-1">
                    <input v-model.number="item.price" type="number" class="border border-gray-300 rounded text-sm p-1 w-20" @input="calcRow(item)" />
                  </td>
                  <td class="p-1">
                    <input v-model.number="item.discount_perc" type="number" class="border border-gray-300 rounded text-sm p-1 w-14" @input="calcRow(item)" />
                  </td>
                  <td class="p-1 text-sm whitespace-nowrap">{{ formatCurrency(item.discount_amt || 0) }}</td>
                  <td class="p-1">
                    <input v-model.number="item.tax_perc" type="number" class="border border-gray-300 rounded text-sm p-1 w-14" @input="calcRow(item)" />
                  </td>
                  <td class="p-1 text-sm whitespace-nowrap">{{ formatCurrency(item.row_total || 0) }}</td>
                  <td class="p-1">
                    <UButton size="2xs" color="error" variant="ghost" @click="removeItem(i)">×</UButton>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <UButton size="sm" variant="outline" color="success" @click="addItem">+ Add Item</UButton>

          <hr class="border-gray-200 my-3" />

          <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
            <div class="sm:col-span-6">
              <strong>Grand Total: {{ formatCurrency(grandTotal) }}</strong>
            </div>
            <div class="sm:col-span-3">
              <span>Paid: {{ formatCurrency(form.paid_amount) }}</span>
            </div>
            <div class="sm:col-span-3">
              <span :class="balanceAmount > 0 ? 'text-red-600' : 'text-green-600'">Balance: {{ formatCurrency(balanceAmount) }}</span>
            </div>
          </div>
        </div>

        <div class="md:col-span-5 border-l border-gray-200" :class="activeTab === 'form' ? 'hidden md:block' : ''" v-html="invoicePreview"></div>
      </div>

      <div v-if="showQuickSupplier" class="mt-3 p-3 border border-gray-200 rounded-lg bg-gray-100">
        <h6 class="font-bold mb-2">Quick Add Supplier</h6>
        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2">
          <div class="sm:col-span-4"><UInput v-model="quickSupplierForm.name" size="sm" placeholder="Name" /></div>
          <div class="sm:col-span-3"><UInput v-model="quickSupplierForm.phone" size="sm" placeholder="Phone" /></div>
          <div class="sm:col-span-3">
            <USelect v-model="quickSupplierForm.state" :items="['Maharashtra', 'Delhi', 'Gujarat']" size="sm" />
          </div>
          <div class="sm:col-span-2">
            <UButton color="success" size="sm" @click="createQuickSupplier">Add</UButton>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton color="neutral" variant="ghost" @click="showForm = false">Cancel</UButton>
          <UButton color="success" @click="save">Save Purchase</UButton>
        </div>
      </template>
    </UModal>

    <UModal v-model:open="showView">
      <template #title>Purchase #{{ viewing?.purchase_id?.slice(0, 8) }}</template>
      <div v-if="viewing" class="space-y-2">
        <p><strong>Date:</strong> {{ viewing.date?.slice(0, 10) }}</p>
        <p><strong>Supplier:</strong> {{ partyName(viewing.party_id) }}</p>
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50">
              <th class="p-1 text-left font-semibold">Item</th>
              <th class="p-1 text-left font-semibold">Qty</th>
              <th class="p-1 text-left font-semibold">Price</th>
              <th class="p-1 text-right font-semibold">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="i in viewing.items" :key="i.purchase_item_id" class="border-b border-gray-200">
              <td class="p-1">{{ i.name }}</td>
              <td class="p-1">{{ i.quantity }}</td>
              <td class="p-1">{{ formatCurrency(i.price) }}</td>
              <td class="p-1 text-right">{{ formatCurrency(i.row_total) }}</td>
            </tr>
          </tbody>
        </table>
        <hr class="border-gray-200 my-3" />
        <div class="text-right"><strong>Grand Total: {{ formatCurrency(viewing.grand_total) }}</strong></div>
        <div class="text-right">Paid: {{ formatCurrency(viewing.paid_amount) }}</div>
        <div class="text-right">Balance: {{ formatCurrency(viewing.balance_amount) }}</div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton color="neutral" variant="ghost" @click="showView = false">Close</UButton>
        </div>
      </template>
    </UModal>
  </div>
</template>

<style scoped>
</style>
