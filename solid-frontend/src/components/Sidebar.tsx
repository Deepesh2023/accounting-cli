import { For } from 'solid-js'
import { Link } from '@tanstack/solid-router'
import { companyData } from '../lib/store'

const navItems: { to: string; label: string }[] = [
  { to: '/sales', label: 'Sales' },
  { to: '/purchases', label: 'Purchases' },
  { to: '/outstanding', label: 'Outstanding Report' },
  { to: '/expenses', label: 'Expenses' },
  { to: '/quotation', label: 'Quotation' },
  { to: '/transactions', label: 'Transaction History' },
  { to: '/parties', label: 'Parties' },
  { to: '/stock', label: 'Stock' },
  { to: '/financial-statements', label: 'Financial Statements' },
]

const linkClass =
  'block px-4 py-2 text-sm rounded-[5px] transition-colors cursor-pointer no-underline text-[#adb5bd] hover:text-white hover:bg-[#0d6efd]'

export default function Sidebar() {
  return (
    <div class="w-[260px] min-h-screen bg-[#212529] text-white flex flex-col pt-5 px-3 pb-3">
      <h4 class="text-center text-white mb-4">{companyData.name || 'Printos'}</h4>
      <ul class="flex flex-col mb-auto">
        <h6 class="px-3 mt-2 mb-3 text-[#adb5bd] uppercase text-[0.75rem] tracking-[0.5px] font-semibold">
          Financial Module
        </h6>
        <For each={navItems}>
          {(item) => (
            <li class="mb-[5px]">
              <Link
                to={item.to}
                class={linkClass}
                activeProps={{
                  style: { color: 'white', 'background-color': '#0d6efd' },
                }}
              >
                {item.label}
              </Link>
            </li>
          )}
        </For>
        <li class="mt-3 border-t border-[#adb5bd]/20 pt-3">
          <Link
            to="/company"
            class={linkClass}
            activeProps={{
              style: { color: 'white', 'background-color': '#0d6efd' },
            }}
          >
            Company Details
          </Link>
        </li>
      </ul>
    </div>
  )
}
