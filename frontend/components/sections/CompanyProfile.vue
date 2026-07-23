<script setup lang="ts">
const company = useCompanyStore()

const states = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
  'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
  'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
  'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
  'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
  'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
]

function handleLogoUpload(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => company.update({ logoUrl: reader.result as string })
    reader.readAsDataURL(file)
  }
}

function handleQrUpload(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => company.update({ qrUrl: reader.result as string })
    reader.readAsDataURL(file)
  }
}

function exportData() {
  const data = {
    company: company.profile,
    parties: usePartiesStore().parties,
    stock: useStockStore().items,
    sales: useSalesStore().sales,
    purchases: usePurchasesStore().purchases,
    expenses: useExpensesStore().expenses,
    quotations: useQuotationsStore().quotations,
    ledger: useLedgerStore().entries,
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `printos-backup-${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
}

function importData(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result as string)
      if (data.company) useCompanyStore().update(data.company)
      if (data.parties) usePartiesStore().parties = data.parties
      if (data.stock) useStockStore().items = data.stock
      if (data.sales) useSalesStore().sales = data.sales
      if (data.purchases) usePurchasesStore().purchases = data.purchases
      if (data.expenses) useExpensesStore().expenses = data.expenses
      if (data.quotations) useQuotationsStore().quotations = data.quotations
      if (data.ledger) useLedgerStore().entries = data.ledger
    } catch {
      alert('Invalid backup file')
    }
  }
  reader.readAsText(file)
}
</script>

<template>
  <div class="max-w-5xl mx-auto space-y-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">Company Profile</h2>
      <UButton label="Save Changes" color="primary" />
    </div>

    <UCard>
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Logo & QR -->
        <div class="space-y-8">
          <div>
            <p class="text-xs font-semibold uppercase text-gray-500 mb-3">Company Logo</p>
            <div
              class="w-40 h-40 rounded-full bg-gray-100 dark:bg-gray-700 border-2 border-dashed border-gray-300 dark:border-gray-600 flex items-center justify-center cursor-pointer hover:border-primary transition-colors overflow-hidden"
              @click="document.getElementById('logo-input')?.click()"
            >
              <img v-if="company.profile.logoUrl" :src="company.profile.logoUrl" class="w-full h-full object-cover" alt="Logo" />
              <div v-else class="text-center text-gray-400">
                <UIcon name="i-heroicons-photo" class="w-8 h-8 mx-auto" />
                <span class="text-xs font-semibold">ADD LOGO</span>
              </div>
            </div>
            <input id="logo-input" type="file" accept="image/*" class="hidden" @change="handleLogoUpload" />
            <p class="text-xs text-gray-400 mt-2">Click to upload business logo</p>
          </div>

          <div>
            <p class="text-xs font-semibold uppercase text-gray-500 mb-3">Payment QR Code</p>
            <div
              class="w-40 h-40 bg-gray-100 dark:bg-gray-700 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl flex items-center justify-center cursor-pointer hover:border-primary transition-colors overflow-hidden"
              @click="document.getElementById('qr-input')?.click()"
            >
              <img v-if="company.profile.qrUrl" :src="company.profile.qrUrl" class="w-full h-full object-cover" alt="QR" />
              <div v-else class="text-center text-gray-400">
                <UIcon name="i-heroicons-qr-code" class="w-8 h-8 mx-auto" />
                <span class="text-xs font-semibold">ADD QR</span>
              </div>
            </div>
            <input id="qr-input" type="file" accept="image/*" class="hidden" @change="handleQrUpload" />
            <p class="text-xs text-gray-400 mt-2">Upload UPI or Bank QR</p>
          </div>
        </div>

        <!-- Form -->
        <div class="lg:col-span-3 space-y-6">
          <div class="bg-gray-50 dark:bg-gray-900 rounded-xl p-5 space-y-4">
            <h6 class="font-semibold flex items-center gap-2 text-sm">
              <UIcon name="i-heroicons-information-circle" class="w-4 h-4" />
              Basic Information
            </h6>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <UFormField label="Business Name" required>
                <UInput v-model="company.profile.name" placeholder="e.g. Nectar Technologies" class="w-full" />
              </UFormField>
              <UFormField label="Business Type">
                <USelect v-model="company.profile.businessType" :items="['', 'Retail', 'Wholesale', 'Manufacturing', 'Services']" class="w-full" />
              </UFormField>
              <UFormField label="Business Category">
                <UInput v-model="company.profile.category" placeholder="e.g. IT Services" class="w-full" />
              </UFormField>
              <UFormField label="Beginning Date">
                <UInput v-model="company.profile.beginningDate" type="date" class="w-full" />
              </UFormField>
            </div>
          </div>

          <div class="bg-gray-50 dark:bg-gray-900 rounded-xl p-5 space-y-4">
            <h6 class="font-semibold flex items-center gap-2 text-sm">
              <UIcon name="i-heroicons-map-pin" class="w-4 h-4" />
              Contact & Address
            </h6>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <UFormField label="Phone Number">
                <UInput v-model="company.profile.phone" placeholder="Phone number" class="w-full" />
              </UFormField>
              <UFormField label="Email">
                <UInput v-model="company.profile.email" type="email" placeholder="Email" class="w-full" />
              </UFormField>
              <div class="md:col-span-2">
                <UFormField label="Address">
                  <UTextarea v-model="company.profile.address" rows="2" placeholder="Full address" class="w-full" />
                </UFormField>
              </div>
              <UFormField label="State">
                <USelect v-model="company.profile.state" :items="states" class="w-full" />
              </UFormField>
            </div>
          </div>

          <div class="bg-gray-50 dark:bg-gray-900 rounded-xl p-5 space-y-4">
            <h6 class="font-semibold flex items-center gap-2 text-sm">
              <UIcon name="i-heroicons-cog-6-tooth" class="w-4 h-4" />
              Statutory & Preferences
            </h6>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <UFormField label="GSTIN">
                <UInput v-model="company.profile.gstin" placeholder="Enter GSTIN" class="w-full" />
              </UFormField>
            </div>
          </div>

          <div class="bg-gray-50 dark:bg-gray-900 rounded-xl p-5 space-y-4">
            <h6 class="font-semibold flex items-center gap-2 text-sm">
              <UIcon name="i-heroicons-cloud-arrow-up" class="w-4 h-4" />
              Data Backup & Restore
            </h6>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-white dark:bg-gray-800 rounded-lg p-5 text-center border border-green-200 dark:border-green-800">
                <UIcon name="i-heroicons-cloud-arrow-down" class="w-8 h-8 text-green-600 mx-auto mb-2" />
                <h6 class="font-semibold">Export Backup</h6>
                <p class="text-xs text-gray-500 mb-3">Download all data as JSON</p>
                <UButton label="Export Data" color="green" variant="outline" class="w-full" @click="exportData" />
              </div>
              <div class="bg-white dark:bg-gray-800 rounded-lg p-5 text-center border border-primary/25">
                <UIcon name="i-heroicons-cloud-arrow-up" class="w-8 h-8 text-primary mx-auto mb-2" />
                <h6 class="font-semibold">Import Backup</h6>
                <p class="text-xs text-gray-500 mb-3">Restore from JSON file</p>
                <UButton label="Import Data" color="primary" variant="outline" class="w-full" @click="document.getElementById('import-input')?.click()" />
                <input id="import-input" type="file" accept=".json" class="hidden" @change="importData" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </UCard>
  </div>
</template>
