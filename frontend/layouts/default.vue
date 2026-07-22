<script setup lang="ts">
const route = useRoute()
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
</script>

<template>
  <div class="app-layout">
    <aside class="sidebar">
      <h4 class="sidebar-title">Printos</h4>
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
      <slot />
    </main>
  </div>
</template>

<style scoped>
.app-layout { display: flex; min-height: 100vh; }
.sidebar {
  width: 240px; background: #212529; color: #fff;
  padding: 20px 0; display: flex; flex-direction: column;
  position: fixed; top: 0; left: 0; height: 100vh; z-index: 100;
}
.sidebar-title {
  text-align: center; margin-bottom: 24px; font-weight: 700;
  padding: 0 16px;
}
.nav-link {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 20px; color: #adb5bd; text-decoration: none;
  transition: 0.2s; border-radius: 0; margin: 2px 8px;
  border-radius: 6px; font-size: 0.9rem;
}
.nav-link:hover, .nav-link.active { color: #fff; background: #0d6efd; }
.nav-icon { font-size: 1.1rem; width: 20px; text-align: center; }
.main-content { margin-left: 240px; flex: 1; padding: 24px 32px; overflow-y: auto; }
</style>
