<script setup lang="ts">
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
    name: p.name,
    phone: p.phone || '',
    state: p.state,
    address: p.address || '',
    balance: Number(p.balance),
    party_type: p.party_type,
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
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Parties</h1>
      <button class="btn btn-primary" @click="openAdd">+ Add Party</button>
    </div>
    <div class="card">
      <div class="card-body p-0">
        <div v-if="store.loading" class="text-center py-4 text-muted">Loading...</div>
        <div v-else-if="!store.list.length" class="text-center py-4 text-muted">No parties found.</div>
        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>#</th><th>Name</th><th>Phone</th><th>State</th><th>Type</th><th>Balance</th><th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(p, i) in store.list" :key="p.party_id">
                <td>{{ i + 1 }}</td>
                <td>{{ p.name }}</td>
                <td>{{ p.phone || '-' }}</td>
                <td>{{ p.state }}</td>
                <td>
                  <span :class="p.party_type === 'DEBTOR' ? 'badge bg-info' : 'badge bg-warning'">
                    {{ p.party_type === 'DEBTOR' ? 'Debtor' : 'Creditor' }}
                  </span>
                </td>
                <td :class="Number(p.balance) >= 0 ? 'text-success' : 'text-danger'">
                  {{ currency(p.balance) }}
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-info me-1" @click="openLedger(p)">Ledger</button>
                  <button class="btn btn-sm btn-outline-primary me-1" @click="openEdit(p)">Edit</button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(p.party_id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="modal-backdrop fade show" @click="showModal = false"></div>
    <div v-if="showModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editing ? 'Edit' : 'Add' }} Party</h5>
            <button type="button" class="btn-close" @click="showModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Party Name</label>
              <input v-model="form.name" class="form-control" />
            </div>
            <div class="row g-3">
              <div class="col-6">
                <label class="form-label">Phone</label>
                <input v-model="form.phone" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label">State</label>
                <select v-model="form.state" class="form-select">
                  <option value="" disabled>Select State</option>
                  <option v-for="s in indianStates" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>
            </div>
            <div class="mb-3 mt-3">
              <label class="form-label">Address</label>
              <textarea v-model="form.address" class="form-control" rows="2"></textarea>
            </div>
            <div class="row g-3">
              <div class="col-6">
                <label class="form-label">Opening Balance</label>
                <input v-model.number="form.balance" type="number" step="0.01" class="form-control" />
              </div>
              <div class="col-6">
                <label class="form-label">Type</label>
                <select v-model="form.party_type" class="form-select">
                  <option value="DEBTOR">Receive (Debtor)</option>
                  <option value="CREDITOR">Pay (Creditor)</option>
                </select>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showModal = false">Cancel</button>
            <button class="btn btn-primary" @click="save">Save</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showLedger" class="modal-backdrop fade show" @click="showLedger = false"></div>
    <div v-if="showLedger" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Ledger: {{ ledgerParty?.name }}</h5>
            <button type="button" class="btn-close" @click="showLedger = false"></button>
          </div>
          <div class="modal-body">
            <div v-if="!ledgerTxns.length" class="text-muted text-center py-3">No transactions found.</div>
            <div v-else class="table-responsive">
              <table class="table table-sm">
                <thead class="table-light">
                  <tr><th>Date</th><th>Particulars</th><th>Debit</th><th>Credit</th><th>Balance</th></tr>
                </thead>
                <tbody>
                  <tr v-for="t in ledgerTxns" :key="t.transaction_id || t.id">
                    <td>{{ t.date?.slice(0, 10) }}</td>
                    <td>{{ t.particulars || t.description || '-' }}</td>
                    <td class="text-danger">{{ t.debit ? currency(t.debit) : '-' }}</td>
                    <td class="text-success">{{ t.credit ? currency(t.credit) : '-' }}</td>
                    <td>{{ currency(t.balance || t.running_balance || 0) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showLedger = false">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-radius: 8px; }
.table th { font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.table td { vertical-align: middle; }
</style>
