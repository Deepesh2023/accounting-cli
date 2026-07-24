export interface SaleItem {
  item_id: string
  name: string
  qty: number
  unit: string
  price: number
  disc_perc: number
  disc_amt: number
  tax_perc: number
  tax_amt: number
  total: number
}

export interface SaleDetails {
  customer_id: string
  invoice_no: string
  phone: string
  address: string
  state_of_supply: string
  due_date: string
  items: SaleItem[]
  paid_amount: number
  balance_amount: number
  payment_status: 'Paid' | 'Partial' | 'Unpaid'
  is_roundoff: boolean
  price_type: 'Without Tax' | 'With Tax'
  terms: string
}

export interface PurchaseItem {
  item_id: string
  name: string
  qty: number
  unit: string
  price: number
  disc_perc: number
  disc_amt: number
  tax_perc: number
  tax_amt: number
  total: number
}

export interface PurchaseDetails {
  supplier_id: string
  bill_no: string
  phone: string
  address: string
  state_of_supply: string
  due_date: string
  items: PurchaseItem[]
  paid_amount: number
  balance_amount: number
  payment_status: 'Paid' | 'Partial' | 'Unpaid'
  is_roundoff: boolean
  price_type: 'Without Tax' | 'With Tax'
  terms: string
}

export interface Transaction {
  id: number
  type: 'Sale' | 'Purchase' | 'Expense' | 'Income' | 'Capital' | 'Asset'
  date: string
  particulars: string
  payment_mode: 'Credit' | 'Cash' | 'Bank'
  amount: number
  sale_details?: SaleDetails
  purchase_details?: PurchaseDetails
}

export interface Party {
  id: number
  name: string
  phone: string
  address: string
  state: string
  type: 'Receive' | 'Pay'
  balance: number
}

export interface QuotationItem {
  item_id: string
  qty: number
  price: number
  tax: number
}

export interface Quotation {
  id: number
  quote_no: string
  date: string
  customer_id: string
  customer_name: string
  total: number
  items: QuotationItem[]
}

export interface Expense {
  id: number
  date: string
  category: string
  paid_by: string
  amount: number
  notes: string
}

export interface CompanyData {
  name: string
  type: string
  phone: string
  category: string
  gstin: string
  state: string
  email: string
  pincode: string
  start_date: string
  address: string
  netting_enabled: boolean
  logo: string
  qr: string
  gst_rates: number[]
}

export interface LedgerEntry {
  date: string
  type: 'DR' | 'CR'
  amount: number
  ref: number
  narration: string
}

export interface StockItem {
  id: number
  name: string
  item_code: string
  qty: number
  unit: string
  price: number
}
