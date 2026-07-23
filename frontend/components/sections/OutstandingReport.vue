<script setup lang="ts">
const salesStore = useSalesStore()
const purchasesStore = usePurchasesStore()

const outstanding = computed(() => {
  const items: Array<{
    refNo: string
    date: string
    party: string
    type: string
    totalAmount: number
    balanceDue: number
    dueDate: string
    overdue: boolean
  }> = []

  for (const s of salesStore.sales) {
    if (s.balanceAmount > 0) {
      items.push({
        refNo: s.id,
        date: s.date,
        party: s.partyName,
        type: 'Sale',
        totalAmount: s.grandTotal,
        balanceDue: s.balanceAmount,
        dueDate: s.dueDate,
        overdue: s.dueDate ? new Date(s.dueDate) < new Date() : false,
      })
    }
  }

  for (const p of purchasesStore.purchases) {
    if (p.balanceAmount > 0) {
      items.push({
        refNo: p.id,
        date: p.date,
        party: p.partyName,
        type: 'Purchase',
        totalAmount: p.grandTotal,
        balanceDue: p.balanceAmount,
        dueDate: p.dueDate,
        overdue: p.dueDate ? new Date(p.dueDate) < new Date() : false,
      })
    }
  }

  return items.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
})
</script>

<template>
  <UCard>
    <template #header>
      <h3 class="font-semibold text-red-600">Outstanding & Due Report</h3>
    </template>

    <UTable
      :rows="outstanding"
      :columns="[
        { key: 'refNo', label: 'Ref No' },
        { key: 'date', label: 'Date', sortable: true },
        { key: 'party', label: 'Party', sortable: true },
        { key: 'type', label: 'Type' },
        { key: 'totalAmount', label: 'Total Amount (₹)', sortable: true },
        { key: 'balanceDue', label: 'Balance Due (₹)', sortable: true },
        { key: 'dueDate', label: 'Due Date' },
        { key: 'overdue', label: 'Overdue Status' },
      ]"
    >
      <template #totalAmount-data="{ row }">
        ₹ {{ row.totalAmount.toFixed(2) }}
      </template>
      <template #balanceDue-data="{ row }">
        <span class="font-medium text-red-600">₹ {{ row.balanceDue.toFixed(2) }}</span>
      </template>
      <template #overdue-data="{ row }">
        <UBadge v-if="row.overdue" color="red" variant="solid">Overdue</UBadge>
        <UBadge v-else color="green" variant="soft">On Time</UBadge>
      </template>
      <template #empty>
        <div class="text-center py-8 text-gray-400">
          <UIcon name="i-heroicons-exclamation-triangle" class="w-12 h-12 mx-auto mb-2" />
          <p>No outstanding amounts!</p>
        </div>
      </template>
    </UTable>
  </UCard>
</template>
