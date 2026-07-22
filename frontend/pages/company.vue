<script setup lang="ts">
import { useCompanyStore } from '~/stores/company'

definePageMeta({ title: 'Company' })

const store = useCompanyStore()

const form = ref({
  name: '', business_type: '', category: '', beginning_date: '',
  phone: '', email: '', address: '', state: '', pincode: '',
  gstin: '', enable_party_netting: false,
  logo_data: '' as string,
  qr_data: '' as string,
})

const stateOptions = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
  'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
  'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
  'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
  'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
  'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry',
]

onMounted(() => {
  store.fetchProfile().then(() => {
    if (store.profile) {
      form.value.name = store.profile.name || ''
      form.value.business_type = store.profile.business_type || ''
      form.value.category = store.profile.category || ''
      form.value.beginning_date = store.profile.beginning_date?.slice(0, 10) || ''
      form.value.phone = store.profile.phone || ''
      form.value.email = store.profile.email || ''
      form.value.address = store.profile.address || ''
    }
  })
})

async function save() {
  try {
    await store.save({
      name: form.value.name,
      business_type: form.value.business_type || null,
      category: form.value.category || null,
      beginning_date: form.value.beginning_date || null,
      phone: form.value.phone || null,
      email: form.value.email || null,
      address: form.value.address || null,
      logo_path: form.value.logo_data || null,
      qr_path: form.value.qr_data || null,
    })
    alert('Company profile saved.')
  } catch (e: any) { alert(e.message) }
}

function onLogoUpload(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => { form.value.logo_data = reader.result as string }
  reader.readAsDataURL(file)
}

