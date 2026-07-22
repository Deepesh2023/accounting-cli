<script setup lang="ts">
const route = useRoute()
const mobileOpen = ref(false)

const links = [
  { label: 'Dashboard', icon: 'i-heroicons-presentation-chart-bar', to: '/' },
  { label: 'Sales', icon: 'i-heroicons-currency-rupee', to: '/sales' },
  { label: 'Purchases', icon: 'i-heroicons-arrow-down-tray', to: '/purchases' },
  { label: 'Outstanding', icon: 'i-heroicons-exclamation-triangle', to: '/outstanding' },
  { label: 'Expenses', icon: 'i-heroicons-banknotes', to: '/expenses' },
  { label: 'Quotations', icon: 'i-heroicons-document-text', to: '/quotations' },
  { label: 'Transactions', icon: 'i-heroicons-arrow-path', to: '/transactions' },
  { label: 'Parties', icon: 'i-heroicons-users', to: '/parties' },
  { label: 'Stock', icon: 'i-heroicons-cube', to: '/stock' },
  { label: 'Reports', icon: 'i-heroicons-chart-bar', to: '/reports' },
  { label: 'Company', icon: 'i-heroicons-building-office-2', to: '/company' },
]

watch(route, () => { mobileOpen.value = false })
</script>

<template>
  <div class="flex min-h-screen">
    <UButton
      class="fixed top-3 left-3 z-50 lg:hidden"
      color="neutral"
      variant="solid"
      icon="i-heroicons-bars-3"
      @click="mobileOpen = !mobileOpen"
    />
    <div
      class="fixed inset-0 bg-black/50 z-40 lg:hidden"
      :class="mobileOpen ? 'block' : 'hidden'"
      @click="mobileOpen = false"
    />
    <aside
      class="fixed top-0 left-0 z-40 h-full w-60 bg-gray-900 transition-transform duration-300 lg:translate-x-0 overflow-y-auto"
      :class="mobileOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="p-4 border-b border-gray-700">
      <h4 class="text-white font-bold text-lg text-center">Printos</h4>
      </div>
      <div class="px-3 pt-4 pb-1 text-xs uppercase tracking-wider text-gray-500 font-semibold">Financial Module</div>
      <nav class="p-2 space-y-1">
        <NuxtLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors"
          :class="route.path === link.to ? 'bg-primary text-white' : 'text-gray-300 hover:bg-gray-800 hover:text-white'"
        >
          <UIcon :name="link.icon" class="w-5 h-5" />
          {{ link.label }}
        </NuxtLink>
      </nav>
    </aside>
    <main class="flex-1 lg:ml-60 p-4 md:p-8 min-h-screen">
      <slot />
    </main>
  </div>
</template>
