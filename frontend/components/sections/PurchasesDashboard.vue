<script setup lang="ts">
const purchasesStore = usePurchasesStore()
const partiesStore = usePartiesStore()
const purchaseModal = ref<InstanceType<typeof PurchaseFormModal>>()

const filterMonth = ref('')
const filterFrom = ref('')
const filterTo = ref('')
const filterParty = ref('')

const partyOptions = computed(() => [
  { label: 'All Suppliers', value: '' },
  ...partiesStore.parties.filter(p => p.type === 'CREDITOR').map(p => ({ label: p.name, value: p.id })),
])

const filteredPurchases = computed(() => {
  return purchasesStore.purchases.filter(p => {
    if (filterParty.value && p.partyId !== filterParty.value) return false
    if (filterMonth.value) {
      const pm = p.date.slice(0, 7)
      if (pm !== filterMonth.value) return false
    }
    if (filterFrom.value && p.date < filterFrom.value) return false
    if (filterTo.value && p.date > filterTo.value) return false
    return true
  })
})

function clearFilters() {
  filterMonth.value = ''
  filterFrom.value = ''
  filterTo.value = ''
  filterParty.value = ''
}

function deletePurchase(id: string) {
  purchasesStore.remove(id)
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
      <div class="bg-green-600 text-white rounded-xl p-5 w-full sm:w-72">
        <p class="text-xs font-semibold uppercase tracking-wider opacity-75">Total Purchases (All Time)</p>
        <p class="text-3xl font-bold mt-1">₹ {{ purchasesStore.totalPurchases.toFixed(2) }}</p>
      </div>
      <UButton label="+ Record Purchase" color="green" size="lg" icon="i-heroicons-plus" @click="purchaseModal?.openCreate()" />
    </div>

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
        <UFormField label="Supplier">
          <USelect v-model="filterParty" :items="partyOptions" size="sm" />
        </UFormField>
        <div class="flex items-end gap-2">
          <UButton label="Filter" color="green" size="sm" />
          <UButton label="Clear" color="gray" variant="outline" size="sm" @click="clearFilters" />
        </div>
      </div>
    </UCard>

    <UCard>
      <template #header>
        <h3 class="font-semibold text-gray-900 dark:text-white">Purchase History</h3>
      </template>
      <UTable
        :rows="filteredPurchases"
        :columns="[
          { key: 'id', label: 'Bill No', sortable: true },
          { key: 'date', label: 'Date', sortable: true },
          { key: 'partyName', label: 'Supplier', sortable: true },
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
            <UTooltip text="Delete">
              <UButton icon="i-heroicons-trash" color="red" variant="ghost" size="2xs" @click="deletePurchase(row.id)" />
            </UTooltip>
          </div>
        </template>
        <template #empty>
          <div class="text-center py-8 text-gray-400">
            <UIcon name="i-heroicons-arrow-trending-down" class="w-12 h-12 mx-auto mb-2" />
            <p>No purchases yet. Record your first purchase!</p>
          </div>
        </template>
      </UTable>
    </UCard>

    <PurchaseFormModal ref="purchaseModal" />
  </div>
</template>
