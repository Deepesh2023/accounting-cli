<script setup lang="ts">
const colorMode = useColorMode()
const currentSection = ref('sales')
const mobileOpen = ref(false)

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

function navigateTo(id: string) {
  currentSection.value = id
  mobileOpen.value = false
}

const sectionTitle = computed(() => sections.find(s => s.id === currentSection.value)?.label || currentSection.value)
</script>

<template>
  <UTooltipProvider>
  <div class="flex h-screen overflow-hidden bg-white dark:bg-gray-950">
    <!-- Desktop sidebar -->
    <aside class="hidden lg:flex flex-col w-64 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shrink-0">
      <div class="flex items-center gap-2.5 px-5 h-14 border-b border-gray-200 dark:border-gray-800">
        <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-sm">P</div>
        <span class="text-lg font-bold text-gray-900 dark:text-white">Printos</span>
      </div>
      <nav class="flex-1 overflow-y-auto p-3 space-y-0.5">
        <p class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-widest">Financial Module</p>
        <button
          v-for="s in sections" :key="s.id"
          @click="navigateTo(s.id)"
          :class="[
            'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-left',
            currentSection === s.id
              ? 'bg-primary text-white shadow-sm'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
          ]"
        >
          <UIcon :name="s.icon" class="w-5 h-5 shrink-0" />
          <span class="truncate">{{ s.label }}</span>
        </button>
      </nav>
    </aside>

    <!-- Mobile sidebar overlay -->
    <Teleport to="body">
      <div v-if="mobileOpen" class="lg:hidden fixed inset-0 z-50 flex">
        <div class="absolute inset-0 bg-black/50" @click="mobileOpen = false" />
        <aside class="relative w-64 bg-white dark:bg-gray-900 shadow-xl flex flex-col">
          <div class="flex items-center justify-between px-5 h-14 border-b border-gray-200 dark:border-gray-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-sm">P</div>
              <span class="text-lg font-bold text-gray-900 dark:text-white">Printos</span>
            </div>
            <button @click="mobileOpen = false" class="text-gray-400 hover:text-gray-600">
              <UIcon name="i-heroicons-x-mark" class="w-6 h-6" />
            </button>
          </div>
          <nav class="flex-1 overflow-y-auto p-3 space-y-0.5">
            <p class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-widest">Financial Module</p>
            <button
              v-for="s in sections" :key="s.id"
              @click="navigateTo(s.id)"
              :class="[
                'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-left',
                currentSection === s.id
                  ? 'bg-primary text-white shadow-sm'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              ]"
            >
              <UIcon :name="s.icon" class="w-5 h-5 shrink-0" />
              <span class="truncate">{{ s.label }}</span>
            </button>
          </nav>
        </aside>
      </div>
    </Teleport>

    <!-- Main area -->
    <div class="flex-1 flex flex-col min-w-0">
      <header class="h-14 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 flex items-center justify-between px-4 lg:px-6 shrink-0">
        <div class="flex items-center gap-3">
          <button class="lg:hidden text-gray-500 hover:text-gray-700 dark:hover:text-gray-300" @click="mobileOpen = true">
            <UIcon name="i-heroicons-bars-3" class="w-6 h-6" />
          </button>
          <h1 class="text-lg font-semibold text-gray-900 dark:text-white">{{ sectionTitle }}</h1>
        </div>
        <div class="flex items-center gap-2">
          <UTooltip :text="colorMode.preference === 'dark' ? 'Switch to light' : 'Switch to dark'">
            <UButton
              :icon="colorMode.preference === 'dark' ? 'i-heroicons-sun' : 'i-heroicons-moon'"
              variant="ghost"
              color="gray"
              @click="colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark'"
            />
          </UTooltip>
        </div>
      </header>

      <main class="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-950 p-4 lg:p-6">
        <SalesDashboard v-if="currentSection === 'sales'" />
        <PurchasesDashboard v-else-if="currentSection === 'purchases'" />
        <OutstandingReport v-else-if="currentSection === 'outstanding'" />
        <ExpensesDashboard v-else-if="currentSection === 'expenses'" />
        <QuotationsDashboard v-else-if="currentSection === 'quotations'" />
        <TransactionHistory v-else-if="currentSection === 'transactions'" />
        <PartiesList v-else-if="currentSection === 'parties'" />
        <StockInventory v-else-if="currentSection === 'stock'" />
        <FinancialStatements v-else-if="currentSection === 'reports'" />
        <CompanyProfile v-else-if="currentSection === 'company'" />
      </main>
    </div>
  </div>
  </UTooltipProvider>
</template>
