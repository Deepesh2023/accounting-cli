<template>
  <div>
    <div class="flex gap-4 mb-6">
      <div class="flex-1">
        <div class="bg-cyan-500 text-white rounded-xl shadow-lg p-5">
          <p class="opacity-75 uppercase font-bold tracking-wider text-xs mb-1">Cash Balance</p>
          <h3 class="text-xl font-bold">₹0.00</h3>
        </div>
      </div>
      <div class="flex-1">
        <div class="bg-blue-600 text-white rounded-xl shadow-lg p-5">
          <p class="opacity-75 uppercase font-bold tracking-wider text-xs mb-1">Bank Balance</p>
          <h3 class="text-xl font-bold">₹0.00</h3>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-200 dark:border-gray-800">
        <h5 class="font-bold text-gray-600 dark:text-gray-300">Transaction History</h5>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-800 text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400">
              <th class="px-4 py-3 text-left font-semibold">#</th>
              <th class="px-4 py-3 text-left font-semibold">Date</th>
              <th class="px-4 py-3 text-left font-semibold">Particulars</th>
              <th class="px-4 py-3 text-left font-semibold">Type</th>
              <th class="px-4 py-3 text-left font-semibold">Payment Mode</th>
              <th class="px-4 py-3 text-right font-semibold">Amount (₹)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 cursor-pointer">
              <td colspan="6" class="px-4 py-8 text-center text-gray-400">No transactions yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
