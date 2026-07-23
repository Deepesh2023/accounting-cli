<template>
  <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
    <div class="px-5 py-4 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
      <h5 class="font-bold text-gray-600 dark:text-gray-300">Stock Inventory</h5>
      <UButton color="primary" size="sm" icon="i-heroicons-plus" class="shadow-sm">Add Stock</UButton>
    </div>
    <div class="mx-4 mt-3">
      <div class="bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-sm p-2 rounded">
        <strong>Tip:</strong> Double-click a row to edit. Right-click a row to delete.
      </div>
    </div>
    <div class="overflow-x-auto mt-2">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 dark:bg-gray-800 text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400">
            <th class="px-4 py-3 text-left font-semibold" style="width:50px">#</th>
            <th class="px-4 py-3 text-left font-semibold">Item Code</th>
            <th class="px-4 py-3 text-left font-semibold">Name</th>
            <th class="px-4 py-3 text-right font-semibold">Qty</th>
            <th class="px-4 py-3 text-left font-semibold">Unit</th>
            <th class="px-4 py-3 text-right font-semibold">Price (₹)</th>
            <th class="px-4 py-3 text-right font-semibold">Total Value (₹)</th>
            <th class="px-4 py-3 text-center font-semibold" style="width:120px">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
          <tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <td colspan="8" class="px-4 py-8 text-center text-gray-400">No stock items added yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
