import { createServerFn } from '@tanstack/solid-start'
import type { components } from './schema'

type ProductResponse = components['schemas']['ProductResponse']
type ProductCreate = components['schemas']['ProductCreate']
type ProductUpdate = components['schemas']['ProductUpdate']

const API_BASE = process.env.API_URL ?? 'http://localhost:8000'

export const getStock = createServerFn({ method: 'GET' })
  .handler(async () => {
    const res = await fetch(`${API_BASE}/api/inventory`)
    if (!res.ok) throw new Error(`Failed to fetch stock: ${res.status}`)
    return res.json() as Promise<ProductResponse[]>
  })

export const createStock = createServerFn({ method: 'POST' })
  .validator((d: ProductCreate) => d)
  .handler(async ({ data }) => {
    const res = await fetch(`${API_BASE}/api/inventory`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!res.ok) throw new Error(`Failed to create stock: ${res.status}`)
    return res.json() as Promise<ProductResponse>
  })

export const updateStock = createServerFn({ method: 'POST' })
  .validator((d: ProductUpdate & { product_id: string }) => d)
  .handler(async ({ data }) => {
    const { product_id, ...body } = data
    const res = await fetch(`${API_BASE}/api/inventory/${product_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!res.ok) throw new Error(`Failed to update stock: ${res.status}`)
    return res.json() as Promise<ProductResponse>
  })

export const deleteStock = createServerFn({ method: 'POST' })
  .validator((d: { product_id: string }) => d)
  .handler(async ({ data }) => {
    const res = await fetch(`${API_BASE}/api/inventory/${data.product_id}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error(`Failed to delete stock: ${res.status}`)
  })
