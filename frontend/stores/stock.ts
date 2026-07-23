export interface StockItem {
  id: string
  name: string
  itemCode: string
  quantity: number
  unit: string
  price: number
  gstRate: number
  hsnCode: string
}

export const useStockStore = defineStore('stock', () => {
  const items = ref<StockItem[]>([])

  function add(item: StockItem) {
    items.value.push(item)
  }

  function update(id: string, data: Partial<StockItem>) {
    const idx = items.value.findIndex(i => i.id === id)
    if (idx !== -1) Object.assign(items.value[idx], data)
  }

  function remove(id: string) {
    items.value = items.value.filter(i => i.id !== id)
  }

  function get(id: string): StockItem | undefined {
    return items.value.find(i => i.id === id)
  }

  const closingStock = computed(() =>
    items.value.reduce((sum, i) => sum + i.quantity * i.price, 0)
  )

  return { items, add, update, remove, get, closingStock }
})
