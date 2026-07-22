<script setup lang="ts">
import type { SaleResponse, SaleCreate, SaleItemInput, PartyResponse, ProductResponse } from '~/lib/api/client'

definePageMeta({ title: 'Sales' })

const sales = ref<SaleResponse[]>([])
const parties = ref<PartyResponse[]>([])
const products = ref<ProductResponse[]>([])
const loading = ref(false)
const showForm = ref(false)
const showView = ref(false)
const editing = ref<string | null>(null)
const viewing = ref<SaleResponse | null>(null)
const filterMonth = ref('')
const filterParty = ref('')
const activeTab = ref<'form' | 'preview'>('form')

const form = ref<{
  party_id: string, paid_amount: number, round_off: boolean, tax_inclusive: boolean,
  items: (SaleItemInput & { name?: string, price?: number, row_total?: number })[],
}>({
  party_id: '', paid_amount: 0, round_off: false, tax_inclusive: false,
  items: [],
})

const showQuickParty = ref(false)
const quickPartyForm = ref({ name: '', phone: '', state: 'Maharashtra', address: '', balance: 0, party_type: 'DEBTOR' as const })

async function loadAll() {
  loading.value = true
  try {
    const [s, p, pr] = await Promise.all([
      api().listSales(), api().listParties(), api().listProducts(),
    ])
    sales.value = s
    parties.value = p
    products.value = pr
  } finally { loading.value = false }
}

onMounted(loadAll)

const filteredSales = computed(() => {
  let list = sales.value
  if (filterMonth.value) {
    list = list.filter(s => s.date?.startsWith(filterMonth.value))
  }
  if (filterParty.value) {
    list = list.filter(s => s.party_id === filterParty.value)
  }
  return list
})

const totalSales = computed(() => sales.value.reduce((sum, s) => sum + Number(s.grand_total), 0))

function openAdd() {
  editing.value = null
  form.value = { party_id: '', paid_amount: 0, round_off: false, tax_inclusive: false, items: [] }
  addItem()
  showForm.value = true
  activeTab.value = 'form'
}

async function openEdit(s: SaleResponse) {
  editing.value = s.sale_id
  form.value = {
    party_id: s.party_id || '', paid_amount: Number(s.paid_amount),
    round_off: s.round_off, tax_inclusive: false,
    items: s.items.map(i => ({
      product_id: i.product_id, quantity: i.quantity,
      discount_perc: 0, discount_amt: Number(i.discount_amount),
      tax_perc: 0, name: i.name, price: Number(i.price),
      row_total: Number(i.row_total),
    })),
  }
  showForm.value = true
  activeTab.value = 'form'
}

function addItem() {
  form.value.items.push({ product_id: '', quantity: 1, discount_perc: 0, discount_amt: 0, tax_perc: 0, name: '', price: 0, row_total: 0 })
}

function removeItem(i: number) { form.value.items.splice(i, 1) }

function onProductSelect(item: any) {
  const p = products.value.find(x => x.product_id === item.product_id)
  if (p) {
    item.name = p.name
    item.price = Number(p.selling_price)
    item.tax_perc = Number(p.gst_rate)
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
      <h5 style="text-align:center;margin-bottom:16px">TAX INVOICE</h5>
      <table style="width:100%;border-collapse:collapse">
        <thead><tr style="background:#f5f5f5"><th style="padding:6px;border:1px solid #ddd;text-align:left">Item</th><th style="padding:6px;border:1px solid #ddd">Qty</th><th style="padding:6px;border:1px solid #ddd">Price</th><th style="padding:6px;border:1px solid #ddd">Disc</th><th style="padding:6px;border:1px solid #ddd">Tax</th><th style="padding:6px;border:1px solid #ddd;text-align:right">Total</th></tr></thead>
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
    const payload: SaleCreate = {
      party_id: form.value.party_id || undefined,
      items_data: form.value.items.map(i => ({
        product_id: i.product_id, quantity: i.quantity,
        discount_perc: i.discount_perc, discount_amt: i.discount_amt, tax_perc: i.tax_perc,
      })),
      paid_amount: form.value.paid_amount,
      round_off: form.value.round_off,
      tax_inclusive: form.value.tax_inclusive,
    }
    if (editing.value) {
      await api().updateSale(editing.value, payload)
    } else {
      await api().createSale(payload)
    }
    showForm.value = false
    await loadAll()
  } catch (e: any) { alert(e.message) }
}

async function confirmDelete(id: string) {
  if (confirm('Delete this sale? This will reverse stock & balance.')) {
    await api().deleteSale(id)
    await loadAll()
  }
}

async function viewSale(s: SaleResponse) {
  viewing.value = s
  showView.value = true
}

async function createQuickParty() {
  try {
    const p = await api().createParty(quickPartyForm.value)
    parties.value.push(p)
    form.value.party_id = p.party_id
    showQuickParty.value = false
  } catch (e: any) { alert(e.message) }
}

function partyName(id: string | undefined) {
  return parties.value.find(p => p.party_id === id)?.name || 'Walk-in'
}

function statusLabel(s: SaleResponse) {
  const bal = Number(s.balance_amount)
  if (bal <= 0) return { text: 'Paid', cls: 'bg-success' }
  if (Number(s.paid_amount) > 0) return { text: 'Partial', cls: 'bg-warning text-dark' }
  return { text: 'Unpaid', cls: 'bg-danger' }
}

function modeLabel(s: SaleResponse) {
  return Number(s.balance_amount) <= 0 ? 'Cash' : 'Credit'
}

