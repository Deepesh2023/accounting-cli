export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const backendBase = config.apiBase as string

  const path = getRouterParam(event, 'path') || ''
  const query = getQuery(event)
  const method = getMethod(event).toLowerCase()

  const url = new URL(`${backendBase}/api/${path}`)
  for (const [k, v] of Object.entries(query)) {
    if (v !== undefined && v !== '') url.searchParams.set(k, String(v))
  }

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }
  const authHeader = getHeader(event, 'authorization')
  if (authHeader) headers['authorization'] = authHeader

  const body = method === 'post' || method === 'put' || method === 'patch'
    ? await readBody(event)
    : undefined

  const res = await fetch(url.toString(), {
    method: getMethod(event),
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  if (res.status === 204) {
    setResponseStatus(event, 204)
    return
  }

  const text = await res.text()
  try {
    return JSON.parse(text)
  } catch {
    return text
  }
})
