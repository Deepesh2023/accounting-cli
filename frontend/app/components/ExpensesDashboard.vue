<template>
  <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
    <div class="px-5 py-4 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
      <h5 class="font-bold text-gray-600 dark:text-gray-300">Expenses</h5>
      <UButton color="primary" size="sm" icon="i-heroicons-plus" class="shadow-sm">Add Expense</UButton>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 dark:bg-gray-800 text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400">
            <th class="px-4 py-3 text-left font-semibold">Date</th>
            <th class="px-4 py-3 text-left font-semibold">Category</th>
            <th class="px-4 py-3 text-left font-semibold">Paid By</th>
            <th class="px-4 py-3 text-left font-semibold">Notes</th>
            <th class="px-4 py-3 text-right font-semibold">Amount (₹)</th>
            <th class="px-4 py-3 text-center font-semibold" style="width:100px">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <td colspan="6" class="px-4 py-8 text-center text-gray-400">No expenses recorded.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