const formatCurrency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="m-0">Sales</h1>
      <UButton color="primary" size="lg" @click="openAdd">+ Record Sale</UButton>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-12 gap-3 mb-4">
      <div class="md:col-span-4">
        <div class="bg-blue-600 text-white rounded-xl p-5">
          <h6 class="opacity-80 text-xs uppercase tracking-wider mb-2">TOTAL SALES</h6>
          <h2 class="font-bold text-2xl m-0">{{ formatCurrency(totalSales) }}</h2>
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
          <label class="text-sm">Customer</label>
          <USelect v-model="filterParty" :items="[{label: 'All', value: ''}, ...parties.map(p => ({label: p.name, value: p.party_id}))]" size="sm" />
        </div>
        <div>
          <UButton color="neutral" variant="outline" size="sm" @click="filterMonth='';filterParty=''">Clear</UButton>
        </div>
      </div>
    </UCard>

    <UCard>
      <div v-if="loading" class="text-center py-4 text-gray-500">Loading...</div>
      <div v-else-if="!filteredSales.length" class="text-center py-4 text-gray-500">No sales found.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50">
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Invoice No</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Date</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Customer</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Mode</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Status</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Amount</th>
              <th class="p-2 text-left font-semibold text-xs uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in filteredSales" :key="s.sale_id" class="hover:bg-gray-50 border-b border-gray-200">
              <td class="p-2"><code>#{{ s.sale_id?.slice(0, 8) }}</code></td>
              <td class="p-2">{{ s.date?.slice(0, 10) }}</td>
              <td class="p-2">{{ partyName(s.party_id) }}</td>
              <td class="p-2">{{ modeLabel(s) }}</td>
              <td class="p-2">
                <UBadge :color="statusLabel(s).text === 'Paid' ? 'success' : statusLabel(s).text === 'Partial' ? 'warning' : 'error'" variant="solid">{{ statusLabel(s).text }}</UBadge>
              </td>
              <td class="p-2">{{ formatCurrency(s.grand_total) }}</td>
              <td class="p-2">
                <div class="flex gap-1">
                  <UButton size="sm" variant="ghost" color="info" @click="viewSale(s)">View</UButton>
                  <UButton size="sm" variant="ghost" color="primary" @click="openEdit(s)">Edit</UButton>
                  <UButton size="sm" variant="ghost" color="error" @click="confirmDelete(s.sale_id)">Delete</UButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UCard>

    <UModal v-model:open="showForm" fullscreen>
      <template #title>{{ editing ? 'Edit' : 'Record' }} Sale</template>

      <div class="flex gap-1 mb-3">
        <UButton :color="activeTab === 'form' ? 'primary' : 'neutral'" variant="soft" size="sm" @click="activeTab = 'form'">Form</UButton>
        <UButton :color="activeTab === 'preview' ? 'primary' : 'neutral'" variant="soft" size="sm" @click="activeTab = 'preview'">Preview</UButton>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
        <div class="md:col-span-7" :class="activeTab === 'preview' ? 'hidden md:block' : ''">
          <div class="grid grid-cols-1 sm:grid-cols-12 gap-3 mb-3">
            <div class="sm:col-span-6">
              <label class="text-sm">Customer</label>
              <div class="flex gap-1">
                <USelect v-model="form.party_id" :items="[{label: 'Walk-in', value: ''}, ...parties.map(p => ({label: p.name, value: p.party_id}))]" class="flex-1" />
                <UButton color="neutral" variant="outline" @click="showQuickParty = true">+</UButton>
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
          <UButton size="sm" variant="outline" color="primary" @click="addItem">+ Add Item</UButton>

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

      <div v-if="showQuickParty" class="mt-3 p-3 border border-gray-200 rounded-lg bg-gray-100">
        <h6 class="font-bold mb-2">Quick Add Party</h6>
        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2">
          <div class="sm:col-span-4"><UInput v-model="quickPartyForm.name" size="sm" placeholder="Name" /></div>
          <div class="sm:col-span-3"><UInput v-model="quickPartyForm.phone" size="sm" placeholder="Phone" /></div>
          <div class="sm:col-span-3">
            <USelect v-model="quickPartyForm.state" :items="['Maharashtra', 'Delhi', 'Gujarat']" size="sm" />
          </div>
          <div class="sm:col-span-2">
            <UButton color="success" size="sm" @click="createQuickParty">Add</UButton>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton color="neutral" variant="ghost" @click="showForm = false">Cancel</UButton>
          <UButton color="primary" @click="save">Save Sale</UButton>
        </div>
      </template>
    </UModal>

    <UModal v-model:open="showView">
      <template #title>Sale #{{ viewing?.sale_id?.slice(0, 8) }}</template>
      <div v-if="viewing" class="space-y-2">
        <p><strong>Date:</strong> {{ viewing.date?.slice(0, 10) }}</p>
        <p><strong>Customer:</strong> {{ partyName(viewing.party_id) }}</p>
        <p><strong>Mode:</strong> {{ modeLabel(viewing) }}</p>
        <p><strong>Status:</strong> <UBadge :color="statusLabel(viewing).text === 'Paid' ? 'success' : statusLabel(viewing).text === 'Partial' ? 'warning' : 'error'" variant="solid">{{ statusLabel(viewing).text }}</UBadge></p>
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
            <tr v-for="i in viewing.items" :key="i.sale_item_id" class="border-b border-gray-200">
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
