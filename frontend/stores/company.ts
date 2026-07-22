import { api } from '~/lib/api/client'
import type { CompanyResponse, CompanyUpdate } from '~/lib/api/client'

export const useCompanyStore = defineStore('company', () => {
  const profile = ref<CompanyResponse | null>(null)
  const loading = ref(false)

  async function fetchProfile() {
    loading.value = true
    try { profile.value = await api().getCompany() }
    finally { loading.value = false }
  }

  async function save(data: CompanyUpdate) {
    profile.value = await api().updateCompany(data)
  }

  return { profile, loading, fetchProfile, save }
})
