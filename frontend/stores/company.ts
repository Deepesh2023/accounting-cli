import { defineStore } from 'pinia'
import { api } from '~/lib/api/client'

export const useCompanyStore = defineStore('company', () => {
  const profile = ref<import('~/lib/api/client').CompanyResponse | null>(null)
  const loading = ref(false)

  async function fetchProfile() {
    loading.value = true
    try { profile.value = await api().getCompany() }
    catch { profile.value = null }
    finally { loading.value = false }
  }

  async function save(data: import('~/lib/api/client').CompanyUpdate) {
    profile.value = await api().updateCompany(data)
    return profile.value
  }

  return { profile, loading, fetchProfile, save }
})
