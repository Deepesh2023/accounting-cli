<script setup lang="ts">
const props = defineProps<{
  sales: number
  purchases: number
  closingStock: number
}>()

const grossProfit = computed(() => Math.max(0, (props.sales + props.closingStock) - props.purchases))
const grossLoss = computed(() => Math.max(0, props.purchases - (props.sales + props.closingStock)))
const isProfit = computed(() => grossProfit.value > 0)

const totalDr = computed(() => isProfit.value ? props.purchases + grossProfit.value : props.purchases)
const totalCr = computed(() => isProfit.value ? props.sales + props.closingStock : props.sales + props.closingStock + grossLoss.value)
</script>

<template>
  <div class="border-t-4 border-blue-500 rounded-xl bg-white dark:bg-gray-800 shadow-sm overflow-hidden">
    <div class="text-center py-4 border-b border-gray-200 dark:border-gray-700">
      <h4 class="text-lg font-bold text-blue-600">Trading Account</h4>
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
        <tr>
          <td class="px-4 py-2">Purchases</td>
          <td class="text-right px-4 py-2 font-mono">{{ purchases.toFixed(2) }}</td>
          <td class="px-4 py-2">Sales</td>
          <td class="text-right px-4 py-2 font-mono">{{ sales.toFixed(2) }}</td>
        </tr>
        <tr>
          <td></td>
          <td></td>
          <td class="px-4 py-2">Closing Stock</td>
          <td class="text-right px-4 py-2 font-mono">{{ closingStock.toFixed(2) }}</td>
        </tr>
        <tr v-if="isProfit" class="bg-green-50 dark:bg-green-900/20 font-semibold text-green-700 dark:text-green-400">
          <td class="px-4 py-2">Gross Profit (c/d)</td>
          <td class="text-right px-4 py-2 font-mono">{{ grossProfit.toFixed(2) }}</td>
          <td></td>
          <td></td>
        </tr>
        <tr v-else class="bg-red-50 dark:bg-red-900/20 font-semibold text-red-700 dark:text-red-400">
          <td></td>
          <td></td>
          <td class="px-4 py-2">Gross Loss (c/d)</td>
          <td class="text-right px-4 py-2 font-mono">{{ grossLoss.toFixed(2) }}</td>
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
