<script setup lang="ts">
import { useInventoryStore } from '~/stores/inventory'
import type { ProductResponse, ProductCreate, ProductUpdate } from '~/lib/api/client'

definePageMeta({ title: 'Stock' })

const store = useInventoryStore()
const showModal = ref(false)
const editing = ref<string | null>(null)
const form = ref<ProductCreate>({ name: '', selling_price: 0, quantity: 0, gst_rate: 0, hsn_code: '' })

onMounted(() => store.fetchAll())

function openAdd() {
  editing.value = null
  form.value = { name: '', selling_price: 0, quantity: 0, gst_rate: 0, hsn_code: '' }
  showModal.value = true
}

function openEdit(p: ProductResponse) {
  editing.value = p.product_id
  form.value = {
    name: p.name,
    selling_price: Number(p.selling_price),
    quantity: p.quantity,
    gst_rate: Number(p.gst_rate),
    hsn_code: p.hsn_code,
  }
  showModal.value = true
}

async function save() {
  if (editing.value) {
    await store.update(editing.value, form.value as ProductUpdate)
  } else {
    await store.create(form.value)
  }
  showModal.value = false
}

async function confirmDelete(id: string) {
  if (confirm('Delete this product?')) await store.remove(id)
}

const currency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Stock</h1>
      <button class="btn btn-primary" @click="openAdd">+ Add Stock</button>
    </div>
    <div class="card">
      <div class="card-body p-0">
        <div v-if="store.loading" class="text-center py-4 text-muted">Loading...</div>
        <div v-else-if="!store.items.length" class="text-center py-4 text-muted">No products found.</div>
        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>#</th><th>Name</th><th>Price</th><th>Qty</th><th>GST%</th><th>HSN</th><th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, i) in store.items" :key="p.product_id">
                <td>{{ i + 1 }}</td>
                <td>{{ p.name }}</td>
                <td>{{ currency(p.selling_price) }}</td>
                <td>{{ p.quantity }}</td>
                <td>{{ p.gst_rate }}%</td>
                <td><code>{{ p.hsn_code }}</code></td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-1" @click="openEdit(p)">Edit</button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(p.product_id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-backdrop fade show" @click="showModal = false"></div>
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editing ? 'Edit' : 'Add' }} Product</h5>
            <button type="button" class="btn-close" @click="showModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input v-model="form.name" class="form-control" placeholder="Product name" />
            </div>
            <div class="row g-3">
              <div class="col-12 col-sm-6">
                <label class="form-label">Selling Price</label>
                <input v-model.number="form.selling_price" type="number" step="0.01" class="form-control" />
              </div>
              <div class="col-12 col-sm-6">
                <label class="form-label">Quantity</label>
                <input v-model.number="form.quantity" type="number" class="form-control" />
              </div>
            </div>
            <div class="row g-3 mt-1">
              <div class="col-12 col-sm-6">
                <label class="form-label">GST Rate (%)</label>
                <input v-model.number="form.gst_rate" type="number" step="0.1" class="form-control" />
              </div>
              <div class="col-12 col-sm-6">
                <label class="form-label">HSN Code</label>
                <input v-model="form.hsn_code" class="form-control" placeholder="e.g. 8471" />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showModal = false">Cancel</button>
            <button class="btn btn-primary" @click="save">Save</button>
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
code { font-size: 0.85rem; }
</style>
