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
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Outstanding</h1>
      <UButton color="primary" variant="outline" @click="loadAll">Refresh</UButton>
    </div>
    <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
      <div v-if="loading" class="text-center py-4 text-gray-500">Loading...</div>
      <div v-else-if="!outstanding.length" class="text-center py-4 text-gray-500">No outstanding items.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Ref No</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Date</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Party</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Type</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Total</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Balance Due</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Due Date</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Status</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="(row, i) in outstanding" :key="i" class="hover:bg-gray-50">
              <td class="px-4 py-3"><code class="text-sm bg-gray-100 px-1 rounded">#{{ row.ref_no || row.sale_id?.slice(0, 8) || row.purchase_id?.slice(0, 8) }}</code></td>
              <td class="px-4 py-3">{{ row.date?.slice(0, 10) }}</td>
              <td class="px-4 py-3">{{ partyName(row.party_id) }}</td>
              <td class="px-4 py-3">
                <UBadge :color="row.type === 'Receivable' || row.balance_amount > 0 ? 'primary' : 'warning'">
                  {{ row.type || (Number(row.balance_amount) > 0 ? 'Receivable' : 'Payable') }}
                </UBadge>
              </td>
              <td class="px-4 py-3">{{ currency(row.total || row.grand_total || 0) }}</td>
              <td class="px-4 py-3 font-bold">{{ currency(row.balance_due || row.balance_amount || 0) }}</td>
              <td class="px-4 py-3">{{ row.due_date?.slice(0, 10) || '-' }}</td>
              <td class="px-4 py-3">
                <UBadge v-if="isOverdue(row)" color="error">Overdue</UBadge>
                <UBadge v-else color="success">On Time</UBadge>
              </td>
              <td class="px-4 py-3">
                <UButton color="success" variant="outline" size="sm" @click="openSettle(row)">Settle</UButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <UModal v-model:open="showSettle">
      <template #header>
        <h3 class="text-lg font-semibold">Settle Outstanding</h3>
      </template>
      <p>Party: <strong>{{ partyName(settleTarget?.party_id) }}</strong></p>
      <p>Balance Due: <strong>{{ currency(settleTarget?.balance_due || settleTarget?.balance_amount || 0) }}</strong></p>
      <div class="mt-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Settle Amount</label>
        <UInput v-model.number="settleAmount" type="number" step="0.01" />
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton color="neutral" variant="outline" @click="showSettle = false">Cancel</UButton>
          <UButton color="success" @click="confirmSettle">Confirm</UButton>
        </div>
      </template>
    </UModal>
  </div>
</template>

<style scoped>
</style>
