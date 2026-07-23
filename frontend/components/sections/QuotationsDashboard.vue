<script setup lang="ts">
const store = useQuotationsStore()
const partiesStore = usePartiesStore()
const quoteModal = ref<InstanceType<typeof QuotationFormModal>>()

function deleteQuote(id: string) {
  store.remove(id)
}
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-gray-900 dark:text-white">Quotation History</h3>
        <UButton label="+ Add Quotation" color="primary" size="sm" @click="quoteModal?.openCreate()" />
      </div>
    </template>

    <UTable
      :rows="store.quotations"
      :columns="[
        { key: 'id', label: 'ID' },
        { key: 'date', label: 'Date', sortable: true },
        { key: 'partyName', label: 'Customer', sortable: true },
        { key: 'totalAmount', label: 'Total Amount', sortable: true },
        { key: 'status', label: 'Status' },
        { key: 'actions', label: 'Actions' },
      ]"
    >
      <template #totalAmount-data="{ row }">
        <span class="font-medium">₹ {{ row.totalAmount.toFixed(2) }}</span>
      </template>
      <template #status-data="{ row }">
        <UBadge :color="row.status === 'Draft' ? 'yellow' : row.status === 'Sent' ? 'blue' : 'green'" variant="soft">
          {{ row.status }}
        </UBadge>
      </template>
      <template #actions-data="{ row }">
        <div class="flex gap-1">
          <UTooltip text="Delete">
            <UButton icon="i-heroicons-trash" color="red" variant="ghost" size="2xs" @click="deleteQuote(row.id)" />
          </UTooltip>
        </div>
      </template>
      <template #empty>
        <div class="text-center py-8 text-gray-400">
          <UIcon name="i-heroicons-document-text" class="w-12 h-12 mx-auto mb-2" />
          <p>No quotations yet.</p>
        </div>
      </template>
    </UTable>

    <QuotationFormModal ref="quoteModal" />
  </UCard>
</template>
