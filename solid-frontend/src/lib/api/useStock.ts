import { createMutation, createQuery, useQueryClient } from '@tanstack/solid-query'
import { api } from './client'
import type { components } from './schema'

type ProductCreate = components['schemas']['ProductCreate']
type ProductUpdate = components['schemas']['ProductUpdate']

export const STOCK_QUERY_KEY = ['stock'] as const

export function useStock() {
  return createQuery(() => ({
    queryKey: STOCK_QUERY_KEY,
    queryFn: async () => {
      const { data, error } = await api.GET('/api/inventory')
      if (error) throw error
      return data ?? []
    },
  }))
}

export function useCreateStock() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: async (body: ProductCreate) => {
      const { data, error } = await api.POST('/api/inventory', { body })
      if (error) throw error
      return data!
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: STOCK_QUERY_KEY })
    },
  }))
}

export function useUpdateStock() {
  const queryClient = useQueryClient()
  return createMutation(() => ({
    mutationFn: async ({ product_id, ...body }: ProductUpdate & { product_id: string }) => {
      const { data, error } = await api.PUT('/api/inventory/{product_id}', {
        params: { path: { product_id } },
        body,
      })
      if (error) throw error
      return data!
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
      const { error } = await api.DELETE('/api/inventory/{product_id}', {
        params: { path: { product_id } },
      })
      if (error) throw error
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: STOCK_QUERY_KEY })
    },
  }))
}
