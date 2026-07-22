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
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="m-0">Expenses</h1>
      <button class="btn btn-primary" @click="openAdd">+ Add Expense</button>
    </div>
    <div class="row g-3 mb-4">
      <div class="col-12 col-md-4">
        <div class="stat-card bg-danger text-white">
          <h6>TOTAL EXPENSES</h6>
          <h2>{{ currency(totalExpenses) }}</h2>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-body p-0">
        <div v-if="loading" class="text-center py-4 text-muted">Loading...</div>
        <div v-else-if="!expenses.length" class="text-center py-4 text-muted">No expenses recorded.</div>
        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr><th>Date</th><th>Category</th><th>Paid By</th><th>Notes</th><th>Amount</th><th>Actions</th></tr>
            </thead>
            <tbody>
              <tr v-for="e in expenses" :key="e.expense_id">
                <td>{{ e.date?.slice(0, 10) }}</td>
                <td><span class="badge bg-secondary">{{ e.category }}</span></td>
                <td>{{ e.paid_by }}</td>
                <td>{{ e.notes || '-' }}</td>
                <td class="text-danger">{{ currency(e.amount) }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-1" @click="openEdit(e)">Edit</button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(e.expense_id)">Delete</button>
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
            <h5 class="modal-title">{{ editing ? 'Edit' : 'Add' }} Expense</h5>
            <button type="button" class="btn-close" @click="showModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Date</label>
              <input v-model="form.date" type="date" class="form-control" />
            </div>
            <div class="mb-3">
              <label class="form-label">Category</label>
              <select v-model="form.category" class="form-select">
                <option value="" disabled>Select category</option>
                <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
              </select>
            </div>
            <div class="row g-3">
              <div class="col-12 col-sm-6">
                <label class="form-label">Paid By</label>
                <select v-model="form.paid_by" class="form-select">
                  <option value="Cash">Cash</option>
                  <option value="Bank">Bank</option>
                </select>
              </div>
              <div class="col-12 col-sm-6">
                <label class="form-label">Amount</label>
                <input v-model.number="form.amount" type="number" step="0.01" class="form-control" />
              </div>
            </div>
            <div class="mb-3 mt-3">
              <label class="form-label">Notes</label>
              <textarea v-model="form.notes" class="form-control" rows="2"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showModal = false">Cancel</button>
            <button class="btn btn-primary" @click="save">Save</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stat-card { border-radius: 12px; padding: 20px 24px; border: none; }
.stat-card h6 { opacity: 0.8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 8px; }
.stat-card h2 { margin: 0; font-weight: 700; }
.card { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-radius: 8px; }
.table th { font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.table td { vertical-align: middle; }
</style>
