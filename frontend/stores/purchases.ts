export interface PurchaseItem {
  id: string
  productId: string
  name: string
  quantity: number
  price: number
  discountAmount: number
  taxableAmount: number
  taxAmount: number
  cgst: number
  sgst: number
  igst: number
  rowTotal: number
}

export interface Purchase {
  id: string
  date: string
  dueDate: string
  partyId: string
  partyName: string
  items: PurchaseItem[]
  totalTaxable: number
  totalTax: number
  grandTotal: number
  paidAmount: number
  balanceAmount: number
  roundOff: boolean
  taxInclusive: boolean
}

export const usePurchasesStore = defineStore('purchases', () => {
  const purchases = ref<Purchase[]>([])

  function add(p: Purchase) {
    purchases.value.push(p)
  }

  function update(id: string, data: Partial<Purchase>) {
    const idx = purchases.value.findIndex(p => p.id === id)
    if (idx !== -1) Object.assign(purchases.value[idx], data)
  }

  function remove(id: string) {
    purchases.value = purchases.value.filter(p => p.id !== id)
  }

  function get(id: string): Purchase | undefined {
    return purchases.value.find(p => p.id === id)
  }

  const totalPurchases = computed(() =>
    purchases.value.reduce((sum, p) => sum + p.grandTotal, 0)
  )

  return { purchases, add, update, remove, get, totalPurchases }
})
