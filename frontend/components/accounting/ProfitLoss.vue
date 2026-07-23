<script setup lang="ts">
const props = defineProps<{
  grossProfit: number
  grossLoss: number
  expenses: number
  incomes: number
}>()

const netProfit = computed(() => Math.max(0, (props.grossProfit + props.incomes) - props.expenses))
const netLoss = computed(() => Math.max(0, props.expenses - (props.grossProfit + props.incomes)))
const isProfit = computed(() => netProfit.value > 0)

const totalDr = computed(() => isProfit.value ? props.expenses + netProfit.value : props.expenses)
const totalCr = computed(() => isProfit.value ? props.incomes + props.grossProfit : props.incomes + props.grossProfit + netLoss.value)
</script>

<template>
  <div class="border-t-4 border-green-500 rounded-xl bg-white dark:bg-gray-800 shadow-sm overflow-hidden">
    <div class="text-center py-4 border-b border-gray-200 dark:border-gray-700">
      <h4 class="text-lg font-bold text-green-600">Profit & Loss Account</h4>
    </div>
    <table class="w-full text-sm">
      <thead>
        <tr class="bg-gray-50 dark:bg-gray-900 text-xs text-gray-500 uppercase">
          <th class="text-left px-4 py-3 w-2/5">Particulars (Expenses)</th>
          <th class="text-right px-4 py-3 w-1/5">Amount (₹)</th>
          <th class="text-left px-4 py-3 w-2/5">Particulars (Incomes)</th>
          <th class="text-right px-4 py-3 w-1/5">Amount (₹)</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
        <tr v-if="props.grossProfit > 0" class="text-green-700 dark:text-green-400">
          <td></td>
          <td></td>
          <td class="px-4 py-2">Gross Profit (b/d)</td>
          <td class="text-right px-4 py-2 font-mono">{{ props.grossProfit.toFixed(2) }}</td>
        </tr>
        <tr v-else class="text-red-700 dark:text-red-400">
          <td class="px-4 py-2">Gross Loss (b/d)</td>
          <td class="text-right px-4 py-2 font-mono">{{ props.grossLoss.toFixed(2) }}</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td class="px-4 py-2">Expenses</td>
          <td class="text-right px-4 py-2 font-mono">{{ props.expenses.toFixed(2) }}</td>
          <td class="px-4 py-2">Other Incomes</td>
          <td class="text-right px-4 py-2 font-mono">{{ props.incomes.toFixed(2) }}</td>
        </tr>
        <tr v-if="isProfit" class="bg-green-50 dark:bg-green-900/20 font-semibold text-green-700 dark:text-green-400">
          <td class="px-4 py-2">Net Profit</td>
          <td class="text-right px-4 py-2 font-mono">{{ netProfit.toFixed(2) }}</td>
          <td></td>
          <td></td>
        </tr>
        <tr v-else class="bg-red-50 dark:bg-red-900/20 font-semibold text-red-700 dark:text-red-400">
          <td></td>
          <td></td>
          <td class="px-4 py-2">Net Loss</td>
          <td class="text-right px-4 py-2 font-mono">{{ netLoss.toFixed(2) }}</td>
        </tr>
        <tr class="bg-gray-100 dark:bg-gray-700 font-bold">
          <td class="px-4 py-3">Total</td>
          <td class="text-right px-4 py-3 font-mono border-b-2 border-gray-800 dark:border-gray-300">{{ totalDr.toFixed(2) }}</td>
          <td class="px-4 py-3">Total</td>
          <td class="text-right px-4 py-3 font-mono border-b-2 border-gray-800 dark:border-gray-300">{{ totalCr.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
