<script setup lang="ts">
const colorMode = useColorMode()
const route = useRoute()
const nav = useNavigationStore()

const currentSection = computed(() => route.path.replace('/', '') || 'sales')
const sectionTitle = computed(() => nav.sections.find(s => s.id === currentSection.value)?.label || 'Sales')
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-gray-100 dark:bg-gray-950">
    <USidebar v-model:open="nav.sidebarOpen" variant="sidebar" class="!bg-gray-900 !text-white" :ui="{ root: '!bg-gray-900 !text-white', header: 'border-b border-gray-800', footer: 'border-t border-gray-800' }">
      <template #title>
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm">P</div>
          <span class="text-lg font-bold text-white">Printos</span>
        </div>
      </template>

      <div class="space-y-0.5">
        <p class="px-3 py-2 text-xs font-semibold text-gray-400 uppercase tracking-widest">Financial Module</p>
        <UButton
          v-for="s in nav.sections" :key="s.id"
          :to="`/${s.id}`"
          :label="s.label"
          :icon="s.icon"
          variant="ghost"
          block
          class="!justify-start"
          :class="[currentSection === s.id ? '!bg-blue-600 !text-white' : '!text-gray-300 hover:!bg-gray-800 hover:!text-white', s.id === 'company' ? 'mt-3 border-t border-gray-700 pt-3 !rounded-none' : '']"
        />
      </div>
    </USidebar>

    <div class="flex-1 flex flex-col min-w-0">
      <header class="h-14 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 flex items-center justify-between px-4 lg:px-6 shrink-0">
        <div class="flex items-center gap-3">
          <UButton icon="i-heroicons-bars-3" variant="ghost" color="gray" class="lg:hidden" @click="nav.toggleSidebar()" />
          <h1 class="text-lg font-semibold text-gray-900 dark:text-white">{{ sectionTitle }}</h1>
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
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
:deep(.sidebar-root) {
  background-color: #1e293b !important;
}
</style>
