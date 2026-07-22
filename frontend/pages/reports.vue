<script setup lang="ts">
definePageMeta({ title: 'Reports' })

const trading = ref<any>(null)
const pnl = ref<any>(null)
const balanceSheet = ref<any>(null)
const loading = ref(false)

onMounted(loadAll)

async function loadAll() {
  loading.value = true
  try {
    const [t, p, b] = await Promise.all([
      api().getTradingAccount(),
      api().getProfitAndLoss(),
      api().getBalanceSheet(),
    ])
    trading.value = t
    pnl.value = p
    balanceSheet.value = b
  } finally { loading.value = false }
}

const currency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))

function isTallied(section: any) {
  if (!section) return true
  const debitTotal = section.debit_total || section.debit || section.total_debit || 0
  const creditTotal = section.credit_total || section.credit || section.total_credit || 0
  return Math.abs(Number(debitTotal) - Number(creditTotal)) < 0.01
}

function entries(section: any, side: 'debit' | 'credit') {
  if (!section) return []
  return section[`${side}_entries`] || section[`${side}_items`] || section[side] || []
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Financial Reports</h1>
      <button class="btn btn-outline-primary" @click="loadAll">Refresh</button>
    </div>

    <div v-if="loading" class="text-center py-5 text-muted">Loading reports...</div>

    <template v-else>
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="m-0">Trading Account</h5>
          <span v-if="trading" :class="isTallied(trading) ? 'badge bg-success' : 'badge bg-danger'">
            {{ isTallied(trading) ? 'Tallied' : 'Not Tallied' }}
          </span>
        </div>
        <div class="card-body p-0">
          <table class="table mb-0">
            <thead class="table-light">
              <tr><th>Particulars</th><th class="text-end">Amount (₹)</th></tr>
            </thead>
            <tbody>
              <tr v-for="(e, i) in entries(trading, 'debit')" :key="i">
                <td>{{ e.name || e.particulars || e.label }}</td>
                <td class="text-end">{{ currency(e.amount || e.value || 0) }}</td>
              </tr>
              <tr class="table-secondary fw-bold">
                <td>Total (Dr)</td>
                <td class="text-end">{{ currency(trading?.debit_total || trading?.debit || 0) }}</td>
              </tr>
              <tr v-for="(e, i) in entries(trading, 'credit')" :key="'c' + i">
                <td>{{ e.name || e.particulars || e.label }}</td>
                <td class="text-end">{{ currency(e.amount || e.value || 0) }}</td>
              </tr>
              <tr class="table-secondary fw-bold">
                <td>Total (Cr)</td>
                <td class="text-end">{{ currency(trading?.credit_total || trading?.credit || 0) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer text-end" v-if="trading?.gross_profit !== undefined || trading?.gross_loss !== undefined">
          <strong v-if="trading.gross_profit" class="text-success">Gross Profit: {{ currency(trading.gross_profit) }}</strong>
          <strong v-else class="text-danger">Gross Loss: {{ currency(trading.gross_loss) }}</strong>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="m-0">Profit & Loss</h5>
          <span v-if="pnl" :class="isTallied(pnl) ? 'badge bg-success' : 'badge bg-danger'">
            {{ isTallied(pnl) ? 'Tallied' : 'Not Tallied' }}
          </span>
        </div>
        <div class="card-body p-0">
          <table class="table mb-0">
            <thead class="table-light">
              <tr><th>Particulars</th><th class="text-end">Amount (₹)</th></tr>
            </thead>
            <tbody>
              <tr v-for="(e, i) in entries(pnl, 'debit')" :key="i">
                <td>{{ e.name || e.particulars || e.label }}</td>
                <td class="text-end">{{ currency(e.amount || e.value || 0) }}</td>
              </tr>
              <tr class="table-secondary fw-bold">
                <td>Total (Dr)</td>
                <td class="text-end">{{ currency(pnl?.debit_total || pnl?.debit || 0) }}</td>
              </tr>
              <tr v-for="(e, i) in entries(pnl, 'credit')" :key="'c' + i">
                <td>{{ e.name || e.particulars || e.label }}</td>
                <td class="text-end">{{ currency(e.amount || e.value || 0) }}</td>
              </tr>
              <tr class="table-secondary fw-bold">
                <td>Total (Cr)</td>
                <td class="text-end">{{ currency(pnl?.credit_total || pnl?.credit || 0) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer text-end" v-if="pnl?.net_profit !== undefined || pnl?.net_loss !== undefined">
          <strong v-if="pnl.net_profit" class="text-success">Net Profit: {{ currency(pnl.net_profit) }}</strong>
          <strong v-else class="text-danger">Net Loss: {{ currency(pnl.net_loss) }}</strong>
        </div>
      </div>

      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="m-0">Balance Sheet</h5>
          <span v-if="balanceSheet" :class="isTallied(balanceSheet) ? 'badge bg-success' : 'badge bg-danger'">
            {{ isTallied(balanceSheet) ? 'Tallied' : 'Not Tallied' }}
          </span>
        </div>
        <div class="card-body p-0">
          <div class="row g-0">
            <div class="col-12 col-md-6 border-end-md">
              <table class="table mb-0">
                <thead class="table-light"><tr><th>Liabilities</th><th class="text-end">Amount</th></tr></thead>
                <tbody>
                  <tr v-for="(e, i) in entries(balanceSheet, 'debit')" :key="i">
                    <td>{{ e.name || e.particulars || e.label }}</td>
                    <td class="text-end">{{ currency(e.amount || e.value || 0) }}</td>
                  </tr>
                  <tr class="table-secondary fw-bold">
                    <td>Total</td>
                    <td class="text-end">{{ currency(balanceSheet?.debit_total || balanceSheet?.debit || 0) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="col-12 col-md-6">
              <table class="table mb-0">
                <thead class="table-light"><tr><th>Assets</th><th class="text-end">Amount</th></tr></thead>
                <tbody>
                  <tr v-for="(e, i) in entries(balanceSheet, 'credit')" :key="i">
                    <td>{{ e.name || e.particulars || e.label }}</td>
                    <td class="text-end">{{ currency(e.amount || e.value || 0) }}</td>
                  </tr>
                  <tr class="table-secondary fw-bold">
                    <td>Total</td>
                    <td class="text-end">{{ currency(balanceSheet?.credit_total || balanceSheet?.credit || 0) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.card { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-radius: 8px; }
.card-header { background: #fff; border-bottom: 1px solid #eee; font-weight: 600; }
.card-header h5 { font-weight: 700; }
.table th { font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.table td { vertical-align: middle; }
@media (min-width: 768px) {
  .border-end-md { border-right: 1px solid #dee2e6; }
}
</style>
