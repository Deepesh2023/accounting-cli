export interface SaleItem {
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

export interface Sale {
  id: string
  date: string
  dueDate: string
  partyId: string
  partyName: string
  items: SaleItem[]
  totalTaxable: number
  totalTax: number
  grandTotal: number
  paidAmount: number
  balanceAmount: number
  roundOff: boolean
  taxInclusive: boolean
}

export const useSalesStore = defineStore('sales', () => {
  const sales = ref<Sale[]>([])

  function add(s: Sale) {
    sales.value.push(s)
  }

  function update(id: string, data: Partial<Sale>) {
    const idx = sales.value.findIndex(s => s.id === id)
    if (idx !== -1) Object.assign(sales.value[idx], data)
  }

  function remove(id: string) {
    sales.value = sales.value.filter(s => s.id !== id)
  }

  function get(id: string): Sale | undefined {
    return sales.value.find(s => s.id === id)
  }

  const totalSales = computed(() =>
    sales.value.reduce((sum, s) => sum + s.grandTotal, 0)
  )

  return { sales, add, update, remove, get, totalSales }
})
