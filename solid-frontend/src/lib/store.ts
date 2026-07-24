import { createStore } from 'solid-js/store'
import type { Transaction, Party, StockItem, Quotation, Expense, CompanyData, LedgerEntry } from './types'

const [transactions, setTransactions] = createStore<Transaction[]>([])
const [partyList, setPartyList] = createStore<Party[]>([])
const [stockList, setStockList] = createStore<StockItem[]>([])
const [quotationList, setQuotationList] = createStore<Quotation[]>([])
const [expenseList, setExpenseList] = createStore<Expense[]>([])
const [ledgerList, setLedgerList] = createStore<Record<string, LedgerEntry[]>>({})
const [companyData, setCompanyData] = createStore<CompanyData>({
  name: '',
  type: '',
  phone: '',
  category: '',
  gstin: '',
  state: '',
  email: '',
  pincode: '',
  start_date: '',
  address: '',
  netting_enabled: false,
  logo: '',
  qr: '',
})

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
  quotationList,
  setQuotationList,
  expenseList,
  setExpenseList,
  ledgerList,
  setLedgerList,
  companyData,
  setCompanyData,
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

export function updateLedger(
  date: string,
  account: string,
  type: 'DR' | 'CR',
  amount: number,
  ref: number,
  narration: string,
) {
  const entry: LedgerEntry = { date, type, amount, ref, narration }
  const existing = ledgerList[account] ?? []
  setLedgerList(account, [...existing, entry])
}

export function deleteLedgerByRef(ref: number) {
  for (const account of Object.keys(ledgerList)) {
    setLedgerList(account, (entries) => entries.filter((e) => e.ref !== ref))
  }
}
