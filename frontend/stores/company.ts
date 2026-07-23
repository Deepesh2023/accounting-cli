export const useCompanyStore = defineStore('company', () => {
  const profile = ref({
    name: '',
    businessType: '',
    category: '',
    beginningDate: '',
    phone: '',
    email: '',
    address: '',
    state: '',
    gstin: '',
    logoUrl: '',
    qrUrl: '',
  })

  function update(data: Partial<typeof profile.value>) {
    Object.assign(profile.value, data)
  }

  return { profile, update }
})
