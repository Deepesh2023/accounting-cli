import { createStore } from 'solid-js/store'
import type { Transaction, Party, StockItem, Expense } from './types'

const [transactions, setTransactions] = createStore<Transaction[]>([])
const [partyList, setPartyList] = createStore<Party[]>([])
const [stockList, setStockList] = createStore<StockItem[]>([])
const [expenseList, setExpenseList] = createStore<Expense[]>([])

const indianStates = [
  'Select State', 'Andaman and Nicobar Islands', 'Andhra Pradesh',
  'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
  'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat',
  'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
  'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
  'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
  'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
  'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
]

export {
  transactions,
  setTransactions,
  partyList,
  setPartyList,
  stockList,
  setStockList,
  expenseList,
  setExpenseList,
  indianStates,
}

export const formatMoney = (num: number) => {
  if (isNaN(num)) return '0.00'
  return new Intl.NumberFormat('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num)
}

export function generateInvoiceNo(): string {
  const salesCount = transactions.filter((t) => t.type === 'Sale').length
  return 'INV-' + String(salesCount + 1).padStart(4, '0')
}

let nextId = 1001
export function getNextId(): number {
  return nextId++
}
