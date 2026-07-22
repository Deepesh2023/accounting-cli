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
  const amt = Number(row.amount || row.debit || row.credit || 0)
  if (row.type) return row.type
  if ((row.debit || 0) > 0) return 'Debit'
  if ((row.credit || 0) > 0) return 'Credit'
  return amt >= 0 ? 'Credit' : 'Debit'
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
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Transactions</h1>
    </div>
    <div class="row g-3 mb-4">
      <div class="col-12 col-md-6">
        <div class="stat-card bg-info text-white">
          <h6>CASH BALANCE</h6>
          <h2>{{ currency(cashBalance) }}</h2>
        </div>
      </div>
      <div class="col-12 col-md-6">
        <div class="stat-card bg-primary text-white">
          <h6>BANK BALANCE</h6>
          <h2>{{ currency(bankBalance) }}</h2>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-4 text-muted">Loading...</div>
        <div v-else-if="!transactions.length" class="text-center py-4 text-muted">No transactions found.</div>
        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr><th>#</th><th>Date</th><th>Particulars</th><th>Type</th><th>Payment Mode</th><th>Amount</th></tr>
            </thead>
            <tbody>
              <tr v-for="(t, i) in transactions" :key="t.transaction_id || t.id || i">
                <td>{{ i + 1 }}</td>
                <td>{{ t.date?.slice(0, 10) }}</td>
                <td>{{ t.particulars || t.description || t.notes || '-' }}</td>
                <td>
                  <span :class="txnType(t) === 'Debit' ? 'badge bg-danger' : 'badge bg-success'">
                    {{ txnType(t) }}
                  </span>
                </td>
                <td>{{ paymentMode(t) }}</td>
                <td :class="txnType(t) === 'Debit' ? 'text-danger' : 'text-success'">
                  {{ txnType(t) === 'Debit' ? '-' : '+' }}{{ currency(txnAmount(t)) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stat-card { border-radius: 12px; padding: 20px 24px; border: none; }
.stat-card h6 { opacity: 0.8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 8px; }
.stat-card h2 { margin: 0; font-weight: 700; }
.card { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-radius: 8px; }
.table th { font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.table td { vertical-align: middle; }
</style>
