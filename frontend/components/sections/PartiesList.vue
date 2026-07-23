<script setup lang="ts">
const store = usePartiesStore()
const partyModal = ref<InstanceType<typeof PartyFormModal>>()

function deleteParty(id: string) {
  store.remove(id)
}

function editParty(party: any) {
  partyModal.value?.openEdit(party)
}
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="font-semibold text-gray-900 dark:text-white">Parties (Debtors & Creditors)</h3>
        <UButton label="+ Add Party" color="primary" size="sm" @click="partyModal?.openCreate()" />
      </div>
    </template>

    <div class="bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-sm p-3 rounded-lg mb-4">
      <strong>Tip:</strong> Double-click a row to edit. Right-click a row to delete.
    </div>

    <UTable
      :rows="store.parties"
      :columns="[
        { key: 'index', label: '#' },
        { key: 'name', label: 'Name', sortable: true },
        { key: 'phone', label: 'Phone' },
        { key: 'state', label: 'State' },
        { key: 'type', label: 'Type', sortable: true },
        { key: 'balance', label: 'Balance (₹)', sortable: true },
        { key: 'actions', label: 'Actions' },
      ]"
    >
      <template #index-data="{ index }">
        {{ index + 1 }}
      </template>
      <template #type-data="{ row }">
        <UBadge :color="row.type === 'DEBTOR' ? 'blue' : 'orange'" variant="soft">
          {{ row.type === 'DEBTOR' ? 'Receive' : 'Pay' }}
        </UBadge>
      </template>
      <template #balance-data="{ row }">
        <span :class="row.balance >= 0 ? 'text-green-600' : 'text-red-600'" class="font-medium">
          ₹ {{ Math.abs(row.balance).toFixed(2) }}
        </span>
      </template>
      <template #actions-data="{ row }">
        <div class="flex gap-1">
          <UButton icon="i-heroicons-pencil-square" color="gray" variant="ghost" size="2xs" @click="editParty(row)"  tooltip="Edit" />
          <UButton icon="i-heroicons-trash" color="red" variant="ghost" size="2xs" @click="deleteParty(row.id)"  tooltip="Delete" />
        </div>
      </template>
      <template #empty>
        <div class="text-center py-8 text-gray-400">
          <UIcon name="i-heroicons-users" class="w-12 h-12 mx-auto mb-2" />
          <p>No parties yet. Add your first party!</p>
        </div>
      </template>
    </UTable>

    <PartyFormModal ref="partyModal" />
  </UCard>
</template>
