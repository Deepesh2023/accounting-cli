<script setup lang="ts">
const salesStore = useSalesStore()
const partiesStore = usePartiesStore()
const saleModal = ref<InstanceType<typeof SaleFormModal>>()

const filterMonth = ref('')
const filterFrom = ref('')
const filterTo = ref('')
const filterParty = ref('')

const partyOptions = computed(() => [
  { label: 'All Parties', value: '' },
  ...partiesStore.parties.filter(p => p.type === 'DEBTOR').map(p => ({ label: p.name, value: p.id })),
])

const filteredSales = computed(() => {
  return salesStore.sales.filter(s => {
    if (filterParty.value && s.partyId !== filterParty.value) return false
    if (filterMonth.value) {
      const saleMonth = s.date.slice(0, 7)
      if (saleMonth !== filterMonth.value) return false
    }
    if (filterFrom.value && s.date < filterFrom.value) return false
    if (filterTo.value && s.date > filterTo.value) return false
    return true
  })
})

function clearFilters() {
  filterMonth.value = ''
  filterFrom.value = ''
  filterTo.value = ''
  filterParty.value = ''
}

function viewInvoice(sale: any) {
  // TODO: open invoice view modal
}

function recordPayment(sale: any) {
  // TODO
}

function deleteSale(id: string) {
  salesStore.remove(id)
}
</script>

<template>
  <div class="space-y-6">
    <!-- Summary + action -->
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <div class="bg-primary text-white rounded-xl p-5 w-full sm:w-72">
        <p class="text-xs font-semibold uppercase tracking-wider opacity-75">Total Sales (All Time)</p>
        <p class="text-3xl font-bold mt-1">₹ {{ salesStore.totalSales.toFixed(2) }}</p>
      </div>
      <UButton label="+ Record Sale" color="primary" size="lg" icon="i-heroicons-plus" @click="saleModal?.openCreate()" />
    </div>

    <!-- Filters -->
    <UCard :ui="{ body: { padding: 'p-4' } }">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <UFormField label="Month">
          <UInput v-model="filterMonth" type="month" size="sm" />
        </UFormField>
        <UFormField label="From">
          <UInput v-model="filterFrom" type="date" size="sm" />
        </UFormField>
        <UFormField label="To">
          <UInput v-model="filterTo" type="date" size="sm" />
        </UFormField>
        <UFormField label="Party">
          <USelect v-model="filterParty" :items="partyOptions" size="sm" />
        </UFormField>
        <div class="flex items-end gap-2">
          <UButton label="Filter" color="primary" size="sm" />
          <UButton label="Clear" color="gray" variant="outline" size="sm" @click="clearFilters" />
        </div>
      </div>
    </UCard>

    <!-- Sales table -->
    <UCard>
      <template #header>
        <h3 class="font-semibold text-gray-900 dark:text-white">Recent Sales History</h3>
      </template>
      <UTable
        :rows="filteredSales"
        :columns="[
          { key: 'id', label: 'Invoice No', sortable: true },
          { key: 'date', label: 'Date', sortable: true },
          { key: 'partyName', label: 'Customer', sortable: true },
          { key: 'grandTotal', label: 'Amount (₹)', sortable: true },
          { key: 'balanceAmount', label: 'Balance', sortable: true },
          { key: 'actions', label: 'Actions', sortable: false },
        ]"
      >
        <template #grandTotal-data="{ row }">
          <span class="font-medium">₹ {{ row.grandTotal.toFixed(2) }}</span>
        </template>
        <template #balanceAmount-data="{ row }">
          <span :class="row.balanceAmount > 0 ? 'text-red-600 font-medium' : 'text-green-600'">
            ₹ {{ row.balanceAmount.toFixed(2) }}
          </span>
        </template>
        <template #actions-data="{ row }">
          <div class="flex gap-1">
            <UTooltip text="View Invoice">
              <UButton icon="i-heroicons-eye" color="gray" variant="ghost" size="2xs" @click="viewInvoice(row)" />
            </UTooltip>
            <UTooltip v-if="row.balanceAmount > 0" text="Record Payment">
              <UButton icon="i-heroicons-currency-rupee" color="green" variant="ghost" size="2xs" @click="recordPayment(row)" />
            </UTooltip>
            <UTooltip text="Delete">
              <UButton icon="i-heroicons-trash" color="red" variant="ghost" size="2xs" @click="deleteSale(row.id)" />
            </UTooltip>
          </div>
        </template>
        <template #empty>
          <div class="text-center py-8 text-gray-400">
            <UIcon name="i-heroicons-shopping-cart" class="w-12 h-12 mx-auto mb-2" />
            <p>No sales yet. Record your first sale!</p>
          </div>
        </template>
      </UTable>
    </UCard>

    <SaleFormModal ref="saleModal" />
  </div>
</template>
