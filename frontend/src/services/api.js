import axios from 'axios'

const client = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000' })

// Turn any failure into an Error whose message the UI can show directly.
function toError(err) {
  const detail = err.response?.data?.detail
  if (typeof detail === 'string') return new Error(detail)
  if (err.code === 'ERR_NETWORK') {
    return new Error('Cannot reach the AgriGuard server. Check your connection and that the backend is running.')
  }
  return new Error('Something went wrong. Please try again.')
}

export async function predict(file, crop = 'tomato', onProgress) {
  const form = new FormData()
  form.append('image', file)
  form.append('crop', crop)
  try {
    const { data } = await client.post('/api/predict', form, {
      onUploadProgress: (e) => e.total && onProgress?.(Math.round((e.loaded / e.total) * 100)),
    })
    return data
  } catch (e) {
    throw toError(e)
  }
}

export async function getCrops() {
  try { return (await client.get('/api/crops')).data } catch (e) { throw toError(e) }
}
export async function getHealth() {
  try { return (await client.get('/health')).data } catch (e) { throw toError(e) }
}
