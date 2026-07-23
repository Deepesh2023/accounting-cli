<script setup lang="ts">
const store = useStockStore()

const open = ref(false)
const editingId = ref<string | null>(null)
const form = reactive({
  name: '',
  itemCode: '',
  quantity: 0,
  unit: '',
  price: 0,
  gstRate: 0,
  hsnCode: '',
})

function openCreate() {
  editingId.value = null
  form.name = ''
  form.itemCode = ''
  form.quantity = 0
  form.unit = ''
  form.price = 0
  form.gstRate = 0
  form.hsnCode = ''
  open.value = true
}

function openEdit(item: { id: string; name: string; itemCode: string; quantity: number; unit: string; price: number; gstRate: number; hsnCode: string }) {
  editingId.value = item.id
  form.name = item.name
  form.itemCode = item.itemCode
  form.quantity = item.quantity
  form.unit = item.unit
  form.price = item.price
  form.gstRate = item.gstRate
  form.hsnCode = item.hsnCode
  open.value = true
}

function submit() {
  if (!form.name.trim()) return
  const data = {
    id: editingId.value || crypto.randomUUID(),
    name: form.name,
    itemCode: form.itemCode,
    quantity: form.quantity,
    unit: form.unit,
    price: form.price,
    gstRate: form.gstRate,
    hsnCode: form.hsnCode,
  }
  if (editingId.value) {
    store.update(editingId.value, data)
  } else {
    store.add(data)
  }
  open.value = false
}

defineExpose({ openCreate, openEdit })
</script>

<template>
  <UModal v-model:open="open" :title="editingId ? 'Edit Stock Item' : 'Add Stock Item'">
    <template #body>
      <form @submit.prevent="submit" class="space-y-4">
        <UFormField label="Name" required>
          <UInput v-model="form.name" placeholder="Item name" class="w-full" />
        </UFormField>
        <UFormField label="Item Code">
          <UInput v-model="form.itemCode" placeholder="Optional" class="w-full" />
        </UFormField>
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="Quantity">
            <UInput v-model="form.quantity" type="number" min="0" class="w-full" />
          </UFormField>
          <UFormField label="Unit">
            <UInput v-model="form.unit" placeholder="e.g. pcs, kg" class="w-full" />
          </UFormField>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="Price (₹)">
            <UInput v-model="form.price" type="number" min="0" step="0.01" class="w-full" />
          </UFormField>
          <UFormField label="GST Rate (%)">
            <UInput v-model="form.gstRate" type="number" min="0" step="0.1" class="w-full" />
          </UFormField>
        </div>
        <UFormField label="HSN Code">
          <UInput v-model="form.hsnCode" placeholder="Optional" class="w-full" />
        </UFormField>
      </form>
    </template>
    <template #footer>
      <UButton label="Cancel" variant="ghost" color="gray" @click="open = false" />
      <UButton :label="editingId ? 'Update' : 'Save'" color="primary" @click="submit" />
    </template>
  </UModal>
</template>
