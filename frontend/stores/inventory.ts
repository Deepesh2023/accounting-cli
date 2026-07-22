import { defineStore } from 'pinia'
import { api } from '~/lib/api/client'

export const useInventoryStore = defineStore('inventory', () => {
  const items = ref<import('~/lib/api/client').ProductResponse[]>([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try { items.value = await api().listProducts() }
    finally { loading.value = false }
  }

  async function create(data: import('~/lib/api/client').ProductCreate) {
    const p = await api().createProduct(data)
    items.value.push(p)
    return p
  }

  async function update(id: string, data: import('~/lib/api/client').ProductUpdate) {
    const p = await api().updateProduct(id, data)
    const i = items.value.findIndex(x => x.product_id === id)
    if (i >= 0) items.value[i] = p
    return p
  }

  async function remove(id: string) {
    await api().deleteProduct(id)
    items.value = items.value.filter(x => x.product_id !== id)
  }

  return { items, loading, fetchAll, create, update, remove }
})
