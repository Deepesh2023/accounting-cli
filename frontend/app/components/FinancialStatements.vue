<template>
  <div class="space-y-8">
    <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden" style="border-top: 4px solid #3b82f6">
      <div class="px-5 py-4 text-center border-b border-gray-200 dark:border-gray-800">
        <h4 class="text-blue-600 font-bold mb-0">Trading Account</h4>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-800 text-xs uppercase tracking-wider text-gray-500">
              <th class="px-4 py-3 text-left font-semibold" style="width:35%">Particulars (Expenses)</th>
              <th class="px-4 py-3 text-right font-semibold" style="width:15%">Amount (₹)</th>
              <th class="px-4 py-3 text-left font-semibold" style="width:35%">Particulars (Incomes)</th>
              <th class="px-4 py-3 text-right font-semibold" style="width:15%">Amount (₹)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr>
              <td class="px-4 py-2.5">Purchases</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
              <td class="px-4 py-2.5">Sales</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
            </tr>
            <tr>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5">Closing Stock (From Stock List)</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
            </tr>
            <tr class="font-bold text-green-600">
              <td class="px-4 py-2.5">Gross Profit (c/d)</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5"></td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-800 font-bold">
              <td class="px-4 py-2.5 border-b-2 border-gray-900 dark:border-gray-100">Total</td>
              <td class="px-4 py-2.5 text-right font-mono border-b-2 border-gray-900 dark:border-gray-100">0.00</td>
              <td class="px-4 py-2.5 border-b-2 border-gray-900 dark:border-gray-100">Total</td>
              <td class="px-4 py-2.5 text-right font-mono border-b-2 border-gray-900 dark:border-gray-100">0.00</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden" style="border-top: 4px solid #22c55e">
      <div class="px-5 py-4 text-center border-b border-gray-200 dark:border-gray-800">
        <h4 class="text-green-600 font-bold mb-0">Profit & Loss Account</h4>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-800 text-xs uppercase tracking-wider text-gray-500">
              <th class="px-4 py-3 text-left font-semibold" style="width:35%">Particulars (Expenses)</th>
              <th class="px-4 py-3 text-right font-semibold" style="width:15%">Amount (₹)</th>
              <th class="px-4 py-3 text-left font-semibold" style="width:35%">Particulars (Incomes)</th>
              <th class="px-4 py-3 text-right font-semibold" style="width:15%">Amount (₹)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr class="text-green-600 font-semibold">
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5">Gross Profit (b/d)</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
            </tr>
            <tr>
              <td class="px-4 py-2.5">Expenses</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
              <td class="px-4 py-2.5">Other Incomes</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
            </tr>
            <tr class="font-bold text-green-600">
              <td class="px-4 py-2.5">Net Profit</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5"></td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-800 font-bold">
              <td class="px-4 py-2.5 border-b-2 border-gray-900 dark:border-gray-100">Total</td>
              <td class="px-4 py-2.5 text-right font-mono border-b-2 border-gray-900 dark:border-gray-100">0.00</td>
              <td class="px-4 py-2.5 border-b-2 border-gray-900 dark:border-gray-100">Total</td>
              <td class="px-4 py-2.5 text-right font-mono border-b-2 border-gray-900 dark:border-gray-100">0.00</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden" style="border-top: 4px solid #a855f7">
      <div class="px-5 py-4 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
        <h4 class="font-bold" style="color:#a855f7">Balance Sheet</h4>
        <span class="bg-gray-500 text-white text-sm font-semibold py-1.5 px-3 rounded-full shadow-sm">Not Tallied</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 dark:bg-gray-800 text-xs uppercase tracking-wider text-gray-500">
              <th class="px-4 py-3 text-left font-semibold" style="width:35%">Liabilities & Equity</th>
              <th class="px-4 py-3 text-right font-semibold" style="width:15%">Amount (₹)</th>
              <th class="px-4 py-3 text-left font-semibold" style="width:35%">Assets</th>
              <th class="px-4 py-3 text-right font-semibold" style="width:15%">Amount (₹)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
            <tr>
              <td class="px-4 py-2.5">Capital</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
              <td class="px-4 py-2.5">Fixed Assets</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
            </tr>
            <tr>
              <td class="px-4 py-2.5">Add: Net Profit (or Less Loss)</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
              <td class="px-4 py-2.5 font-bold">Current Assets:</td>
              <td class="px-4 py-2.5"></td>
            </tr>
            <tr>
              <td class="px-4 py-2.5 font-bold">Current Liabilities:</td>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5 pl-6">- Stock in Hand</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
            </tr>
            <tr>
              <td class="px-4 py-2.5 pl-6 font-semibold text-gray-500">- Sundry Creditors (To Pay)</td>
              <td class="px-4 py-2.5 text-right font-mono font-semibold text-gray-500">0.00</td>
              <td class="px-4 py-2.5 pl-6 font-semibold text-gray-500">- Sundry Debtors (To Receive)</td>
              <td class="px-4 py-2.5 text-right font-mono font-semibold text-gray-500">0.00</td>
            </tr>
            <tr>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5 pl-6">- Cash Balance</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
            </tr>
            <tr>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5"></td>
              <td class="px-4 py-2.5 pl-6">- Bank Balance</td>
              <td class="px-4 py-2.5 text-right font-mono">0.00</td>
            </tr>
            <tr class="bg-gray-50 dark:bg-gray-800 font-bold text-base">
              <td class="px-4 py-3 border-b-2 border-gray-900 dark:border-gray-100">Total</td>
              <td class="px-4 py-3 text-right font-mono border-b-2 border-gray-900 dark:border-gray-100">0.00</td>
              <td class="px-4 py-3 border-b-2 border-gray-900 dark:border-gray-100">Total</td>
              <td class="px-4 py-3 text-right font-mono border-b-2 border-gray-900 dark:border-gray-100">0.00</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
