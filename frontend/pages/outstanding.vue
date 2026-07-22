<script setup lang="ts">
import type { PartyResponse } from '~/lib/api/client'

definePageMeta({ title: 'Outstanding' })

const outstanding = ref<any[]>([])
const parties = ref<PartyResponse[]>([])
const loading = ref(false)
const settleAmount = ref(0)
const showSettle = ref(false)
const settleTarget = ref<any>(null)

onMounted(loadAll)

async function loadAll() {
  loading.value = true
  try {
    const [o, p] = await Promise.all([
      api().getOutstandingReport(),
      api().listParties(),
    ])
    outstanding.value = Array.isArray(o) ? o : []
    parties.value = p
  } finally { loading.value = false }
}

function partyName(id: string | undefined) {
  return parties.value.find(p => p.party_id === id)?.name || 'Unknown'
}

function openSettle(row: any) {
  settleTarget.value = row
  settleAmount.value = Number(row.balance_due || row.balance_amount || 0)
  showSettle.value = true
}

async function confirmSettle() {
  if (!settleTarget.value) return
  try {
    const id = settleTarget.value.party_id || settleTarget.value.sale_id || settleTarget.value.purchase_id
    await api().adjustPartyBalance(id, { amount: settleAmount.value })
    showSettle.value = false
    await loadAll()
  } catch (e: any) { alert(e.message) }
}

function isOverdue(row: any) {
  if (!row.due_date) return false
  return new Date(row.due_date) < new Date()
}

const currency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Outstanding</h1>
      <button class="btn btn-outline-primary" @click="loadAll">Refresh</button>
    </div>
    <div class="card">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-4 text-muted">Loading...</div>
        <div v-else-if="!outstanding.length" class="text-center py-4 text-muted">No outstanding items.</div>
        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr><th>Ref No</th><th>Date</th><th>Party</th><th>Type</th><th>Total</th><th>Balance Due</th><th>Due Date</th><th>Status</th><th>Actions</th></tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in outstanding" :key="i">
                <td><code>#{{ row.ref_no || row.sale_id?.slice(0, 8) || row.purchase_id?.slice(0, 8) }}</code></td>
                <td>{{ row.date?.slice(0, 10) }}</td>
                <td>{{ partyName(row.party_id) }}</td>
                <td>
                  <span :class="row.type === 'Receivable' || row.balance_amount > 0 ? 'badge bg-info' : 'badge bg-warning'">
                    {{ row.type || (Number(row.balance_amount) > 0 ? 'Receivable' : 'Payable') }}
                  </span>
                </td>
                <td>{{ currency(row.total || row.grand_total || 0) }}</td>
                <td class="fw-bold">{{ currency(row.balance_due || row.balance_amount || 0) }}</td>
                <td>{{ row.due_date?.slice(0, 10) || '-' }}</td>
                <td>
                  <span v-if="isOverdue(row)" class="badge bg-danger">Overdue</span>
                  <span v-else class="badge bg-success">On Time</span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-success" @click="openSettle(row)">Settle</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showSettle" class="modal-backdrop fade show" @click="showSettle = false"></div>
    <div v-if="showSettle" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-sm">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Settle Outstanding</h5>
            <button type="button" class="btn-close" @click="showSettle = false"></button>
          </div>
          <div class="modal-body">
            <p>Party: <strong>{{ partyName(settleTarget?.party_id) }}</strong></p>
            <p>Balance Due: <strong>{{ currency(settleTarget?.balance_due || settleTarget?.balance_amount || 0) }}</strong></p>
            <div class="mb-3">
              <label class="form-label">Settle Amount</label>
              <input v-model.number="settleAmount" type="number" step="0.01" class="form-control" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showSettle = false">Cancel</button>
            <button class="btn btn-success" @click="confirmSettle">Confirm</button>
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
