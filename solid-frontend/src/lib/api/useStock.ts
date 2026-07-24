import { createMutation, createQuery, useQueryClient } from '@tanstack/solid-query'
import { getStock, createStock, updateStock, deleteStock } from './stock-fns'
import type { components } from './schema'

type ProductCreate = components['schemas']['ProductCreate']
type ProductUpdate = components['schemas']['ProductUpdate']

export const STOCK_QUERY_KEY = ['stock'] as const

export function useStock() {
  return createQuery(() => ({
    queryKey: STOCK_QUERY_KEY,
    queryFn: () => getStock(),
  }))
}

export function useCreateStock() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: async (body: ProductCreate) => {
      const res = await createStock({ data: body })
      return res
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: STOCK_QUERY_KEY })
    },
  }))
}

export function useUpdateStock() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: async (input: ProductUpdate & { product_id: string }) => {
      const res = await updateStock({ data: input })
      return res
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: STOCK_QUERY_KEY })
    },
  }))
}

export function useDeleteStock() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: async (product_id: string) => {
      await deleteStock({ data: { product_id } })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: STOCK_QUERY_KEY })
    },
  }))
}
