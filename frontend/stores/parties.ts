import { api } from '~/lib/api/client'
import type { PartyResponse, PartyCreate, PartyUpdate } from '~/lib/api/client'

export const usePartiesStore = defineStore('parties', () => {
  const list = ref<PartyResponse[]>([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try { list.value = await api().listParties() }
    finally { loading.value = false }
  }

  async function create(data: PartyCreate) {
    const p = await api().createParty(data)
    list.value.push(p)
  }

  async function update(id: string, data: PartyUpdate) {
    const p = await api().updateParty(id, data)
    const idx = list.value.findIndex(x => x.party_id === id)
    if (idx >= 0) list.value[idx] = p
  }

  async function remove(id: string) {
    await api().deleteParty(id)
    list.value = list.value.filter(x => x.party_id !== id)
  }

  return { list, loading, fetchAll, create, update, remove }
})
