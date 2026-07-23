<template>
  <div>
    <div class="flex gap-4 items-center mb-6">
      <div class="w-full max-w-sm">
        <div class="bg-green-600 text-white rounded-xl shadow-lg p-5">
          <p class="opacity-75 uppercase font-bold tracking-wider text-xs">Total Purchases</p>
          <h2 class="text-2xl font-bold mt-2">₹0.00</h2>
        </div>
      </div>
      <div class="flex-1 text-right">
        <UButton color="primary" size="lg" icon="i-heroicons-plus" class="shadow-md px-5">Record Purchase</UButton>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-200 dark:border-gray-800">
        <h5 class="font-bold text-gray-600 dark:text-gray-300">Purchase History</h5>
        <div class="flex gap-3 items-end bg-gray-50 dark:bg-gray-800/50 p-3 rounded-lg mt-3">
          <div class="flex-1">
            <label class="text-xs text-gray-500 mb-1 block">Month</label>
            <input type="month" class="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-800">
          </div>
          <div class="flex-1">
            <label class="text-xs text-gray-500 mb-1 block">Date Range</label>
            <div class="flex gap-2">
              <input type="date" class="flex-1 text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-800">
              <input type="date" class="flex-1 text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-800">
            </div>
          </div>
          <div class="flex-1">
            <label class="text-xs text-gray-500 mb-1 block">Supplier</label>
            <select class="w-full text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1.5 bg-white dark:bg-gray-800">
              <option>All Suppliers</option>
            </select>
          </div>
          <div class="flex gap-2">
            <UButton color="primary" size="sm">Filter</UButton>
            <UButton color="gray" variant="outline" size="sm">Clear</UButton>
          </div>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-800 text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400">
              <th class="px-4 py-3 text-left font-semibold">Bill No</th>
              <th class="px-4 py-3 text-left font-semibold">Date</th>
              <th class="px-4 py-3 text-left font-semibold">Supplier</th>
              <th class="px-4 py-3 text-left font-semibold">Mode</th>
              <th class="px-4 py-3 text-left font-semibold">Status</th>
              <th class="px-4 py-3 text-right font-semibold">Amount (₹)</th>
              <th class="px-4 py-3 text-center font-semibold" style="width:150px">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
              <td colspan="7" class="px-4 py-8 text-center text-gray-400">No purchases yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
