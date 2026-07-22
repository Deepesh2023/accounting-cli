<script setup lang="ts">
import type { SaleResponse, PurchaseResponse, SaleCreate, SaleItemInput, PartyResponse, ProductResponse } from '~/lib/api/client'

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
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Sales</h1>
      <button class="btn btn-primary btn-lg" @click="openAdd">+ Record Sale</button>
    </div>
    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <div class="stat-card bg-primary text-white">
          <h6>TOTAL SALES</h6>
          <h2>{{ formatCurrency(totalSales) }}</h2>
        </div>
      </div>
    </div>
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-auto">
            <label class="form-label small">Month</label>
            <input v-model="filterMonth" type="month" class="form-control form-control-sm" />
          </div>
          <div class="col-auto">
            <label class="form-label small">Customer</label>
            <select v-model="filterParty" class="form-select form-select-sm">
              <option value="">All</option>
              <option v-for="p in parties" :key="p.party_id" :value="p.party_id">{{ p.name }}</option>
            </select>
          </div>
          <div class="col-auto">
            <button class="btn btn-sm btn-outline-secondary" @click="filterMonth='';filterParty=''">Clear</button>
          </div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-4 text-muted">Loading...</div>
        <div v-else-if="!filteredSales.length" class="text-center py-4 text-muted">No sales found.</div>
        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Invoice No</th><th>Date</th><th>Customer</th><th>Mode</th><th>Status</th><th>Amount</th><th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in filteredSales" :key="s.sale_id">
                <td><code>#{{ s.sale_id?.slice(0, 8) }}</code></td>
                <td>{{ s.date?.slice(0, 10) }}</td>
                <td>{{ partyName(s.party_id) }}</td>
                <td>{{ modeLabel(s) }}</td>
                <td><span class="badge" :class="statusLabel(s).cls">{{ statusLabel(s).text }}</span></td>
                <td>{{ formatCurrency(s.grand_total) }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-info me-1" @click="viewSale(s)">View</button>
                  <button class="btn btn-sm btn-outline-primary me-1" @click="openEdit(s)">Edit</button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(s.sale_id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showForm" class="modal-backdrop fade show" @click="showForm = false"></div>
    <div v-if="showForm" class="modal fade show d-block" tabindex="-1" style="overflow-y:auto">
      <div class="modal-dialog modal-fullscreen">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editing ? 'Edit' : 'Record' }} Sale</h5>
            <ul class="nav nav-pills ms-4">
              <li class="nav-item"><button class="nav-link small" :class="{ active: activeTab === 'form' }" @click="activeTab = 'form'">Form</button></li>
              <li class="nav-item"><button class="nav-link small" :class="{ active: activeTab === 'preview' }" @click="activeTab = 'preview'">Preview</button></li>
            </ul>
            <button type="button" class="btn-close" @click="showForm = false"></button>
          </div>
          <div class="modal-body" v-if="activeTab === 'form'">
            <div class="row g-4">
              <div class="col-md-7">
                <div class="row g-3 mb-3">
                  <div class="col-6">
                    <label class="form-label">Customer</label>
                    <div class="input-group">
                      <select v-model="form.party_id" class="form-select">
                        <option value="">Walk-in</option>
                        <option v-for="p in parties" :key="p.party_id" :value="p.party_id">{{ p.name }}</option>
                      </select>
                      <button class="btn btn-outline-secondary" @click="showQuickParty = true">+</button>
                    </div>
                  </div>
                  <div class="col-3">
                    <label class="form-label">Paid Amount</label>
                    <input v-model.number="form.paid_amount" type="number" step="0.01" class="form-control" />
                  </div>
                  <div class="col-3 d-flex align-items-end">
                    <div class="form-check">
                      <input v-model="form.round_off" type="checkbox" class="form-check-input" id="ro" />
                      <label class="form-check-label" for="ro">Round Off</label>
                    </div>
                  </div>
                </div>

                <div class="table-responsive">
                  <table class="table table-sm table-bordered">
                    <thead class="table-light">
                      <tr>
                        <th>Product</th><th>Qty</th><th>Price</th><th>Disc%</th><th>Disc Amt</th><th>Tax%</th><th>Total</th><th></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(item, i) in form.items" :key="i">
                        <td style="min-width:160px">
                          <select v-model="item.product_id" class="form-select form-select-sm" @change="onProductSelect(item)">
                            <option value="">Select</option>
                            <option v-for="p in products" :key="p.product_id" :value="p.product_id">{{ p.name }}</option>
                          </select>
                        </td>
                        <td><input v-model.number="item.quantity" type="number" class="form-control form-control-sm" style="width:70px" @input="calcRow(item)" /></td>
                        <td><input v-model.number="item.price" type="number" class="form-control form-control-sm" style="width:90px" @input="calcRow(item)" /></td>
                        <td><input v-model.number="item.discount_perc" type="number" class="form-control form-control-sm" style="width:60px" @input="calcRow(item)" /></td>
                        <td>{{ formatCurrency(item.discount_amt || 0) }}</td>
                        <td><input v-model.number="item.tax_perc" type="number" class="form-control form-control-sm" style="width:60px" @input="calcRow(item)" /></td>
                        <td>{{ formatCurrency(item.row_total || 0) }}</td>
                        <td><button class="btn btn-sm btn-outline-danger" @click="removeItem(i)">×</button></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <button class="btn btn-sm btn-outline-primary" @click="addItem">+ Add Item</button>

                <hr />
                <div class="row g-3">
                  <div class="col-6">
                    <strong>Grand Total: {{ formatCurrency(grandTotal) }}</strong>
                  </div>
                  <div class="col-3">
                    <span>Paid: {{ formatCurrency(form.paid_amount) }}</span>
                  </div>
                  <div class="col-3">
                    <span :class="balanceAmount > 0 ? 'text-danger' : 'text-success'">Balance: {{ formatCurrency(balanceAmount) }}</span>
                  </div>
                </div>
              </div>
              <div class="col-md-5 border-start" v-html="invoicePreview"></div>
            </div>

            <div v-if="showQuickParty" class="mt-3 p-3 border rounded bg-light">
              <h6>Quick Add Party</h6>
              <div class="row g-2">
                <div class="col-4"><input v-model="quickPartyForm.name" class="form-control form-control-sm" placeholder="Name" /></div>
                <div class="col-3"><input v-model="quickPartyForm.phone" class="form-control form-control-sm" placeholder="Phone" /></div>
                <div class="col-3">
                  <select v-model="quickPartyForm.state" class="form-select form-select-sm">
                    <option value="Maharashtra">Maharashtra</option>
                    <option value="Delhi">Delhi</option>
                    <option value="Gujarat">Gujarat</option>
                  </select>
                </div>
                <div class="col-2">
                  <button class="btn btn-sm btn-success" @click="createQuickParty">Add</button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showForm = false">Cancel</button>
            <button class="btn btn-primary" @click="save">Save Sale</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showView" class="modal-backdrop fade show" @click="showView = false"></div>
    <div v-if="showView" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Sale #{{ viewing?.sale_id?.slice(0, 8) }}</h5>
            <button type="button" class="btn-close" @click="showView = false"></button>
          </div>
          <div class="modal-body" v-if="viewing">
            <p><strong>Date:</strong> {{ viewing.date?.slice(0, 10) }}</p>
            <p><strong>Customer:</strong> {{ partyName(viewing.party_id) }}</p>
            <p><strong>Mode:</strong> {{ modeLabel(viewing) }}</p>
            <p><strong>Status:</strong> <span class="badge" :class="statusLabel(viewing).cls">{{ statusLabel(viewing).text }}</span></p>
            <table class="table table-sm">
              <thead><tr><th>Item</th><th>Qty</th><th>Price</th><th class="text-end">Total</th></tr></thead>
              <tbody>
                <tr v-for="i in viewing.items" :key="i.sale_item_id">
                  <td>{{ i.name }}</td><td>{{ i.quantity }}</td><td>{{ formatCurrency(i.price) }}</td><td class="text-end">{{ formatCurrency(i.row_total) }}</td>
                </tr>
              </tbody>
            </table>
            <hr />
            <div class="text-end"><strong>Grand Total: {{ formatCurrency(viewing.grand_total) }}</strong></div>
            <div class="text-end">Paid: {{ formatCurrency(viewing.paid_amount) }}</div>
            <div class="text-end">Balance: {{ formatCurrency(viewing.balance_amount) }}</div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showView = false">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stat-card { border-radius: 12px; padding: 20px 24px; border: none; }
.stat-card h6 { opacity: 0.8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 8px; }
.stat-card h2 { margin: 0; font-weight: 700; }
.card { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-radius: 8px; }
.table th { font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.table td { vertical-align: middle; }
.modal-fullscreen { max-width: 95vw; }
</style>
