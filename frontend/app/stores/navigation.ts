export const useNavigationStore = defineStore('navigation', () => {
  const sidebarOpen = ref(true)

  const sections = [
    { id: 'sales', label: 'Sales', icon: 'i-heroicons-currency-rupee' },
    { id: 'purchases', label: 'Purchases', icon: 'i-heroicons-arrow-trending-down' },
    { id: 'outstanding', label: 'Outstanding', icon: 'i-heroicons-exclamation-triangle' },
    { id: 'expenses', label: 'Expenses', icon: 'i-heroicons-banknotes' },
    { id: 'quotations', label: 'Quotations', icon: 'i-heroicons-document-text' },
    { id: 'transactions', label: 'Transactions', icon: 'i-heroicons-arrow-path' },
    { id: 'parties', label: 'Parties', icon: 'i-heroicons-users' },
    { id: 'stock', label: 'Stock', icon: 'i-heroicons-cube' },
    { id: 'reports', label: 'Reports', icon: 'i-heroicons-chart-bar' },
    { id: 'company', label: 'Company', icon: 'i-heroicons-building-office-2' },
  ]

  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  return { sidebarOpen, sections, toggleSidebar }
})
