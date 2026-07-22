import type { ProductResponse, ProductCreate, ProductUpdate } from '~/lib/api/client'

export const useInventoryStore = defineStore('inventory', () => {
  const items = ref<ProductResponse[]>([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try { items.value = await api().listProducts() }
    finally { loading.value = false }
  }

  async function create(data: ProductCreate) {
    const p = await api().createProduct(data)
    items.value.push(p)
  }

  async function update(id: string, data: ProductUpdate) {
    const p = await api().updateProduct(id, data)
    const idx = items.value.findIndex(x => x.product_id === id)
    if (idx >= 0) items.value[idx] = p
  }

  async function remove(id: string) {
    await api().deleteProduct(id)
    items.value = items.value.filter(x => x.product_id !== id)
  }

  return { items, loading, fetchAll, create, update, remove }
})
