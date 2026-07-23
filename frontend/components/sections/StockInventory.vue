<script setup lang="ts">
const store = useStockStore()
const stockModal = ref<InstanceType<typeof StockFormModal>>()
const searchQuery = ref('')

const filtered = computed(() => {
  if (!searchQuery.value) return store.items
  const q = searchQuery.value.toLowerCase()
  return store.items.filter(i =>
    i.name.toLowerCase().includes(q) || i.itemCode.toLowerCase().includes(q)
  )
})

function deleteItem(id: string) {
  store.remove(id)
}

function editItem(item: any) {
  stockModal.value?.openEdit(item)
}
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">
        <h3 class="font-semibold text-gray-900 dark:text-white">Stock Inventory</h3>
        <div class="flex gap-2 w-full sm:w-auto">
          <UInput v-model="searchQuery" placeholder="Search items..." class="w-full sm:w-48" size="sm" />
          <UButton label="+ Add Stock" color="primary" size="sm" @click="stockModal?.openCreate()" />
        </div>
      </div>
    </template>

    <div class="bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-sm p-3 rounded-lg mb-4">
      <strong>Tip:</strong> Double-click a row to edit. Right-click a row to delete.
    </div>

    <UTable
      :rows="filtered"
      :columns="[
        { key: 'index', label: '#' },
        { key: 'itemCode', label: 'Item Code' },
        { key: 'name', label: 'Name' },
        { key: 'quantity', label: 'Qty', sortable: true },
        { key: 'unit', label: 'Unit' },
        { key: 'price', label: 'Price (₹)', sortable: true },
        { key: 'totalValue', label: 'Total Value (₹)' },
        { key: 'actions', label: 'Actions' },
      ]"
      @select="editItem"
    >
      <template #index-data="{ index }">
        {{ index + 1 }}
      </template>
      <template #quantity-data="{ row }">
        <span :class="row.quantity > 10 ? 'text-blue-600' : 'text-red-600 font-medium'">{{ row.quantity }}</span>
      </template>
      <template #price-data="{ row }">
        {{ row.price.toFixed(2) }}
      </template>
      <template #totalValue-data="{ row }">
        <span class="font-medium">₹ {{ (row.quantity * row.price).toFixed(2) }}</span>
      </template>
      <template #actions-data="{ row }">
        <div class="flex gap-1">
          <UTooltip text="Edit">
            <UButton icon="i-heroicons-pencil-square" color="gray" variant="ghost" size="2xs" @click="editItem(row)" />
          </UTooltip>
          <UTooltip text="Delete">
            <UButton icon="i-heroicons-trash" color="red" variant="ghost" size="2xs" @click="deleteItem(row.id)" />
          </UTooltip>
        </div>
      </template>
      <template #empty>
        <div class="text-center py-8 text-gray-400">
          <UIcon name="i-heroicons-cube" class="w-12 h-12 mx-auto mb-2" />
          <p>No stock items. Add your first product!</p>
        </div>
      </template>
    </UTable>

    <StockFormModal ref="stockModal" />
  </UCard>
</template>
