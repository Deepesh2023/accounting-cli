<script setup lang="ts">
import { useInventoryStore } from '~/stores/inventory'
import type { ProductResponse, ProductCreate, ProductUpdate } from '~/lib/api/client'

definePageMeta({ title: 'Stock' })

const store = useInventoryStore()
const showModal = ref(false)
const editing = ref<string | null>(null)
const form = ref<ProductCreate>({ name: '', selling_price: 0, quantity: 0, gst_rate: 0, hsn_code: '' })

function totalValue(p: ProductResponse) { return Number(p.selling_price) * p.quantity }

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
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Stock</h1>
      <UButton color="primary" @click="openAdd">+ Add Stock</UButton>
    </div>
    <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
      <div v-if="store.loading" class="text-center py-4 text-gray-500">Loading...</div>
      <div v-else-if="!store.items.length" class="text-center py-4 text-gray-500">No products found.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">#</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Code</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Name</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Qty</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Price</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Total Value</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">GST%</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">HSN</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="(p, i) in store.items" :key="p.product_id" class="hover:bg-gray-50">
              <td class="px-4 py-3">{{ i + 1 }}</td>
              <td class="px-4 py-3"><code class="text-sm bg-gray-100 px-1 rounded">{{ p.item_code || '-' }}</code></td>
              <td class="px-4 py-3">{{ p.name }}</td>
              <td class="px-4 py-3">{{ p.quantity }}</td>
              <td class="px-4 py-3">{{ currency(p.selling_price) }}</td>
              <td class="px-4 py-3">{{ currency(totalValue(p)) }}</td>
              <td class="px-4 py-3">{{ p.gst_rate }}%</td>
              <td class="px-4 py-3"><code class="text-sm bg-gray-100 px-1 rounded">{{ p.hsn_code }}</code></td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <UButton color="primary" variant="outline" size="sm" @click="openEdit(p)">Edit</UButton>
                  <UButton color="error" variant="outline" size="sm" @click="confirmDelete(p.product_id)">Delete</UButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <UModal v-model:open="showModal">
      <template #header>
        <h3 class="text-lg font-semibold">{{ editing ? 'Edit' : 'Add' }} Product</h3>
      </template>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
          <UInput v-model="form.name" placeholder="Product name" />
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Selling Price</label>
            <UInput v-model.number="form.selling_price" type="number" step="0.01" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
            <UInput v-model.number="form.quantity" type="number" />
          </div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">GST Rate (%)</label>
            <UInput v-model.number="form.gst_rate" type="number" step="0.1" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">HSN Code</label>
            <UInput v-model="form.hsn_code" placeholder="e.g. 8471" />
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton color="neutral" variant="outline" @click="showModal = false">Cancel</UButton>
          <UButton color="primary" @click="save">Save</UButton>
        </div>
      </template>
    </UModal>
  </div>
</template>

<style scoped>
</style>
