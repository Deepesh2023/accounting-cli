import type { paths, components } from './schema'

type OpKey = keyof paths
type GetOp<P extends OpKey> = paths[P] extends { get: infer G } ? G : never
type PostOp<P extends OpKey> = paths[P] extends { post: infer G } ? G : never
type PutOp<P extends OpKey> = paths[P] extends { put: infer G } ? G : never
type DeleteOp<P extends OpKey> = paths[P] extends { delete: infer G } ? G : never

type JsonResponse<T> = T extends { content: { 'application/json': infer J } } ? J : never

export type ProductResponse = components['schemas']['ProductResponse']
export type ProductCreate = components['schemas']['ProductCreate']
export type ProductUpdate = components['schemas']['ProductUpdate']
export type PartyResponse = components['schemas']['PartyResponse']
export type PartyCreate = components['schemas']['PartyCreate']
export type PartyUpdate = components['schemas']['PartyUpdate']
export type PartyType = components['schemas']['PartyType']
export type SaleResponse = components['schemas']['SaleResponse']
export type SaleCreate = components['schemas']['SaleCreate']
export type SaleItemInput = components['schemas']['SaleItemInput']
export type PurchaseResponse = components['schemas']['PurchaseResponse']
export type PurchaseCreate = components['schemas']['PurchaseCreate']
export type PurchaseItemInput = components['schemas']['PurchaseItemInput']
export type ExpenseResponse = components['schemas']['ExpenseResponse']
export type ExpenseCreate = components['schemas']['ExpenseCreate']
export type ExpenseUpdate = components['schemas']['ExpenseUpdate']
export type QuotationResponse = components['schemas']['QuotationResponse']
export type QuotationCreate = components['schemas']['QuotationCreate']
export type QuotationItemInput = components['schemas']['QuotationItemInput']
export type CompanyResponse = components['schemas']['CompanyResponse']
export type CompanyUpdate = components['schemas']['CompanyUpdate']
export type PaymentCreate = components['schemas']['PaymentCreate']
export type BalanceAdjust = components['schemas']['BalanceAdjust']

