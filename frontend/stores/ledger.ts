export interface LedgerEntry {
  id: string
  date: string
  accountName: string
  debit: number
  credit: number
  transactionId: string
  description: string
}

export const useLedgerStore = defineStore('ledger', () => {
  const entries = ref<LedgerEntry[]>([])

  function addEntries(transactionId: string, items: Omit<LedgerEntry, 'id' | 'date'>[]) {
    for (const item of items) {
      entries.value.push({
        ...item,
        id: crypto.randomUUID(),
        date: new Date().toISOString(),
        transactionId,
      })
    }
  }

  function clearTransaction(transactionId: string) {
    entries.value = entries.value.filter(e => e.transactionId !== transactionId)
  }

  const getBalance = (account: string) =>
    entries.value
      .filter(e => e.accountName === account)
      .reduce((sum, e) => sum + e.debit - e.credit, 0)

  return { entries, addEntries, clearTransaction, getBalance }
})
