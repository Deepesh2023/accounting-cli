<script setup lang="ts">
import { api } from '~/lib/api/client'

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
    <div class="flex justify-between items-center mb-4">
      <h1 class="m-0">Financial Reports</h1>
      <UButton color="primary" variant="outline" @click="loadAll">Refresh</UButton>
    </div>

    <div v-if="loading" class="text-center py-5 text-gray-500">Loading reports...</div>

    <template v-else>
      <UCard class="mb-4">
        <template #header>
          <div class="flex justify-between items-center">
            <h5 class="m-0 font-bold">Trading Account</h5>
            <UBadge v-if="trading" :color="isTallied(trading) ? 'success' : 'error'" variant="solid">
              {{ isTallied(trading) ? 'Tallied' : 'Not Tallied' }}
            </UBadge>
          </div>
        </template>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Particulars</th>
                <th class="p-3 text-right font-semibold text-sm uppercase tracking-wide">Amount (₹)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(e, i) in entries(trading, 'debit')" :key="i" class="border-b border-gray-200">
                <td class="p-3 align-middle">{{ e.name || e.particulars || e.label }}</td>
                <td class="p-3 text-right align-middle">{{ currency(e.amount || e.value || 0) }}</td>
              </tr>
              <tr class="bg-gray-100 font-bold border-b border-gray-200">
                <td class="p-3 align-middle">Total (Dr)</td>
                <td class="p-3 text-right align-middle">{{ currency(trading?.debit_total || trading?.debit || 0) }}</td>
              </tr>
              <tr v-for="(e, i) in entries(trading, 'credit')" :key="'c' + i" class="border-b border-gray-200">
                <td class="p-3 align-middle">{{ e.name || e.particulars || e.label }}</td>
                <td class="p-3 text-right align-middle">{{ currency(e.amount || e.value || 0) }}</td>
              </tr>
              <tr class="bg-gray-100 font-bold">
                <td class="p-3 align-middle">Total (Cr)</td>
                <td class="p-3 text-right align-middle">{{ currency(trading?.credit_total || trading?.credit || 0) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <template #footer>
          <div class="text-right" v-if="trading?.gross_profit !== undefined || trading?.gross_loss !== undefined">
            <span v-if="trading.gross_profit" class="font-bold text-green-600">Gross Profit: {{ currency(trading.gross_profit) }}</span>
            <span v-else class="font-bold text-red-600">Gross Loss: {{ currency(trading.gross_loss) }}</span>
          </div>
        </template>
      </UCard>

      <UCard class="mb-4">
        <template #header>
          <div class="flex justify-between items-center">
            <h5 class="m-0 font-bold">Profit & Loss</h5>
            <UBadge v-if="pnl" :color="isTallied(pnl) ? 'success' : 'error'" variant="solid">
              {{ isTallied(pnl) ? 'Tallied' : 'Not Tallied' }}
            </UBadge>
          </div>
        </template>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Particulars</th>
                <th class="p-3 text-right font-semibold text-sm uppercase tracking-wide">Amount (₹)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(e, i) in entries(pnl, 'debit')" :key="i" class="border-b border-gray-200">
                <td class="p-3 align-middle">{{ e.name || e.particulars || e.label }}</td>
                <td class="p-3 text-right align-middle">{{ currency(e.amount || e.value || 0) }}</td>
              </tr>
              <tr class="bg-gray-100 font-bold border-b border-gray-200">
                <td class="p-3 align-middle">Total (Dr)</td>
                <td class="p-3 text-right align-middle">{{ currency(pnl?.debit_total || pnl?.debit || 0) }}</td>
              </tr>
              <tr v-for="(e, i) in entries(pnl, 'credit')" :key="'c' + i" class="border-b border-gray-200">
                <td class="p-3 align-middle">{{ e.name || e.particulars || e.label }}</td>
                <td class="p-3 text-right align-middle">{{ currency(e.amount || e.value || 0) }}</td>
              </tr>
              <tr class="bg-gray-100 font-bold">
                <td class="p-3 align-middle">Total (Cr)</td>
                <td class="p-3 text-right align-middle">{{ currency(pnl?.credit_total || pnl?.credit || 0) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <template #footer>
          <div class="text-right" v-if="pnl?.net_profit !== undefined || pnl?.net_loss !== undefined">
            <span v-if="pnl.net_profit" class="font-bold text-green-600">Net Profit: {{ currency(pnl.net_profit) }}</span>
            <span v-else class="font-bold text-red-600">Net Loss: {{ currency(pnl.net_loss) }}</span>
          </div>
        </template>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex justify-between items-center">
            <h5 class="m-0 font-bold">Balance Sheet</h5>
            <UBadge v-if="balanceSheet" :color="isTallied(balanceSheet) ? 'success' : 'error'" variant="solid">
              {{ isTallied(balanceSheet) ? 'Tallied' : 'Not Tallied' }}
            </UBadge>
          </div>
        </template>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-0">
          <div class="md:border-r md:border-gray-200 overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50">
                <tr>
                  <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Liabilities</th>
                  <th class="p-3 text-right font-semibold text-sm uppercase tracking-wide">Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(e, i) in entries(balanceSheet, 'debit')" :key="i" class="border-b border-gray-200">
                  <td class="p-3 align-middle">{{ e.name || e.particulars || e.label }}</td>
                  <td class="p-3 text-right align-middle">{{ currency(e.amount || e.value || 0) }}</td>
                </tr>
                <tr class="bg-gray-100 font-bold">
                  <td class="p-3 align-middle">Total</td>
                  <td class="p-3 text-right align-middle">{{ currency(balanceSheet?.debit_total || balanceSheet?.debit || 0) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50">
                <tr>
                  <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Assets</th>
                  <th class="p-3 text-right font-semibold text-sm uppercase tracking-wide">Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(e, i) in entries(balanceSheet, 'credit')" :key="i" class="border-b border-gray-200">
                  <td class="p-3 align-middle">{{ e.name || e.particulars || e.label }}</td>
                  <td class="p-3 text-right align-middle">{{ currency(e.amount || e.value || 0) }}</td>
                </tr>
                <tr class="bg-gray-100 font-bold">
                  <td class="p-3 align-middle">Total</td>
                  <td class="p-3 text-right align-middle">{{ currency(balanceSheet?.credit_total || balanceSheet?.credit || 0) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </UCard>
    </template>
  </div>
</template>
