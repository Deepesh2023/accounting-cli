<script setup lang="ts">
const store = useExpensesStore()

const open = ref(false)
const editingId = ref<string | null>(null)
const form = reactive({
  date: new Date().toISOString().split('T')[0],
  category: 'Rent',
  paidBy: 'Cash',
  amount: 0,
  notes: '',
})

function openCreate() {
  editingId.value = null
  form.date = new Date().toISOString().split('T')[0]
  form.category = 'Rent'
  form.paidBy = 'Cash'
  form.amount = 0
  form.notes = ''
  open.value = true
}

function openEdit(expense: { id: string; date: string; category: string; paidBy: string; amount: number; notes: string }) {
  editingId.value = expense.id
  form.date = expense.date
  form.category = expense.category
  form.paidBy = expense.paidBy
  form.amount = expense.amount
  form.notes = expense.notes
  open.value = true
}

function submit() {
  if (!form.amount) return
  const data = {
    id: editingId.value || crypto.randomUUID(),
    date: form.date,
    category: form.category,
    paidBy: form.paidBy,
    amount: form.amount,
    notes: form.notes,
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
  <UModal v-model:open="open" :title="editingId ? 'Edit Expense' : 'Add Expense'">
    <template #body>
      <form @submit.prevent="submit" class="space-y-4">
        <UFormField label="Date">
          <UInput v-model="form.date" type="date" class="w-full" />
        </UFormField>
        <UFormField label="Category">
          <USelect v-model="form.category" :items="['Rent', 'Utilities', 'Salary', 'Marketing', 'Office Supplies', 'Travel', 'Other']" class="w-full" />
        </UFormField>
        <UFormField label="Paid By">
          <USelect v-model="form.paidBy" :items="['Cash', 'Bank']" class="w-full" />
        </UFormField>
        <UFormField label="Amount (₹)">
          <UInput v-model="form.amount" type="number" min="0" step="0.01" class="w-full" />
        </UFormField>
        <UFormField label="Notes">
          <UTextarea v-model="form.notes" rows="2" placeholder="Optional notes" class="w-full" />
        </UFormField>
      </form>
    </template>
    <template #footer>
      <UButton label="Cancel" variant="ghost" color="gray" @click="open = false" />
      <UButton :label="editingId ? 'Update' : 'Save'" color="primary" @click="submit" />
    </template>
  </UModal>
</template>
