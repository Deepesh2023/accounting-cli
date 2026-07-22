<script setup lang="ts">
const route = useRoute()
const sidebarOpen = ref(false)

const sidebarLinks = [
  { label: 'Dashboard', icon: '📊', to: '/' },
  { label: 'Sales', icon: '💰', to: '/sales' },
  { label: 'Purchases', icon: '📥', to: '/purchases' },
  { label: 'Outstanding', icon: '⚠️', to: '/outstanding' },
  { label: 'Expenses', icon: '💸', to: '/expenses' },
  { label: 'Quotations', icon: '📄', to: '/quotations' },
  { label: 'Transactions', icon: '🔄', to: '/transactions' },
  { label: 'Parties', icon: '👥', to: '/parties' },
  { label: 'Stock', icon: '📦', to: '/stock' },
  { label: 'Reports', icon: '📈', to: '/reports' },
  { label: 'Company', icon: '🏢', to: '/company' },
]

watch(route, () => { sidebarOpen.value = false })
</script>

<template>
  <div class="app-layout">
    <div
      class="sidebar-overlay"
      :class="{ show: sidebarOpen }"
      @click="sidebarOpen = false"
    />
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <h4 class="sidebar-title">Printos</h4>
        <button class="sidebar-close d-lg-none" @click="sidebarOpen = false">&times;</button>
      </div>
      <nav>
        <NuxtLink
          v-for="link in sidebarLinks"
          :key="link.to"
          :to="link.to"
          class="nav-link"
          :class="{ active: route.path === link.to }"
        >
          <span class="nav-icon">{{ link.icon }}</span>
          {{ link.label }}
        </NuxtLink>
      </nav>
    </aside>
    <main class="main-content">
      <button class="hamburger d-lg-none" @click="sidebarOpen = true">
        <span /> <span /> <span />
      </button>
      <slot />
    </main>
  </div>
</template>

<style scoped>
.app-layout { display: flex; min-height: 100vh; }
.sidebar-overlay {
  display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  z-index: 98;
}
.sidebar-overlay.show { display: block; }

.sidebar {
  width: 240px; background: #212529; color: #fff;
  padding: 0; display: flex; flex-direction: column;
  position: fixed; top: 0; left: 0; height: 100vh; z-index: 100;
  transition: transform 0.3s ease;
}
.sidebar-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 16px 8px;
}
.sidebar-title { margin: 0; font-weight: 700; }
.sidebar-close {
  background: none; border: none; color: #fff; font-size: 1.5rem;
  cursor: pointer; padding: 0; line-height: 1;
}
.nav-link {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 20px; color: #adb5bd; text-decoration: none;
  transition: 0.2s; margin: 2px 8px;
  border-radius: 6px; font-size: 0.9rem;
}
.nav-link:hover, .nav-link.active { color: #fff; background: #0d6efd; }
.nav-icon { font-size: 1.1rem; width: 20px; text-align: center; }
.main-content {
  margin-left: 240px; flex: 1; padding: 24px 32px; overflow-y: auto;
  min-height: 100vh;
}
.hamburger {
  display: none; background: #212529; border: none; border-radius: 6px;
  padding: 8px 10px; cursor: pointer; margin-bottom: 16px;
  flex-direction: column; gap: 4px;
}
.hamburger span {
  display: block; width: 22px; height: 2px; background: #fff;
  border-radius: 2px;
}
@media (max-width: 991.98px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .main-content { margin-left: 0; padding: 16px; }
  .hamburger { display: inline-flex; }
}
</style>
