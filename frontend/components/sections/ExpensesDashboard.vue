<script setup lang="ts">
const store = useExpensesStore()
const expenseModal = ref<InstanceType<typeof ExpenseFormModal>>()

function deleteExpense(id: string) {
  store.remove(id)
}

function editExpense(expense: any) {
  expenseModal.value?.openEdit(expense)
}
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-gray-900 dark:text-white">Expenses</h3>
        <UButton label="+ Add Expense" color="primary" size="sm" @click="expenseModal?.openCreate()" />
      </div>
    </template>

    <UTable
      :rows="store.expenses"
      :columns="[
        { key: 'date', label: 'Date', sortable: true },
        { key: 'category', label: 'Category', sortable: true },
        { key: 'paidBy', label: 'Paid By' },
        { key: 'notes', label: 'Notes' },
        { key: 'amount', label: 'Amount (₹)', sortable: true },
        { key: 'actions', label: 'Actions' },
      ]"
    >
      <template #amount-data="{ row }">
        <span class="font-medium">₹ {{ row.amount.toFixed(2) }}</span>
      </template>
      <template #actions-data="{ row }">
        <div class="flex gap-1">
          <UTooltip text="Edit">
            <UButton icon="i-heroicons-pencil-square" color="gray" variant="ghost" size="2xs" @click="editExpense(row)" />
          </UTooltip>
          <UTooltip text="Delete">
            <UButton icon="i-heroicons-trash" color="red" variant="ghost" size="2xs" @click="deleteExpense(row.id)" />
          </UTooltip>
        </div>
      </template>
      <template #empty>
        <div class="text-center py-8 text-gray-400">
          <UIcon name="i-heroicons-banknotes" class="w-12 h-12 mx-auto mb-2" />
          <p>No expenses recorded yet.</p>
        </div>
      </template>
    </UTable>

    <ExpenseFormModal ref="expenseModal" />
  </UCard>
</template>