function useApi() {
  const config = useRuntimeConfig()
  const base = config.public.apiBase

  async function request<T>(path: string, opts: RequestInit = {}): Promise<T> {
    const res = await fetch(`${base}${path}`, {
      headers: { 'Content-Type': 'application/json', ...opts.headers },
      ...opts,
    })
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      throw new Error((body as any).detail || `HTTP ${res.status}`)
    }
    if (res.status === 204) return undefined as T
    return res.json()
  }

  return {
    // Inventory
    listProducts: (showArchived = false) =>
      request<ProductResponse[]>(`/api/inventory?show_archived=${showArchived}`),
    getProduct: (id: string) =>
      request<ProductResponse>(`/api/inventory/${id}`),
    createProduct: (data: ProductCreate) =>
      request<ProductResponse>('/api/inventory', { method: 'POST', body: JSON.stringify(data) }),
    updateProduct: (id: string, data: ProductUpdate) =>
      request<ProductResponse>(`/api/inventory/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteProduct: (id: string) =>
      request<void>(`/api/inventory/${id}`, { method: 'DELETE' }),

    // Parties
    listParties: (partyType?: PartyType) =>
      request<PartyResponse[]>(`/api/parties${partyType ? `?party_type=${partyType}` : ''}`),
    getParty: (id: string) =>
      request<PartyResponse>(`/api/parties/${id}`),
    createParty: (data: PartyCreate) =>
      request<PartyResponse>('/api/parties', { method: 'POST', body: JSON.stringify(data) }),
    updateParty: (id: string, data: PartyUpdate) =>
      request<PartyResponse>(`/api/parties/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteParty: (id: string) =>
      request<void>(`/api/parties/${id}`, { method: 'DELETE' }),
    adjustPartyBalance: (id: string, data: BalanceAdjust) =>
      request<PartyResponse>(`/api/parties/${id}/adjust-balance`, { method: 'POST', body: JSON.stringify(data) }),

    // Sales
    listSales: () => request<SaleResponse[]>('/api/sales'),
    getSale: (id: string) => request<SaleResponse>(`/api/sales/${id}`),
    createSale: (data: SaleCreate) =>
      request<SaleResponse>('/api/sales', { method: 'POST', body: JSON.stringify(data) }),
    updateSale: (id: string, data: SaleCreate) =>
      request<SaleResponse>(`/api/sales/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteSale: (id: string) =>
      request<void>(`/api/sales/${id}`, { method: 'DELETE' }),
    recordSalePayment: (id: string, data: PaymentCreate) =>
      request<SaleResponse>(`/api/sales/${id}/payment`, { method: 'POST', body: JSON.stringify(data) }),

    // Purchases
    listPurchases: () => request<PurchaseResponse[]>('/api/purchases'),
    getPurchase: (id: string) => request<PurchaseResponse>(`/api/purchases/${id}`),
    createPurchase: (data: PurchaseCreate) =>
      request<PurchaseResponse>('/api/purchases', { method: 'POST', body: JSON.stringify(data) }),
    updatePurchase: (id: string, data: PurchaseCreate) =>
      request<PurchaseResponse>(`/api/purchases/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deletePurchase: (id: string) =>
      request<void>(`/api/purchases/${id}`, { method: 'DELETE' }),
    recordPurchasePayment: (id: string, data: PaymentCreate) =>
      request<PurchaseResponse>(`/api/purchases/${id}/payment`, { method: 'POST', body: JSON.stringify(data) }),

    // Expenses
    listExpenses: (category?: string) =>
      request<ExpenseResponse[]>(`/api/expenses${category ? `?category=${category}` : ''}`),
    getExpense: (id: string) => request<ExpenseResponse>(`/api/expenses/${id}`),
    createExpense: (data: ExpenseCreate) =>
      request<ExpenseResponse>('/api/expenses', { method: 'POST', body: JSON.stringify(data) }),
    updateExpense: (id: string, data: ExpenseUpdate) =>
      request<ExpenseResponse>(`/api/expenses/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteExpense: (id: string) =>
      request<void>(`/api/expenses/${id}`, { method: 'DELETE' }),

    // Quotations
    listQuotations: () => request<QuotationResponse[]>('/api/quotations'),
    getQuotation: (id: string) => request<QuotationResponse>(`/api/quotations/${id}`),
    createQuotation: (data: QuotationCreate) =>
      request<QuotationResponse>('/api/quotations', { method: 'POST', body: JSON.stringify(data) }),
    updateQuotation: (id: string, data: QuotationCreate) =>
      request<QuotationResponse>(`/api/quotations/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteQuotation: (id: string) =>
      request<void>(`/api/quotations/${id}`, { method: 'DELETE' }),

    // Reports
    getTradingAccount: () => request<any>('/api/reports/trading-account'),
    getProfitAndLoss: () => request<any>('/api/reports/profit-and-loss'),
    getBalanceSheet: () => request<any>('/api/reports/balance-sheet'),
    getOutstandingReport: () => request<any>('/api/reports/outstanding'),
    getTransactionHistory: () => request<any>('/api/reports/transactions'),

    // Company
    getCompany: () => request<CompanyResponse>('/api/company'),
    updateCompany: (data: CompanyUpdate) =>
      request<CompanyResponse>('/api/company', { method: 'PUT', body: JSON.stringify(data) }),

    // Ledger
    getLedgerTransactions: (accountName?: string) =>
      request<any[]>(`/api/ledger/transactions${accountName ? `?account_name=${accountName}` : ''}`),
    getAccountBalance: (accountName: string) =>
      request<{ account: string; balance: string }>(`/api/ledger/accounts/${accountName}/balance`),
    getGstSummary: () => request<any>('/api/ledger/gst-summary'),
    getAccountBalances: (accounts: string[]) =>
      request<Record<string, string>>(`/api/ledger/account-balances?accounts=${accounts.join(',')}`),
  }
}

export const api = useApi
