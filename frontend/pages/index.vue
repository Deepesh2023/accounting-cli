<script setup lang="ts">
definePageMeta({ title: 'Dashboard' })
</script>

<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold">Financial Module</h1>
      <p class="text-gray-500">Accounting & Inventory Management</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="rounded-xl p-5 bg-blue-600 text-white shadow-sm">
        <h6 class="text-xs uppercase tracking-wider opacity-80 mb-2">TOTAL SALES (ALL TIME)</h6>
        <h2 class="text-2xl font-bold">₹0.00</h2>
      </div>
      <div class="rounded-xl p-5 bg-emerald-600 text-white shadow-sm">
        <h6 class="text-xs uppercase tracking-wider opacity-80 mb-2">TOTAL PURCHASES</h6>
        <h2 class="text-2xl font-bold">₹0.00</h2>
      </div>
      <div class="rounded-xl p-5 bg-cyan-600 text-white shadow-sm">
        <h6 class="text-xs uppercase tracking-wider opacity-80 mb-2">CASH BALANCE</h6>
        <h2 class="text-2xl font-bold">₹0.00</h2>
      </div>
    </div>
    <UCard class="mt-4">
      <div class="text-center text-gray-500 py-12">
        <p class="text-lg">Select a module from the sidebar to get started.</p>
        <p>Use <strong>Sales</strong> to create invoices, <strong>Stock</strong> to manage inventory, and <strong>Reports</strong> for financial statements.</p>
      </div>
    </UCard>
  </div>
</template>

<style scoped>
</style>
