export interface Expense {
  id: string
  date: string
  category: string
  paidBy: string
  amount: number
  notes: string
}

export const useExpensesStore = defineStore('expenses', () => {
  const expenses = ref<Expense[]>([])

  function add(e: Expense) {
    expenses.value.push(e)
  }

  function update(id: string, data: Partial<Expense>) {
    const idx = expenses.value.findIndex(e => e.id === id)
    if (idx !== -1) Object.assign(expenses.value[idx], data)
  }

  function remove(id: string) {
    expenses.value = expenses.value.filter(e => e.id !== id)
  }

  const totalExpenses = computed(() =>
    expenses.value.reduce((sum, e) => sum + e.amount, 0)
  )

  return { expenses, add, update, remove, totalExpenses }
})
