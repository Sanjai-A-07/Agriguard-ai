import { useEffect, useState } from 'react'
import { X } from 'lucide-react'
import UploadDropzone from '../components/UploadDropzone.jsx'
import PredictionCard from '../components/PredictionCard.jsx'
import AdviceCard from '../components/AdviceCard.jsx'
import DisclaimerBanner from '../components/DisclaimerBanner.jsx'
import LoadingSpinner from '../components/LoadingSpinner.jsx'
import ErrorMessage from '../components/ErrorMessage.jsx'
import { predict, getCrops } from '../services/api.js'

export default function Detect() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [crops, setCrops] = useState([{ id: 'tomato', name: 'Tomato' }])
  const [crop, setCrop] = useState('tomato')
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  useEffect(() => { getCrops().then(setCrops).catch(() => {}) }, [])
  useEffect(() => () => { if (previewUrl) URL.revokeObjectURL(previewUrl) }, [previewUrl])

  function choose(f) {
    setFile(f); setPreviewUrl(URL.createObjectURL(f)); setResult(null); setError('')
  }
  function clear() { setFile(null); setPreviewUrl(null); setResult(null); setError('') }

  async function analyse() {
    setLoading(true); setError(''); setResult(null); setProgress(0)
    try { setResult(await predict(file, crop, setProgress)) }
    catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-forest-900">Detect crop disease</h1>
      <DisclaimerBanner />

      <div>
        <label htmlFor="crop" className="block text-sm font-medium">Crop</label>
        <select id="crop" value={crop} onChange={(e) => setCrop(e.target.value)} className="mt-1 rounded-lg border border-gray-300 bg-white px-3 py-2">
          {crops.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>

      {!file ? (
        <UploadDropzone onFile={choose} onReject={setError} />
      ) : (
        <div className="rounded-2xl bg-white p-4 shadow-sm">
          <img src={previewUrl} alt="Preview of your selected leaf photo" className="mx-auto max-h-72 rounded-xl object-contain" />
          <div className="mt-4 flex flex-wrap justify-center gap-3">
            <button onClick={analyse} disabled={loading} className="rounded-lg bg-forest-800 px-5 py-2.5 font-medium text-white hover:bg-forest-900 disabled:opacity-50">
              Analyse leaf
            </button>
            <button onClick={clear} disabled={loading} className="flex items-center gap-1 rounded-lg border border-gray-300 px-4 py-2.5 hover:bg-cream-100">
              <X className="h-4 w-4" aria-hidden="true" /> Remove / replace
            </button>
          </div>
        </div>
      )}

      {loading && <LoadingSpinner label={progress < 100 ? `Uploading… ${progress}%` : 'Analysing your leaf…'} />}
      <ErrorMessage message={error} />

      {result && (
        <div className="space-y-4" aria-live="polite">
          <PredictionCard result={result} imageUrl={previewUrl} />
          {result.guidance && <AdviceCard guidance={result.guidance} />}
          <DisclaimerBanner>{result.disclaimer}</DisclaimerBanner>
        </div>
      )}
    </div>
  )
}
