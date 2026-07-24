import { createServerFn } from '@tanstack/solid-start'
import type { components } from './schema'

type SaleResponse = components['schemas']['SaleResponse']
type SaleCreate = components['schemas']['SaleCreate']

const API_BASE = process.env.API_URL ?? 'http://localhost:8000'

export const listSales = createServerFn({ method: 'GET' })
  .handler(async () => {
    const res = await fetch(`${API_BASE}/api/sales`)
    if (!res.ok) throw new Error(`Failed to fetch sales: ${res.status}`)
    return res.json() as Promise<SaleResponse[]>
  })

export const getSale = createServerFn({ method: 'GET' })
  .validator((d: { sale_id: string }) => d)
  .handler(async ({ data }) => {
    const res = await fetch(`${API_BASE}/api/sales/${data.sale_id}`)
    if (!res.ok) throw new Error(`Failed to fetch sale: ${res.status}`)
    return res.json() as Promise<SaleResponse>
  })

export const createSale = createServerFn({ method: 'POST' })
  .validator((d: SaleCreate) => d)
  .handler(async ({ data }) => {
    const res = await fetch(`${API_BASE}/api/sales`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!res.ok) throw new Error(`Failed to create sale: ${res.status}`)
    return res.json() as Promise<SaleResponse>
  })

export const updateSale = createServerFn({ method: 'POST' })
  .validator((d: SaleCreate & { sale_id: string }) => d)
  .handler(async ({ data }) => {
    const { sale_id, ...body } = data
    const res = await fetch(`${API_BASE}/api/sales/${sale_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!res.ok) throw new Error(`Failed to update sale: ${res.status}`)
    return res.json() as Promise<SaleResponse>
  })

export const deleteSale = createServerFn({ method: 'POST' })
  .validator((d: { sale_id: string }) => d)
  .handler(async ({ data }) => {
    const res = await fetch(`${API_BASE}/api/sales/${data.sale_id}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error(`Failed to delete sale: ${res.status}`)
  })
