<script setup lang="ts">
const props = defineProps<{
  capital: number
  netProfit: number
  netLoss: number
  creditors: number
  closingStock: number
  debtors: number
  cashBalance: number
  bankBalance: number
  fixedAssets: number
}>()

const totalLiabilities = computed(() => props.capital + (props.netProfit - props.netLoss) + props.creditors)
const totalAssets = computed(() => props.fixedAssets + props.closingStock + props.debtors + props.cashBalance + props.bankBalance)
const isBalanced = computed(() => Math.abs(totalLiabilities.value - totalAssets.value) < 0.01)
</script>

<template>
  <div class="border-t-4 border-purple-500 rounded-xl bg-white dark:bg-gray-800 shadow-sm overflow-hidden">
    <div class="flex items-center justify-between px-4 py-4 border-b border-gray-200 dark:border-gray-700">
      <h4 class="text-lg font-bold text-purple-600">Balance Sheet</h4>
      <UBadge :color="isBalanced ? 'green' : 'red'" :label="isBalanced ? 'Tallied ✓' : 'Not Tallied'" size="md" />
    </div>
    <table class="w-full text-sm">
      <thead>
        <tr class="bg-gray-50 dark:bg-gray-900 text-xs text-gray-500 uppercase">
          <th class="text-left px-4 py-3 w-2/5">Liabilities & Equity</th>
          <th class="text-right px-4 py-3 w-1/5">Amount (₹)</th>
          <th class="text-left px-4 py-3 w-2/5">Assets</th>
          <th class="text-right px-4 py-3 w-1/5">Amount (₹)</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
        <tr>
          <td class="px-4 py-2">Capital</td>
          <td class="text-right px-4 py-2 font-mono">{{ capital.toFixed(2) }}</td>
          <td class="px-4 py-2">Fixed Assets</td>
          <td class="text-right px-4 py-2 font-mono">{{ fixedAssets.toFixed(2) }}</td>
        </tr>
        <tr>
          <td class="px-4 py-2">Add: Net Profit (or Less Loss)</td>
          <td class="text-right px-4 py-2 font-mono">{{ (netProfit - netLoss).toFixed(2) }}</td>
          <td class="px-4 py-2 font-semibold">Current Assets:</td>
          <td></td>
        </tr>
        <tr>
          <td class="px-4 py-2 font-semibold">Current Liabilities:</td>
          <td></td>
          <td class="px-4 py-2 pl-8">- Stock in Hand</td>
          <td class="text-right px-4 py-2 font-mono">{{ closingStock.toFixed(2) }}</td>
        </tr>
        <tr>
          <td class="px-4 py-2 pl-8">- Sundry Creditors</td>
          <td class="text-right px-4 py-2 font-mono">{{ creditors.toFixed(2) }}</td>
          <td class="px-4 py-2 pl-8">- Sundry Debtors</td>
          <td class="text-right px-4 py-2 font-mono">{{ debtors.toFixed(2) }}</td>
        </tr>
        <tr>
          <td></td>
          <td></td>
          <td class="px-4 py-2 pl-8">- Cash Balance</td>
          <td class="text-right px-4 py-2 font-mono">{{ cashBalance.toFixed(2) }}</td>
        </tr>
        <tr>
          <td></td>
          <td></td>
          <td class="px-4 py-2 pl-8">- Bank Balance</td>
          <td class="text-right px-4 py-2 font-mono">{{ bankBalance.toFixed(2) }}</td>
        </tr>
        <tr class="bg-gray-100 dark:bg-gray-700 font-bold text-base">
          <td class="px-4 py-3">Total</td>
          <td class="text-right px-4 py-3 font-mono border-b-2 border-gray-800 dark:border-gray-300">{{ totalLiabilities.toFixed(2) }}</td>
          <td class="px-4 py-3">Total</td>
          <td class="text-right px-4 py-3 font-mono border-b-2 border-gray-800 dark:border-gray-300">{{ totalAssets.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
