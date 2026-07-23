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
    <!-- Desktop sidebar -->
    <aside class="hidden lg:flex flex-col w-64 border-r border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shrink-0">
      <div class="flex items-center gap-2.5 px-5 h-14 border-b border-gray-200 dark:border-gray-800">
        <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-sm">P</div>
        <span class="text-lg font-bold text-gray-900 dark:text-white">Printos</span>
      </div>
      <nav class="flex-1 overflow-y-auto p-3 space-y-0.5">
        <p class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-widest">Financial Module</p>
        <button
          v-for="s in nav.sections" :key="s.id"
          @click="nav.navigateTo(s.id)"
          :class="[
            'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-left',
            nav.currentSection === s.id
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
      <div v-if="nav.mobileOpen" class="lg:hidden fixed inset-0 z-50 flex">
        <div class="absolute inset-0 bg-black/50" @click="nav.mobileOpen = false" />
        <aside class="relative w-64 bg-white dark:bg-gray-900 shadow-xl flex flex-col">
          <div class="flex items-center justify-between px-5 h-14 border-b border-gray-200 dark:border-gray-800">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold text-sm">P</div>
              <span class="text-lg font-bold text-gray-900 dark:text-white">Printos</span>
            </div>
            <button @click="nav.mobileOpen = false" class="text-gray-400 hover:text-gray-600">
              <UIcon name="i-heroicons-x-mark" class="w-6 h-6" />
            </button>
          </div>
          <nav class="flex-1 overflow-y-auto p-3 space-y-0.5">
            <p class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-widest">Financial Module</p>
            <button
              v-for="s in nav.sections" :key="s.id"
              @click="nav.navigateTo(s.id)"
              :class="[
                'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-left',
                nav.currentSection === s.id
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
          <button class="lg:hidden text-gray-500 hover:text-gray-700 dark:hover:text-gray-300" @click="nav.toggleMobile()">
            <UIcon name="i-heroicons-bars-3" class="w-6 h-6" />
          </button>
          <h1 class="text-lg font-semibold text-gray-900 dark:text-white">{{ nav.sectionTitle }}</h1>
        </div>
        <div class="flex items-center gap-2">
          <UButton
            :icon="colorMode.preference === 'dark' ? 'i-heroicons-sun' : 'i-heroicons-moon'"
            variant="ghost"
            color="gray"
            :tooltip="colorMode.preference === 'dark' ? 'Switch to light' : 'Switch to dark'"
            @click="colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark'"
          />
        </div>
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
