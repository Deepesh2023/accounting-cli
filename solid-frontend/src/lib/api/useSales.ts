import { createMutation, createQuery, useQueryClient } from '@tanstack/solid-query'
import { listSales, getSale, createSale, updateSale, deleteSale } from './sale-fns'
import type { components } from './schema'

type SaleCreate = components['schemas']['SaleCreate']

export const SALES_QUERY_KEY = ['sales'] as const

export function useSales() {
  return createQuery(() => ({
    queryKey: SALES_QUERY_KEY,
    queryFn: () => listSales(),
  }))
}

export function useSale(sale_id: string | undefined) {
  return createQuery(() => ({
    queryKey: [...SALES_QUERY_KEY, sale_id],
    queryFn: () => getSale({ data: { sale_id: sale_id! } }),
    enabled: !!sale_id,
  }))
}

export function useCreateSale() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: (body: SaleCreate) => createSale({ data: body }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SALES_QUERY_KEY })
    },
  }))
}

export function useUpdateSale() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: (input: SaleCreate & { sale_id: string }) =>
      updateSale({ data: input }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SALES_QUERY_KEY })
    },
  }))
}

export function useDeleteSale() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: (sale_id: string) => deleteSale({ data: { sale_id } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SALES_QUERY_KEY })
    },
  }))
}
