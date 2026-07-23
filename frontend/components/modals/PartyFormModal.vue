<script setup lang="ts">
const store = usePartiesStore()

const open = ref(false)
const editingId = ref<string | null>(null)
const form = reactive({
  name: '',
  phone: '',
  state: '',
  address: '',
  type: 'DEBTOR' as 'DEBTOR' | 'CREDITOR',
  balance: 0,
})

const states = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
  'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
  'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
  'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha',
  'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
  'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
]

function openCreate() {
  editingId.value = null
  form.name = ''
  form.phone = ''
  form.state = ''
  form.address = ''
  form.type = 'DEBTOR'
  form.balance = 0
  open.value = true
}

function openEdit(party: { id: string; name: string; phone: string; state: string; address: string; type: string; balance: number }) {
  editingId.value = party.id
  form.name = party.name
  form.phone = party.phone
  form.state = party.state
  form.address = party.address
  form.type = party.type as 'DEBTOR' | 'CREDITOR'
  form.balance = party.balance
  open.value = true
}

function submit() {
  if (!form.name.trim()) return
  const data = {
    id: editingId.value || crypto.randomUUID(),
    name: form.name,
    phone: form.phone,
    state: form.state,
    address: form.address,
    type: form.type,
    balance: form.balance,
    gstin: '',
  }
  if (editingId.value) {
    store.update(editingId.value, data)
  } else {
    store.add(data)
  }
  open.value = false
}

defineExpose({ openCreate, openEdit })
</script>

<template>
  <UModal v-model:open="open" :title="editingId ? 'Edit Party' : 'Add Party'">
    <template #body>
      <form @submit.prevent="submit" class="space-y-4">
        <UFormField label="Name" required>
          <UInput v-model="form.name" placeholder="Party name" class="w-full" />
        </UFormField>
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="Phone">
            <UInput v-model="form.phone" placeholder="Phone number" class="w-full" />
          </UFormField>
          <UFormField label="State">
            <USelect v-model="form.state" :items="states" placeholder="Select state" class="w-full" />
          </UFormField>
        </div>
        <UFormField label="Address">
          <UInput v-model="form.address" placeholder="Address" class="w-full" />
        </UFormField>
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="Opening Balance">
            <UInput v-model="form.balance" type="number" step="0.01" class="w-full" />
          </UFormField>
          <UFormField label="Type">
            <USelect v-model="form.type" :items="['DEBTOR', 'CREDITOR']" class="w-full" />
          </UFormField>
        </div>
      </form>
    </template>
    <template #footer>
      <UButton label="Cancel" variant="ghost" color="gray" @click="open = false" />
      <UButton :label="editingId ? 'Update' : 'Save'" color="primary" @click="submit" />
    </template>
  </UModal>
</template>
