import { createStore } from 'solid-js/store'
import type { Transaction, Party, Quotation, Expense, CompanyData, LedgerEntry } from './types'
import type { components } from './api/schema'

const [transactions, setTransactions] = createStore<Transaction[]>([])
const [partyList, setPartyList] = createStore<Party[]>([])
const [stockList, setStockList] = createStore<components['schemas']['ProductResponse'][]>([])
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
  gst_rates: [0, 5, 12, 18, 28],
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

const STORAGE_PREFIX = 'solid_'

function loadStateFromLocalStorage() {
  try {
    const trans = localStorage.getItem(STORAGE_PREFIX + 'transactions')
    if (trans) setTransactions(JSON.parse(trans))
    const parties = localStorage.getItem(STORAGE_PREFIX + 'partyList')
    if (parties) setPartyList(JSON.parse(parties))
    const stock = localStorage.getItem(STORAGE_PREFIX + 'stockList')
    if (stock) setStockList(JSON.parse(stock))
    const expenses = localStorage.getItem(STORAGE_PREFIX + 'expenseList')
    if (expenses) setExpenseList(JSON.parse(expenses))
    const quotes = localStorage.getItem(STORAGE_PREFIX + 'quotationList')
    if (quotes) setQuotationList(JSON.parse(quotes))
    const ledger = localStorage.getItem(STORAGE_PREFIX + 'ledgerList')
    if (ledger) setLedgerList(JSON.parse(ledger))
    const company = localStorage.getItem(STORAGE_PREFIX + 'companyData')
    if (company) setCompanyData(JSON.parse(company))
  } catch (e) {
    console.error('Failed to load state from localStorage', e)
  }
}

if (typeof localStorage !== 'undefined') {
  loadStateFromLocalStorage()
}

export function persistState() {
  localStorage.setItem(STORAGE_PREFIX + 'transactions', JSON.stringify(transactions))
  localStorage.setItem(STORAGE_PREFIX + 'partyList', JSON.stringify(partyList))
  localStorage.setItem(STORAGE_PREFIX + 'stockList', JSON.stringify(stockList))
  localStorage.setItem(STORAGE_PREFIX + 'expenseList', JSON.stringify(expenseList))
  localStorage.setItem(STORAGE_PREFIX + 'quotationList', JSON.stringify(quotationList))
  localStorage.setItem(STORAGE_PREFIX + 'ledgerList', JSON.stringify(ledgerList))
  localStorage.setItem(STORAGE_PREFIX + 'companyData', JSON.stringify(companyData))
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
