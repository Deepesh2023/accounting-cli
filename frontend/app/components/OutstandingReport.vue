<template>
  <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
    <div class="px-5 py-4 border-b border-gray-200 dark:border-gray-800">
      <h5 class="font-bold text-red-600 dark:text-red-400">Outstanding & Due Report</h5>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 dark:bg-gray-800 text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400">
            <th class="px-4 py-3 text-left font-semibold">Ref No</th>
            <th class="px-4 py-3 text-left font-semibold">Date</th>
            <th class="px-4 py-3 text-left font-semibold">Party</th>
            <th class="px-4 py-3 text-left font-semibold">Type</th>
            <th class="px-4 py-3 text-right font-semibold">Total Amount (₹)</th>
            <th class="px-4 py-3 text-right font-semibold">Balance Due (₹)</th>
            <th class="px-4 py-3 text-left font-semibold">Due Date</th>
            <th class="px-4 py-3 text-left font-semibold">Overdue Status</th>
            <th class="px-4 py-3 text-center font-semibold" style="width:100px">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <td colspan="9" class="px-4 py-8 text-center text-gray-400">No outstanding items.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
