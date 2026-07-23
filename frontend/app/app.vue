<script setup lang="ts">
const colorMode = useColorMode()
const nav = useNavigationStore()

useHead({
  htmlAttrs: { lang: 'en' }
})

useSeoMeta({
  title: 'Printos - Financial Accounting',
  ogTitle: 'Printos',
})
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-white dark:bg-gray-950">
    <USidebar v-model:open="nav.sidebarOpen" title="Printos" description="Financial Module" variant="sidebar">
      <template #title>
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-sm">P</div>
          <span class="text-lg font-bold">Printos</span>
        </div>
      </template>

      <div class="space-y-0.5">
        <p class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-widest">Financial Module</p>
        <UButton
          v-for="s in nav.sections" :key="s.id"
          @click="nav.navigateTo(s.id)"
          :label="s.label"
          :icon="s.icon"
          variant="ghost"
          block
          :class="nav.currentSection === s.id ? 'bg-primary text-white' : ''"
        />
      </div>
    </USidebar>

    <div class="flex-1 flex flex-col min-w-0">
      <header class="h-14 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 flex items-center justify-between px-4 lg:px-6 shrink-0">
        <div class="flex items-center gap-3">
          <UButton icon="i-heroicons-bars-3" variant="ghost" color="gray" class="lg:hidden" @click="nav.toggleSidebar()" />
          <h1 class="text-lg font-semibold text-gray-900 dark:text-white">{{ nav.sectionTitle }}</h1>
        </div>
        <UButton
          :icon="colorMode.preference === 'dark' ? 'i-heroicons-sun' : 'i-heroicons-moon'"
          variant="ghost"
          color="gray"
          :tooltip="colorMode.preference === 'dark' ? 'Switch to light' : 'Switch to dark'"
          @click="colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark'"
        />
      </header>

      <main class="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-950 p-4 lg:p-6">
        <SalesDashboard v-if="nav.currentSection === 'sales'" />
        <PurchasesDashboard v-else-if="nav.currentSection === 'purchases'" />
        <OutstandingReport v-else-if="nav.currentSection === 'outstanding'" />
        <ExpensesDashboard v-else-if="nav.currentSection === 'expenses'" />
        <QuotationsDashboard v-else-if="nav.currentSection === 'quotations'" />
        <TransactionHistory v-else-if="nav.currentSection === 'transactions'" />
        <PartiesList v-else-if="nav.currentSection === 'parties'" />
        <StockInventory v-else-if="nav.currentSection === 'stock'" />
        <FinancialStatements v-else-if="nav.currentSection === 'reports'" />
        <CompanyProfile v-else-if="nav.currentSection === 'company'" />
      </main>
    </div>
  </div>
</template>
