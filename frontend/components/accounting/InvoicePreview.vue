<script setup lang="ts">
const props = defineProps<{
  type: 'sale' | 'purchase'
  invoiceNo: string
  date: string
  dueDate: string
  partyName: string
  partyAddress: string
  partyPhone: string
  items: Array<{
    name: string
    quantity: number
    price: number
    taxableAmount: number
    taxAmount: number
    rowTotal: number
  }>
  totalTaxable: number
  totalTax: number
  grandTotal: number
  roundOff: boolean
  amountPaid: number
  balance: number
  terms: string
}>()

const company = useCompanyStore()

const title = props.type === 'sale' ? 'TAX INVOICE' : 'PURCHASE VOUCHER'
const color = props.type === 'sale' ? 'text-primary' : 'text-green-600'
</script>

<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 text-sm">
    <!-- Header -->
    <div class="text-center mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ company.profile.name || 'Your Company' }}</h2>
      <p class="text-gray-500 dark:text-gray-400 text-xs">{{ company.profile.address }}</p>
      <p class="text-gray-500 dark:text-gray-400 text-xs">GSTIN: {{ company.profile.gstin || 'N/A' }}</p>
      <div class="mt-3">
        <span class="text-lg font-bold" :class="color">{{ title }}</span>
      </div>
    </div>

    <!-- Info rows -->
    <div class="grid grid-cols-2 gap-4 mb-4 text-xs">
      <div>
        <p class="text-gray-500">Invoice No: <span class="font-semibold text-gray-800 dark:text-gray-200">{{ invoiceNo }}</span></p>
        <p class="text-gray-500">Date: <span class="font-semibold text-gray-800 dark:text-gray-200">{{ date }}</span></p>
        <p class="text-gray-500">Due Date: <span class="font-semibold text-gray-800 dark:text-gray-200">{{ dueDate }}</span></p>
      </div>
      <div class="text-right">
        <p class="font-semibold text-gray-800 dark:text-gray-200">{{ partyName || 'Walk-in Customer' }}</p>
        <p class="text-gray-500">{{ partyAddress }}</p>
        <p class="text-gray-500">{{ partyPhone }}</p>
      </div>
    </div>

    <!-- Items table -->
    <table class="w-full text-xs mb-4">
      <thead>
        <tr class="border-y border-gray-300 dark:border-gray-600">
          <th class="text-left py-2 font-semibold text-gray-700 dark:text-gray-300">#</th>
          <th class="text-left py-2 font-semibold text-gray-700 dark:text-gray-300">Item</th>
          <th class="text-center py-2 font-semibold text-gray-700 dark:text-gray-300">Qty</th>
          <th class="text-right py-2 font-semibold text-gray-700 dark:text-gray-300">Price</th>
          <th class="text-right py-2 font-semibold text-gray-700 dark:text-gray-300">Taxable</th>
          <th class="text-right py-2 font-semibold text-gray-700 dark:text-gray-300">Tax</th>
          <th class="text-right py-2 font-semibold text-gray-700 dark:text-gray-300">Total</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, i) in items" :key="i" class="border-b border-gray-100 dark:border-gray-700">
          <td class="py-1.5 text-gray-600 dark:text-gray-400">{{ i + 1 }}</td>
          <td class="py-1.5 text-gray-800 dark:text-gray-200">{{ item.name }}</td>
          <td class="py-1.5 text-center text-gray-800 dark:text-gray-200">{{ item.quantity }}</td>
          <td class="py-1.5 text-right text-gray-800 dark:text-gray-200">{{ item.price.toFixed(2) }}</td>
          <td class="py-1.5 text-right text-gray-800 dark:text-gray-200">{{ item.taxableAmount.toFixed(2) }}</td>
          <td class="py-1.5 text-right text-gray-800 dark:text-gray-200">{{ item.taxAmount.toFixed(2) }}</td>
          <td class="py-1.5 text-right font-medium text-gray-800 dark:text-gray-200">{{ item.rowTotal.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Totals -->
    <div class="flex justify-end mb-4">
      <div class="w-64 space-y-1 text-xs">
        <div class="flex justify-between text-gray-600 dark:text-gray-400">
          <span>Total Taxable</span>
          <span>{{ totalTaxable.toFixed(2) }}</span>
        </div>
        <div class="flex justify-between text-gray-600 dark:text-gray-400">
          <span>Total Tax</span>
          <span>{{ totalTax.toFixed(2) }}</span>
        </div>
        <div v-if="roundOff" class="flex justify-between text-gray-600 dark:text-gray-400">
          <span>Round Off</span>
          <span>{{ (grandTotal - (totalTaxable + totalTax)).toFixed(2) }}</span>
        </div>
        <div class="flex justify-between font-bold text-base pt-1 border-t border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white">
          <span>Grand Total</span>
          <span>₹ {{ grandTotal.toFixed(2) }}</span>
        </div>
        <div v-if="amountPaid > 0" class="flex justify-between text-green-600">
          <span>Amount Paid</span>
          <span>{{ amountPaid.toFixed(2) }}</span>
        </div>
        <div v-if="balance > 0" class="flex justify-between font-semibold text-red-600">
          <span>Balance Due</span>
          <span>{{ balance.toFixed(2) }}</span>
        </div>
      </div>
    </div>

    <!-- Terms -->
    <div v-if="terms" class="border-t border-gray-300 dark:border-gray-600 pt-3 mt-2">
      <p class="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Terms & Conditions</p>
      <p class="text-xs text-gray-500 dark:text-gray-400 whitespace-pre-line">{{ terms }}</p>
    </div>

    <!-- Signature -->
    <div class="mt-8 pt-4 border-t border-gray-300 dark:border-gray-600 text-xs text-right text-gray-500">
      <p class="font-semibold text-gray-700 dark:text-gray-300">Authorized Signature</p>
    </div>
  </div>
</template>
