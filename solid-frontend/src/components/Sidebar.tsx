import { For, createSignal } from 'solid-js'

export type Section =
  | 'sales'
  | 'purchases'
  | 'outstanding'
  | 'expenses'
  | 'quotation'
  | 'transactions'
  | 'parties'
  | 'stock'
  | 'financial-statements'
  | 'company'

const [activeSection, setActiveSection] = createSignal<Section>('sales')

export { activeSection, setActiveSection }

const navItems: { id: Section; label: string }[] = [
  { id: 'sales', label: 'Sales' },
  { id: 'purchases', label: 'Purchases' },
  { id: 'outstanding', label: 'Outstanding Report' },
  { id: 'expenses', label: 'Expenses' },
  { id: 'quotation', label: 'Quotation' },
  { id: 'transactions', label: 'Transaction History' },
  { id: 'parties', label: 'Parties' },
  { id: 'stock', label: 'Stock' },
  { id: 'financial-statements', label: 'Financial Statements' },
]

export default function Sidebar() {
  const current = activeSection

  return (
    <div class="w-[260px] min-h-screen bg-[#212529] text-white flex flex-col p-3">
      <h4 class="text-center text-white mb-4">Printos</h4>
      <ul class="flex flex-col gap-0.5 mb-auto">
        <h6 class="px-3 mt-2 mb-3 text-[#adb5bd] uppercase text-[0.75rem] tracking-[0.5px] font-semibold">
          Financial Module
        </h6>
        <For each={navItems}>
          {(item) => (
            <li>
              <button
                onClick={() => setActiveSection(item.id)}
                class={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors cursor-pointer ${
                  current() === item.id
                    ? 'bg-[#0d6efd] text-white'
                    : 'text-[#adb5bd] hover:text-white hover:bg-[#0d6efd]'
                }`}
              >
                {item.label}
              </button>
            </li>
          )}
        </For>
      </ul>
      <ul class="border-t border-[#adb5bd]/20 pt-3 mt-3">
        <li>
          <button
            onClick={() => setActiveSection('company')}
            class={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors cursor-pointer ${
              current() === 'company'
                ? 'bg-[#0d6efd] text-white'
                : 'text-[#adb5bd] hover:text-white hover:bg-[#0d6efd]'
            }`}
          >
            Company Details
          </button>
        </li>
      </ul>
    </div>
  )
}
