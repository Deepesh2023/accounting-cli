export type PartyType = 'DEBTOR' | 'CREDITOR'

export interface Party {
  id: string
  name: string
  phone: string
  state: string
  address: string
  type: PartyType
  balance: number
  gstin: string
}

export const usePartiesStore = defineStore('parties', () => {
  const parties = ref<Party[]>([])

  function add(p: Party) {
    parties.value.push(p)
  }

  function update(id: string, data: Partial<Party>) {
    const idx = parties.value.findIndex(p => p.id === id)
    if (idx !== -1) Object.assign(parties.value[idx], data)
  }

  function remove(id: string) {
    parties.value = parties.value.filter(p => p.id !== id)
  }

  function get(id: string): Party | undefined {
    return parties.value.find(p => p.id === id)
  }

  return { parties, add, update, remove, get }
})
