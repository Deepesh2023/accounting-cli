import {
  HeadContent,
  Outlet,
  Scripts,
  createRootRouteWithContext,
} from '@tanstack/solid-router'

import { TanStackRouterDevtools } from '@tanstack/solid-router-devtools'

import { QueryClientProvider } from '@tanstack/solid-query'
import { HydrationScript } from 'solid-js/web'
import { Suspense } from 'solid-js'

import Sidebar from '../components/Sidebar'
import { queryClient } from '../integrations/tanstack-query/provider'

import styleCss from '../styles.css?url'

export const Route = createRootRouteWithContext()({
  head: () => ({
    links: [{ rel: 'stylesheet', href: styleCss }],
  }),
  shellComponent: RootComponent,
})

function RootComponent() {
  return (
    <html>
      <head>
        <HydrationScript />
        <HeadContent />
      </head>
      <body>
        <QueryClientProvider client={queryClient}>
          <div class="flex min-h-screen bg-[#f8f9fa]">
            <Sidebar />
            <main class="flex-1 overflow-y-auto p-8">
              <Suspense>
                <Outlet />
              </Suspense>
            </main>
          </div>
          <TanStackRouterDevtools />
        </QueryClientProvider>
        <Scripts />
      </body>
    </html>
  )
}
