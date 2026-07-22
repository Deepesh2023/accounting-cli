export default defineEventHandler(async (event) => {
  const path = getRouterParam(event, 'path') || ''
  const apiBase = useRuntimeConfig().apiBase
  const target = `${apiBase}/${path}`

  const method = event.method
  const headers: Record<string, string> = {}
  if (method !== 'GET' && method !== 'HEAD') {
    headers['Content-Type'] = 'application/json'
  }

  const body = method !== 'GET' && method !== 'HEAD'
    ? await readBody(event)
    : undefined

  try {
    const res = await $fetch.raw(target, {
      method,
      body,
      headers,
    })

    setResponseStatus(event, res.status)
    return res._data
  } catch (e: any) {
    throw createError({
      statusCode: e.statusCode || 500,
      statusMessage: e.statusMessage || 'Backend error',
      data: e.data,
    })
  }
})
