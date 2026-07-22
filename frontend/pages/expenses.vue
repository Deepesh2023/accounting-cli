<script setup lang="ts">
import type { ExpenseResponse, ExpenseCreate, ExpenseUpdate } from '~/lib/api/client'

definePageMeta({ title: 'Expenses' })

const expenses = ref<ExpenseResponse[]>([])
const loading = ref(false)
const showModal = ref(false)
const editing = ref<string | null>(null)
const form = ref<ExpenseCreate>({ category: '', paid_by: 'Cash', amount: 0, notes: '' })

const categories = ['Rent', 'Utilities', 'Salary', 'Office Supplies', 'Travel', 'Marketing', 'Maintenance', 'Legal', 'Other']

onMounted(fetchAll)

async function fetchAll() {
  loading.value = true
  try { expenses.value = await api().listExpenses() }
  finally { loading.value = false }
}

function openAdd() {
  editing.value = null
  form.value = { category: '', paid_by: 'Cash', amount: 0, notes: '' }
  showModal.value = true
}

function openEdit(e: ExpenseResponse) {
  editing.value = e.expense_id
  form.value = { category: e.category, paid_by: e.paid_by, amount: Number(e.amount), notes: e.notes || '' }
  showModal.value = true
}

async function save() {
  try {
    if (editing.value) {
      await api().updateExpense(editing.value, form.value as ExpenseUpdate)
    } else {
      await api().createExpense(form.value)
    }
    showModal.value = false
    await fetchAll()
  } catch (e: any) { alert(e.message) }
}

async function confirmDelete(id: string) {
  if (confirm('Delete this expense?')) {
    await api().deleteExpense(id)
    await fetchAll()
  }
}

const totalExpenses = computed(() => expenses.value.reduce((s, e) => s + Number(e.amount), 0))
const currency = (v: string | number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(Number(v))
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Expenses</h1>
      <UButton color="primary" @click="openAdd">+ Add Expense</UButton>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
      <div class="rounded-xl p-5 bg-red-600 text-white shadow-sm">
        <h6 class="text-xs uppercase tracking-wider opacity-80 mb-2">TOTAL EXPENSES</h6>
        <h2 class="text-2xl font-bold">{{ currency(totalExpenses) }}</h2>
      </div>
    </div>
    <UCard>
      <div v-if="loading" class="text-center py-4 text-gray-500">Loading...</div>
      <div v-else-if="!expenses.length" class="text-center py-4 text-gray-500">No expenses recorded.</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Date</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Category</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Paid By</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Notes</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Amount</th>
              <th class="text-left px-4 py-3 font-semibold text-xs uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="e in expenses" :key="e.expense_id" class="hover:bg-gray-50">
              <td class="px-4 py-3">{{ e.date?.slice(0, 10) }}</td>
              <td class="px-4 py-3"><UBadge color="neutral">{{ e.category }}</UBadge></td>
              <td class="px-4 py-3">{{ e.paid_by }}</td>
              <td class="px-4 py-3">{{ e.notes || '-' }}</td>
              <td class="px-4 py-3 text-red-600 font-medium">{{ currency(e.amount) }}</td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <UButton color="primary" variant="outline" size="sm" @click="openEdit(e)">Edit</UButton>
                  <UButton color="error" variant="outline" size="sm" @click="confirmDelete(e.expense_id)">Delete</UButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UCard>

    <UModal v-model:open="showModal">
      <template #title>{{ editing ? 'Edit' : 'Add' }} Expense</template>
      <div class="space-y-4">
        <UInput v-model="form.date" type="date" label="Date" />
        <USelect v-model="form.category" :items="categories" placeholder="Category" />
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <USelect v-model="form.paid_by" :items="['Cash', 'Bank']" label="Paid By" />
          <UInput v-model.number="form.amount" type="number" step="0.01" label="Amount" />
        </div>
        <UTextarea v-model="form.notes" placeholder="Notes" :rows="2" />
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <UButton color="neutral" variant="outline" @click="showModal = false">Cancel</UButton>
          <UButton color="primary" @click="save">Save</UButton>
        </div>
      </template>
    </UModal>
  </div>
</template>
