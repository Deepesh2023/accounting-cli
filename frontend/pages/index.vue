<script setup lang="ts">
definePageMeta({ title: 'Dashboard' })
</script>

<template>
  <div>
    <div class="header-bar">
      <h1>Financial Module</h1>
      <p class="text-muted">Accounting & Inventory Management</p>
    </div>
    <div class="row g-4 mt-2">
      <div class="col-md-4">
        <div class="stat-card bg-primary text-white">
          <h6>TOTAL SALES (ALL TIME)</h6>
          <h2>₹0.00</h2>
        </div>
      </div>
      <div class="col-md-4">
        <div class="stat-card bg-success text-white">
          <h6>TOTAL PURCHASES</h6>
          <h2>₹0.00</h2>
        </div>
      </div>
      <div class="col-md-4">
        <div class="stat-card bg-info text-white">
          <h6>CASH BALANCE</h6>
          <h2>₹0.00</h2>
        </div>
      </div>
    </div>
    <div class="card mt-4">
      <div class="card-body text-center text-muted py-5">
        <p style="font-size: 1.1rem;">Select a module from the sidebar to get started.</p>
        <p>Use <strong>Sales</strong> to create invoices, <strong>Stock</strong> to manage inventory, and <strong>Reports</strong> for financial statements.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-bar { margin-bottom: 24px; }
.header-bar h1 { margin: 0; font-weight: 700; }
.stat-card { border-radius: 12px; padding: 20px 24px; border: none; }
.stat-card h6 { opacity: 0.8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 8px; }
.stat-card h2 { margin: 0; font-weight: 700; }
.card { border: none; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-radius: 8px; }
</style>
