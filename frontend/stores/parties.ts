import { defineStore } from 'pinia'
import { api } from '~/lib/api/client'

export const usePartiesStore = defineStore('parties', () => {
  const list = ref<import('~/lib/api/client').PartyResponse[]>([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try { list.value = await api().listParties() }
    finally { loading.value = false }
  }

  async function create(data: import('~/lib/api/client').PartyCreate) {
    const p = await api().createParty(data)
    list.value.push(p)
    return p
  }

  async function update(id: string, data: import('~/lib/api/client').PartyUpdate) {
    const p = await api().updateParty(id, data)
    const i = list.value.findIndex(x => x.party_id === id)
    if (i >= 0) list.value[i] = p
    return p
  }

  async function remove(id: string) {
    await api().deleteParty(id)
    list.value = list.value.filter(x => x.party_id !== id)
  }

  return { list, loading, fetchAll, create, update, remove }
})
