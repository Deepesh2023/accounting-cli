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
      <UCard class="mb-4">
        <template #header>
          <h5 class="font-bold">Business Information</h5>
        </template>
        <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
          <div class="sm:col-span-6">
            <label class="block text-sm font-medium text-gray-700 mb-1">Business Name</label>
            <UInput v-model="form.name" />
          </div>
          <div class="sm:col-span-3">
            <label class="block text-sm font-medium text-gray-700 mb-1">Business Type</label>
            <USelect v-model="form.business_type" :items="['Retail', 'Wholesale', 'Manufacturing', 'Service']" placeholder="Select" />
          </div>
          <div class="sm:col-span-3">
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <UInput v-model="form.category" />
          </div>
          <div class="sm:col-span-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
            <UInput v-model="form.beginning_date" type="date" />
          </div>
        </div>
      </UCard>

      <UCard class="mb-4">
        <template #header>
          <h5 class="font-bold">Contact</h5>
        </template>
        <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
          <div class="sm:col-span-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Phone</label>
            <UInput v-model="form.phone" />
          </div>
          <div class="sm:col-span-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <UInput v-model="form.email" type="email" />
          </div>
          <div class="sm:col-span-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">State</label>
            <USelect v-model="form.state" :items="stateOptions" placeholder="Select state" />
          </div>
          <div class="sm:col-span-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Pincode</label>
            <UInput v-model="form.pincode" />
          </div>
          <div class="sm:col-span-12">
            <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
            <textarea v-model="form.address" class="block w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" rows="2"></textarea>
          </div>
        </div>
      </UCard>

      <UCard class="mb-4">
        <template #header>
          <h5 class="font-bold">Tax & Settings</h5>
        </template>
        <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
          <div class="sm:col-span-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">GSTIN</label>
            <UInput v-model="form.gstin" placeholder="22AAAAA0000A1Z5" />
          </div>
          <div class="sm:col-span-4 flex items-end">
            <UCheckbox v-model="form.enable_party_netting" label="Enable Party Netting" />
          </div>
        </div>
      </UCard>

      <UCard class="mb-4">
        <template #header>
          <h5 class="font-bold">Uploads</h5>
        </template>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Logo</label>
            <input type="file" accept="image/*" class="block w-full border border-gray-300 rounded-lg px-3 py-2 text-sm file:mr-3 file:py-1 file:px-3 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200" @change="onLogoUpload" />
            <div v-if="form.logo_data" class="mt-2">
              <img :src="form.logo_data" class="border border-gray-300 rounded p-1 max-h-[100px]" />
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">QR Code</label>
            <input type="file" accept="image/*" class="block w-full border border-gray-300 rounded-lg px-3 py-2 text-sm file:mr-3 file:py-1 file:px-3 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200" @change="onQrUpload" />
            <div v-if="form.qr_data" class="mt-2">
              <img :src="form.qr_data" class="border border-gray-300 rounded p-1 max-h-[100px]" />
            </div>
          </div>
        </div>
      </UCard>

      <div class="text-right mb-4">
        <UButton color="primary" size="lg" class="px-8" @click="save">Save Profile</UButton>
      </div>
    </template>
  </div>
</template>

<style scoped>
</style>
