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
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Quotations</h1>
      <button class="btn btn-primary" @click="openAdd">+ New Quotation</button>
    </div>
    <div class="card">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-4 text-muted">Loading...</div>
        <div v-else-if="!quotations.length" class="text-center py-4 text-muted">No quotations found.</div>
        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr><th>ID</th><th>Date</th><th>Customer</th><th>Amount</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody>
              <tr v-for="q in quotations" :key="q.quotation_id">
                <td><code>#{{ q.quotation_id?.slice(0, 8) }}</code></td>
                <td>{{ q.date?.slice(0, 10) }}</td>
                <td>{{ partyName(q.party_id) }}</td>
                <td>{{ currency(q.total_amount) }}</td>
                <td><span class="badge" :class="q.status === 'Accepted' ? 'bg-success' : q.status === 'Rejected' ? 'bg-danger' : 'bg-secondary'">{{ q.status }}</span></td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-1" @click="openEdit(q)">Edit</button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(q.quotation_id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-backdrop fade show" @click="showModal = false"></div>
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editing ? 'Edit' : 'New' }} Quotation</h5>
            <button type="button" class="btn-close" @click="showModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="row g-3 mb-3">
              <div class="col-6">
                <label class="form-label">Customer</label>
                <select v-model="form.party_id" class="form-select">
                  <option value="">Walk-in</option>
                  <option v-for="p in parties" :key="p.party_id" :value="p.party_id">{{ p.name }}</option>
                </select>
              </div>
              <div class="col-4">
                <label class="form-label">Status</label>
                <select v-model="form.status" class="form-select">
                  <option value="Draft">Draft</option>
                  <option value="Sent">Sent</option>
                  <option value="Accepted">Accepted</option>
                  <option value="Rejected">Rejected</option>
                </select>
              </div>
            </div>

            <div class="table-responsive">
              <table class="table table-sm table-bordered">
                <thead class="table-light">
                  <tr><th>Product</th><th>Qty</th><th>Unit Price</th><th>Total</th><th></th></tr>
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
                    <td><input v-model.number="item.unit_price" type="number" step="0.01" class="form-control form-control-sm" style="width:100px" @input="calcRow(item)" /></td>
                    <td>{{ currency(item.row_total || 0) }}</td>
                    <td><button class="btn btn-sm btn-outline-danger" @click="removeItem(i)">×</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <button class="btn btn-sm btn-outline-primary" @click="addItem">+ Add Item</button>

            <div class="mt-3">
              <label class="form-label">Notes</label>
              <textarea v-model="form.notes" class="form-control" rows="2"></textarea>
            </div>

            <hr />
            <div class="text-end"><strong>Grand Total: {{ currency(grandTotal) }}</strong></div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showModal = false">Cancel</button>
            <button class="btn btn-primary" @click="save">Save Quotation</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-radius: 8px; }
.table th { font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.table td { vertical-align: middle; }
</style>
