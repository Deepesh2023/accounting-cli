<script setup lang="ts">
const salesStore = useSalesStore()
const purchasesStore = usePurchasesStore()
const stockStore = useStockStore()
const expensesStore = useExpensesStore()
const ledgerStore = useLedgerStore()
const partiesStore = usePartiesStore()

const totalSales = computed(() =>
  salesStore.sales.reduce((s, sale) => s + sale.totalTaxable, 0)
)

const totalPurchases = computed(() =>
  purchasesStore.purchases.reduce((s, p) => s + p.totalTaxable, 0)
)

const closingStock = computed(() => stockStore.closingStock)

const totalExpenses = computed(() => expensesStore.totalExpenses)

const otherIncome = computed(() => {
  const income = ledgerStore.getBalance('Other Income')
  return Math.abs(income)
})

const capital = computed(() => {
  const cap = ledgerStore.getBalance('Capital')
  return Math.abs(cap) || 100000 // default capital if none
})

const creditors = computed(() =>
  Math.abs(partiesStore.parties.filter(p => p.type === 'CREDITOR').reduce((s, p) => s + p.balance, 0))
)

const debtors = computed(() =>
  Math.abs(partiesStore.parties.filter(p => p.type === 'DEBTOR').reduce((s, p) => s + p.balance, 0))
)

const cashBalance = computed(() => ledgerStore.getBalance('Cash'))
const bankBalance = computed(() => ledgerStore.getBalance('Bank'))
</script>

<template>
  <div class="space-y-8">
    <TradingAccount
      :sales="totalSales"
      :purchases="totalPurchases"
      :closing-stock="closingStock"
    />

    <ProfitLoss
      :gross-profit="Math.max(0, (totalSales + closingStock) - totalPurchases)"
      :gross-loss="Math.max(0, totalPurchases - (totalSales + closingStock))"
      :expenses="totalExpenses"
      :incomes="otherIncome"
    />

    <BalanceSheet
      :capital="capital"
      :net-profit="Math.max(0, ((totalSales + closingStock) - totalPurchases + otherIncome) - totalExpenses)"
      :net-loss="Math.max(0, totalExpenses - ((totalSales + closingStock) - totalPurchases + otherIncome))"
      :creditors="creditors"
      :closing-stock="closingStock"
      :debtors="debtors"
      :cash-balance="cashBalance"
      :bank-balance="bankBalance"
      :fixed-assets="0"
    />
  </div>
</template>
