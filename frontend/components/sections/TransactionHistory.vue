<script setup lang="ts">
const ledgerStore = useLedgerStore()

const cashBalance = computed(() => ledgerStore.getBalance('Cash'))
const bankBalance = computed(() => ledgerStore.getBalance('Bank'))

const transactions = computed(() =>
  [...ledgerStore.entries].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
)
</script>

<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div class="bg-cyan-600 text-white rounded-xl p-5">
        <p class="text-xs font-semibold uppercase tracking-wider opacity-75">Cash Balance</p>
        <p class="text-2xl font-bold mt-1">₹ {{ cashBalance.toFixed(2) }}</p>
      </div>
      <div class="bg-primary text-white rounded-xl p-5">
        <p class="text-xs font-semibold uppercase tracking-wider opacity-75">Bank Balance</p>
        <p class="text-2xl font-bold mt-1">₹ {{ bankBalance.toFixed(2) }}</p>
      </div>
    </div>

    <UCard>
      <template #header>
        <h3 class="font-semibold text-gray-900 dark:text-white">Transaction History</h3>
      </template>

      <UTable
        :rows="transactions"
        :columns="[
          { key: 'index', label: '#' },
          { key: 'date', label: 'Date', sortable: true },
          { key: 'accountName', label: 'Particulars', sortable: true },
          { key: 'debit', label: 'Debit (₹)' },
          { key: 'credit', label: 'Credit (₹)' },
          { key: 'description', label: 'Description' },
        ]"
      >
        <template #index-data="{ index }">
          {{ transactions.length - index }}
        </template>
        <template #debit-data="{ row }">
          <span v-if="row.debit > 0" class="text-red-600 font-medium">{{ row.debit.toFixed(2) }}</span>
          <span v-else class="text-gray-400">-</span>
        </template>
        <template #credit-data="{ row }">
          <span v-if="row.credit > 0" class="text-green-600 font-medium">{{ row.credit.toFixed(2) }}</span>
          <span v-else class="text-gray-400">-</span>
        </template>
        <template #empty>
          <div class="text-center py-8 text-gray-400">
            <UIcon name="i-heroicons-arrow-path" class="w-12 h-12 mx-auto mb-2" />
            <p>No transactions yet.</p>
          </div>
        </template>
      </UTable>
    </UCard>
  </div>
</template>
