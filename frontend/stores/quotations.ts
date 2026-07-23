export interface QuotationItem {
  id: string
  productId: string
  name: string
  quantity: number
  unitPrice: number
  totalPrice: number
}

export interface Quotation {
  id: string
  date: string
  partyId: string
  partyName: string
  items: QuotationItem[]
  totalAmount: number
  status: string
  notes: string
}

export const useQuotationsStore = defineStore('quotations', () => {
  const quotations = ref<Quotation[]>([])

  function add(q: Quotation) {
    quotations.value.push(q)
  }

  function update(id: string, data: Partial<Quotation>) {
    const idx = quotations.value.findIndex(q => q.id === id)
    if (idx !== -1) Object.assign(quotations.value[idx], data)
  }

  function remove(id: string) {
    quotations.value = quotations.value.filter(q => q.id !== id)
  }

  return { quotations, add, update, remove }
})