function onQrUpload(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => { form.value.qr_data = reader.result as string }
  reader.readAsDataURL(file)
}
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Company Profile</h1>
      <UButton color="primary" @click="save" :disabled="store.loading">Save</UButton>
    </div>

    <div v-if="store.loading" class="text-center py-4 text-gray-500">Loading...</div>

    <template v-else>
      <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div class="md:col-span-3 space-y-6">
          <UCard>
            <div class="text-center">
              <label class="block text-xs uppercase tracking-wider font-bold text-gray-500 mb-3">Company Logo</label>
              <div class="mx-auto w-40 h-40 rounded-full border-2 border-dashed border-gray-300 bg-gray-50 flex items-center justify-center cursor-pointer hover:border-primary hover:bg-blue-50 transition-all overflow-hidden" @click="document.getElementById('logo-input')?.click()">
                <div v-if="!form.logo_data" class="text-center">
                  <UIcon name="i-heroicons-photo" class="text-3xl text-gray-400 mx-auto" />
                  <span class="text-xs text-gray-400 font-bold block mt-1">ADD LOGO</span>
                </div>
                <img v-else :src="form.logo_data" class="w-full h-full object-cover" />
              </div>
              <input id="logo-input" type="file" accept="image/*" class="hidden" @change="onLogoUpload" />
              <p class="text-xs text-gray-400 mt-2">Click to upload your business logo</p>
            </div>
          </UCard>
          <UCard>
            <div class="text-center">
              <label class="block text-xs uppercase tracking-wider font-bold text-gray-500 mb-3">Payment QR Code</label>
              <div class="mx-auto w-40 h-40 border-2 border-dashed border-gray-300 bg-gray-50 flex items-center justify-center cursor-pointer hover:border-primary hover:bg-blue-50 transition-all overflow-hidden rounded-xl" @click="document.getElementById('qr-input')?.click()">
                <div v-if="!form.qr_data" class="text-center">
                  <UIcon name="i-heroicons-qr-code" class="text-3xl text-gray-400 mx-auto" />
                  <span class="text-xs text-gray-400 font-bold block mt-1">ADD QR</span>
                </div>
                <img v-else :src="form.qr_data" class="w-full h-full object-cover" />
              </div>
              <input id="qr-input" type="file" accept="image/*" class="hidden" @change="onQrUpload" />
              <p class="text-xs text-gray-400 mt-2">Upload your UPI or Bank QR code</p>
            </div>
          </UCard>
        </div>
        <div class="md:col-span-9 space-y-4">
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-heroicons-information-circle" class="text-primary" />
                <span class="font-bold">Basic Information</span>
              </div>
            </template>
            <div class="grid grid-cols-1 sm:grid-cols-12 gap-4">
              <div class="sm:col-span-8">
                <UInput v-model="form.name" placeholder="Business Name" label="Business Name" />
              </div>
              <div class="sm:col-span-4">
                <USelect v-model="form.business_type" :items="['Retail', 'Wholesale', 'Manufacturing', 'Service']" placeholder="Select" label="Business Type" />
              </div>
              <div class="sm:col-span-6">
                <UInput v-model="form.category" placeholder="e.g. IT Services" label="Business Category" />
              </div>
              <div class="sm:col-span-6">
                <UInput v-model="form.beginning_date" type="date" label="Account Books Beginning Date" />
              </div>
            </div>
          </UCard>
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-heroicons-map-pin" class="text-primary" />
                <span class="font-bold">Contact & Address</span>
              </div>
            </template>
            <div class="grid grid-cols-1 sm:grid-cols-12 gap-4">
              <div class="sm:col-span-6">
                <UInput v-model="form.phone" placeholder="+91" label="Phone Number" />
              </div>
              <div class="sm:col-span-6">
                <UInput v-model="form.email" type="email" placeholder="email@example.com" label="Email ID" />
              </div>
              <div class="sm:col-span-12">
                <UTextarea v-model="form.address" placeholder="Full Address..." label="Business Address" :rows="2" />
              </div>
              <div class="sm:col-span-6">
                <USelect v-model="form.state" :items="stateOptions" placeholder="Select state" label="State" />
              </div>
              <div class="sm:col-span-6">
                <UInput v-model="form.pincode" label="Pincode" />
              </div>
            </div>
          </UCard>
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-heroicons-cog-6-tooth" class="text-primary" />
                <span class="font-bold">Statutory & Preferences</span>
              </div>
            </template>
            <div class="grid grid-cols-1 sm:grid-cols-12 gap-4">
              <div class="sm:col-span-6">
                <UInput v-model="form.gstin" placeholder="22AAAAA0000A1Z5" label="GSTIN" />
              </div>
              <div class="sm:col-span-6 flex items-end pb-1">
                <UCheckbox v-model="form.enable_party_netting" label="Enable Party Netting" />
              </div>
            </div>
          </UCard>
          <UCard class="mb-4">
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-heroicons-cloud-arrow-up" class="text-primary" />
                <span class="font-bold">Data Backup & Restore</span>
              </div>
            </template>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="p-4 bg-gray-50 rounded-lg text-center border border-green-200 border-opacity-50">
                <UIcon name="i-heroicons-cloud-arrow-down" class="text-2xl text-green-600 mb-1" />
                <h6 class="font-bold text-sm">Export Backup</h6>
                <p class="text-xs text-gray-500 mb-3">Download all your accounting data securely as a JSON file.</p>
                <UButton color="success" variant="outline" class="w-full" size="sm">Export Data</UButton>
              </div>
              <div class="p-4 bg-gray-50 rounded-lg text-center border border-blue-200 border-opacity-50">
                <UIcon name="i-heroicons-cloud-arrow-up" class="text-2xl text-blue-600 mb-1" />
                <h6 class="font-bold text-sm">Import Backup</h6>
                <p class="text-xs text-gray-500 mb-3">Restore your data from a previously downloaded JSON file.</p>
                <UButton color="primary" variant="outline" class="w-full" size="sm">Import Data</UButton>
              </div>
            </div>
          </UCard>
          <div class="text-right">
            <UButton color="primary" size="lg" class="px-8" @click="save" :disabled="store.loading">Save Changes</UButton>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
