<script setup lang="ts">
import { api } from '~/lib/api/client'
import { usePartiesStore } from '~/stores/parties'
import type { PartyResponse, PartyCreate, PartyUpdate } from '~/lib/api/client'

definePageMeta({ title: 'Parties' })

const store = usePartiesStore()
const showModal = ref(false)
const showLedger = ref(false)
const editing = ref<string | null>(null)
const ledgerParty = ref<PartyResponse | null>(null)
const ledgerTxns = ref<any[]>([])

const form = ref<PartyCreate>({
  name: '', phone: '', state: '', address: '', balance: 0, party_type: 'DEBTOR',
})

const indianStates = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat',
  'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
  'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
  'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
  'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh',
  'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Jammu and Kashmir',
  'Ladakh', 'Lakshadweep', 'Puducherry',
]

onMounted(() => store.fetchAll())

function openAdd() {
  editing.value = null
  form.value = { name: '', phone: '', state: '', address: '', balance: 0, party_type: 'DEBTOR' }
  showModal.value = true
}

function openEdit(p: PartyResponse) {
  editing.value = p.party_id
  form.value = {
    name: p.name, phone: p.phone || '', state: p.state,
    address: p.address || '', balance: Number(p.balance), party_type: p.party_type,
  }
  showModal.value = true
}

async function save() {
  if (editing.value) {
    await store.update(editing.value, form.value as PartyUpdate)
  } else {
    await store.create(form.value)
  }
  showModal.value = false
}

async function confirmDelete(id: string) {
  if (confirm('Delete this party?')) await store.remove(id)
}

async function openLedger(p: PartyResponse) {
  ledgerParty.value = p
  ledgerTxns.value = await api().getLedgerTransactions(p.name)
  showLedger.value = true
}

const currency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="m-0">Parties</h1>
      <UButton color="primary" @click="openAdd">+ Add Party</UButton>
    </div>

    <UCard>
      <div v-if="store.loading" class="text-center py-4 text-gray-500">Loading...</div>
      <div v-else-if="!store.list.length" class="text-center py-4 text-gray-500">No parties found.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">#</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Name</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Phone</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">State</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Type</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Balance</th>
              <th class="p-3 text-left font-semibold text-sm uppercase tracking-wide">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, i) in store.list" :key="p.party_id" class="hover:bg-gray-50 border-b border-gray-200">
              <td class="p-3 align-middle">{{ i + 1 }}</td>
              <td class="p-3 align-middle">{{ p.name }}</td>
              <td class="p-3 align-middle">{{ p.phone || '-' }}</td>
              <td class="p-3 align-middle">{{ p.state }}</td>
              <td class="p-3 align-middle">
                <UBadge :color="p.party_type === 'DEBTOR' ? 'primary' : 'warning'" variant="soft">
                  {{ p.party_type === 'DEBTOR' ? 'Debtor' : 'Creditor' }}
                </UBadge>
              </td>
              <td class="p-3 align-middle" :class="Number(p.balance) >= 0 ? 'text-green-600' : 'text-red-600'">
                {{ currency(p.balance) }}
              </td>
              <td class="p-3 align-middle whitespace-nowrap space-x-1">
                <UButton size="sm" variant="ghost" color="primary" @click="openLedger(p)">Ledger</UButton>
                <UButton size="sm" variant="ghost" color="primary" @click="openEdit(p)">Edit</UButton>
                <UButton size="sm" variant="ghost" color="error" @click="confirmDelete(p.party_id)">Delete</UButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UCard>

    <UModal v-model:open="showModal">
      <template #title>{{ editing ? 'Edit' : 'Add' }} Party</template>
      <div class="space-y-4">
        <UInput v-model="form.name" placeholder="Party Name" />
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <UInput v-model="form.phone" placeholder="Phone" />
          <USelect v-model="form.state" :items="indianStates" placeholder="Select State" />
        </div>
        <UTextarea v-model="form.address" placeholder="Address" :rows="2" />
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <UInput v-model.number="form.balance" type="number" step="0.01" placeholder="Opening Balance" />
          <USelect v-model="form.party_type" :items="[{label: 'Receive (Debtor)', value: 'DEBTOR'}, {label: 'Pay (Creditor)', value: 'CREDITOR'}]" />
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton color="neutral" variant="ghost" @click="showModal = false">Cancel</UButton>
          <UButton color="primary" @click="save">Save</UButton>
        </div>
      </template>
    </UModal>

    <UModal v-model:open="showLedger">
      <template #title>Ledger: {{ ledgerParty?.name }}</template>
      <div v-if="!ledgerTxns.length" class="text-gray-500 text-center py-3">No transactions found.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="p-2 text-left font-semibold text-sm">Date</th>
              <th class="p-2 text-left font-semibold text-sm">Particulars</th>
              <th class="p-2 text-right font-semibold text-sm">Debit</th>
              <th class="p-2 text-right font-semibold text-sm">Credit</th>
              <th class="p-2 text-right font-semibold text-sm">Balance</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in ledgerTxns" :key="t.transaction_id || t.id" class="border-b border-gray-200">
              <td class="p-2">{{ t.date?.slice(0, 10) }}</td>
              <td class="p-2">{{ t.particulars || t.description || '-' }}</td>
              <td class="p-2 text-right text-red-600">{{ t.debit ? currency(t.debit) : '-' }}</td>
              <td class="p-2 text-right text-green-600">{{ t.credit ? currency(t.credit) : '-' }}</td>
              <td class="p-2 text-right">{{ currency(t.balance || t.running_balance || 0) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <template #footer>
        <UButton color="neutral" variant="ghost" @click="showLedger = false">Close</UButton>
      </template>
    </UModal>
  </div>
</template>
