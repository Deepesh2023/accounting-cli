<script setup lang="ts">
definePageMeta({ title: 'Transactions' })

const transactions = ref<any[]>([])
const loading = ref(false)
const cashBalance = ref(0)
const bankBalance = ref(0)

onMounted(loadAll)

async function loadAll() {
  loading.value = true
  try {
    const txns = await api().getTransactionHistory()
    transactions.value = Array.isArray(txns) ? txns : []

    const [cash, bank] = await Promise.all([
      api().getAccountBalance('Cash').catch(() => ({ balance: '0' })),
      api().getAccountBalance('Bank').catch(() => ({ balance: '0' })),
    ])
    cashBalance.value = Number(cash.balance)
    bankBalance.value = Number(bank.balance)
  } finally { loading.value = false }
}

const currency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))

function txnType(row: any) {
  if (row.type) return row.type
  if ((row.debit || 0) > 0) return 'Debit'
  if ((row.credit || 0) > 0) return 'Credit'
  return Number(row.amount || 0) >= 0 ? 'Credit' : 'Debit'
}

function txnAmount(row: any) {
  return Math.abs(Number(row.amount || row.debit || row.credit || 0))
}

function paymentMode(row: any) {
  return row.payment_mode || row.mode || row.paid_by || '-'
}
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Transactions</h1>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
      <div class="rounded-xl p-5 bg-cyan-600 text-white shadow-sm">
        <h6 class="text-xs uppercase tracking-wider opacity-80 mb-2">CASH BALANCE</h6>
        <h2 class="text-2xl font-bold">{{ currency(cashBalance) }}</h2>
      </div>
      <div class="rounded-xl p-5 bg-blue-600 text-white shadow-sm">
        <h6 class="text-xs uppercase tracking-wider opacity-80 mb-2">BANK BALANCE</h6>
        <h2 class="text-2xl font-bold">{{ currency(bankBalance) }}</h2>
      </div>
    </div>
    <UCard>
      <div v-if="loading" class="text-center py-4 text-gray-500">Loading...</div>
      <div v-else-if="!transactions.length" class="text-center py-4 text-gray-500">No transactions found.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">#</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Date</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Particulars</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Type</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Payment Mode</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Amount</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="(t, i) in transactions" :key="t.transaction_id || t.id || i" class="hover:bg-gray-50">
              <td class="px-4 py-3">{{ i + 1 }}</td>
              <td class="px-4 py-3">{{ t.date?.slice(0, 10) }}</td>
              <td class="px-4 py-3">{{ t.particulars || t.description || t.notes || '-' }}</td>
              <td class="px-4 py-3">
                <UBadge :color="txnType(t) === 'Debit' ? 'error' : 'success'">
                  {{ txnType(t) }}
                </UBadge>
              </td>
              <td class="px-4 py-3">{{ paymentMode(t) }}</td>
              <td :class="txnType(t) === 'Debit' ? 'px-4 py-3 text-red-600 font-medium' : 'px-4 py-3 text-emerald-600 font-medium'">
                {{ txnType(t) === 'Debit' ? '-' : '+' }}{{ currency(txnAmount(t)) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UCard>
  </div>
</template>
