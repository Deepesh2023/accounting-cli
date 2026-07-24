import { QueryClient } from '@tanstack/solid-query'
import { createContext, useContext } from 'solid-js'

export const queryClient = new QueryClient()

export function getContext() {
  return { queryClient }
}

const QueryClientContext = createContext<QueryClient>(queryClient)

export function useQueryClient() {
  return useContext(QueryClientContext)
}
