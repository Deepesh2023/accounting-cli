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
  const base = '/api'

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
      request<ProductResponse[]>(`/inventory?show_archived=${showArchived}`),
    getProduct: (id: string) =>
      request<ProductResponse>(`/inventory/${id}`),
    createProduct: (data: ProductCreate) =>
      request<ProductResponse>('/inventory', { method: 'POST', body: JSON.stringify(data) }),
    updateProduct: (id: string, data: ProductUpdate) =>
      request<ProductResponse>(`/inventory/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteProduct: (id: string) =>
      request<void>(`/inventory/${id}`, { method: 'DELETE' }),

    // Parties
    listParties: (partyType?: PartyType) =>
      request<PartyResponse[]>(`/parties${partyType ? `?party_type=${partyType}` : ''}`),
    getParty: (id: string) =>
      request<PartyResponse>(`/parties/${id}`),
    createParty: (data: PartyCreate) =>
      request<PartyResponse>('/parties', { method: 'POST', body: JSON.stringify(data) }),
    updateParty: (id: string, data: PartyUpdate) =>
      request<PartyResponse>(`/parties/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteParty: (id: string) =>
      request<void>(`/parties/${id}`, { method: 'DELETE' }),
    adjustPartyBalance: (id: string, data: BalanceAdjust) =>
      request<PartyResponse>(`/parties/${id}/adjust-balance`, { method: 'POST', body: JSON.stringify(data) }),

    // Sales
    listSales: () => request<SaleResponse[]>('/sales'),
    getSale: (id: string) => request<SaleResponse>(`/sales/${id}`),
    createSale: (data: SaleCreate) =>
      request<SaleResponse>('/sales', { method: 'POST', body: JSON.stringify(data) }),
    updateSale: (id: string, data: SaleCreate) =>
      request<SaleResponse>(`/sales/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteSale: (id: string) =>
      request<void>(`/sales/${id}`, { method: 'DELETE' }),
    recordSalePayment: (id: string, data: PaymentCreate) =>
      request<SaleResponse>(`/sales/${id}/payment`, { method: 'POST', body: JSON.stringify(data) }),

    // Purchases
    listPurchases: () => request<PurchaseResponse[]>('/purchases'),
    getPurchase: (id: string) => request<PurchaseResponse>(`/purchases/${id}`),
    createPurchase: (data: PurchaseCreate) =>
      request<PurchaseResponse>('/purchases', { method: 'POST', body: JSON.stringify(data) }),
    updatePurchase: (id: string, data: PurchaseCreate) =>
      request<PurchaseResponse>(`/purchases/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deletePurchase: (id: string) =>
      request<void>(`/purchases/${id}`, { method: 'DELETE' }),
    recordPurchasePayment: (id: string, data: PaymentCreate) =>
      request<PurchaseResponse>(`/purchases/${id}/payment`, { method: 'POST', body: JSON.stringify(data) }),

    // Expenses
    listExpenses: (category?: string) =>
      request<ExpenseResponse[]>(`/expenses${category ? `?category=${category}` : ''}`),
    getExpense: (id: string) => request<ExpenseResponse>(`/expenses/${id}`),
    createExpense: (data: ExpenseCreate) =>
      request<ExpenseResponse>('/expenses', { method: 'POST', body: JSON.stringify(data) }),
    updateExpense: (id: string, data: ExpenseUpdate) =>
      request<ExpenseResponse>(`/expenses/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteExpense: (id: string) =>
      request<void>(`/expenses/${id}`, { method: 'DELETE' }),

    // Quotations
    listQuotations: () => request<QuotationResponse[]>('/quotations'),
    getQuotation: (id: string) => request<QuotationResponse>(`/quotations/${id}`),
    createQuotation: (data: QuotationCreate) =>
      request<QuotationResponse>('/quotations', { method: 'POST', body: JSON.stringify(data) }),
    updateQuotation: (id: string, data: QuotationCreate) =>
      request<QuotationResponse>(`/quotations/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    deleteQuotation: (id: string) =>
      request<void>(`/quotations/${id}`, { method: 'DELETE' }),

    // Reports
    getTradingAccount: () => request<any>('/reports/trading-account'),
    getProfitAndLoss: () => request<any>('/reports/profit-and-loss'),
    getBalanceSheet: () => request<any>('/reports/balance-sheet'),
    getOutstandingReport: () => request<any>('/reports/outstanding'),
    getTransactionHistory: () => request<any>('/reports/transactions'),

    // Company
    getCompany: () => request<CompanyResponse>('/company'),
    updateCompany: (data: CompanyUpdate) =>
      request<CompanyResponse>('/company', { method: 'PUT', body: JSON.stringify(data) }),

    // Ledger
    getLedgerTransactions: (accountName?: string) =>
      request<any[]>(`/ledger/transactions${accountName ? `?account_name=${accountName}` : ''}`),
    getAccountBalance: (accountName: string) =>
      request<{ account: string; balance: string }>(`/ledger/accounts/${accountName}/balance`),
    getGstSummary: () => request<any>('/ledger/gst-summary'),
    getAccountBalances: (accounts: string[]) =>
      request<Record<string, string>>(`/ledger/account-balances?accounts=${accounts.join(',')}`),
  }
}

export const api = useApi
