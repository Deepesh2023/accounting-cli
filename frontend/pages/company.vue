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
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Company Profile</h1>
      <button class="btn btn-primary" @click="save" :disabled="store.loading">Save</button>
    </div>

    <div v-if="store.loading" class="text-center py-4 text-muted">Loading...</div>

    <template v-else>
      <div class="card mb-4">
        <div class="card-header"><h5 class="m-0">Business Information</h5></div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-12 col-sm-6">
              <label class="form-label">Business Name</label>
              <input v-model="form.name" class="form-control" />
            </div>
            <div class="col-12 col-sm-3">
              <label class="form-label">Business Type</label>
              <select v-model="form.business_type" class="form-select">
                <option value="">Select</option>
                <option value="Retail">Retail</option>
                <option value="Wholesale">Wholesale</option>
                <option value="Manufacturing">Manufacturing</option>
                <option value="Service">Service</option>
              </select>
            </div>
            <div class="col-12 col-sm-3">
              <label class="form-label">Category</label>
              <input v-model="form.category" class="form-control" />
            </div>
            <div class="col-12 col-sm-4">
              <label class="form-label">Start Date</label>
              <input v-model="form.beginning_date" type="date" class="form-control" />
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header"><h5 class="m-0">Contact</h5></div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-12 col-sm-4">
              <label class="form-label">Phone</label>
              <input v-model="form.phone" class="form-control" />
            </div>
            <div class="col-12 col-sm-4">
              <label class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-control" />
            </div>
            <div class="col-12 col-sm-4">
              <label class="form-label">State</label>
              <input v-model="form.state" class="form-control" />
            </div>
            <div class="col-12 col-sm-4">
              <label class="form-label">Pincode</label>
              <input v-model="form.pincode" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">Address</label>
              <textarea v-model="form.address" class="form-control" rows="2"></textarea>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header"><h5 class="m-0">Tax & Settings</h5></div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-12 col-sm-4">
              <label class="form-label">GSTIN</label>
              <input v-model="form.gstin" class="form-control" placeholder="22AAAAA0000A1Z5" />
            </div>
            <div class="col-12 col-sm-4 d-flex align-items-end">
              <div class="form-check">
                <input v-model="form.enable_party_netting" type="checkbox" class="form-check-input" id="netting" />
                <label class="form-check-label" for="netting">Enable Party Netting</label>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header"><h5 class="m-0">Uploads</h5></div>
        <div class="card-body">
          <div class="row g-4">
            <div class="col-12 col-sm-6">
              <label class="form-label">Logo</label>
              <input type="file" accept="image/*" class="form-control" @change="onLogoUpload" />
              <div v-if="form.logo_data" class="mt-2">
                <img :src="form.logo_data" class="img-thumbnail" style="max-height:100px" />
              </div>
            </div>
            <div class="col-12 col-sm-6">
              <label class="form-label">QR Code</label>
              <input type="file" accept="image/*" class="form-control" @change="onQrUpload" />
              <div v-if="form.qr_data" class="mt-2">
                <img :src="form.qr_data" class="img-thumbnail" style="max-height:100px" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="text-end mb-4">
        <button class="btn btn-primary btn-lg px-5" @click="save">Save Profile</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.card { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-radius: 8px; }
.card-header { background: #fff; border-bottom: 1px solid #eee; font-weight: 600; }
.card-header h5 { font-weight: 700; }
.form-label { font-weight: 500; font-size: 0.9rem; color: #444; }
</style>
