import { useRef, useState } from 'react'
import { UploadCloud } from 'lucide-react'

const TYPES = ['image/jpeg', 'image/png', 'image/webp']
const MAX_MB = 5

export default function UploadDropzone({ onFile, onReject, disabled }) {
  const input = useRef(null)
  const [over, setOver] = useState(false)

  function accept(file) {
    if (!file) return
    if (!TYPES.includes(file.type)) return onReject('Please choose a JPEG, PNG or WebP image.')
    if (file.size === 0) return onReject('That file is empty.')
    if (file.size > MAX_MB * 1024 * 1024) return onReject(`Image is larger than ${MAX_MB} MB. Please choose a smaller one.`)
    onFile(file)
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setOver(true) }}
      onDragLeave={() => setOver(false)}
      onDrop={(e) => { e.preventDefault(); setOver(false); if (!disabled) accept(e.dataTransfer.files?.[0]) }}
      className={`rounded-2xl border-2 border-dashed p-8 text-center transition ${over ? 'border-leaf-500 bg-leaf-100' : 'border-gray-300 bg-white'}`}
    >
      <UploadCloud className="mx-auto h-10 w-10 text-leaf-500" aria-hidden="true" />
      <p className="mt-3 font-medium text-forest-900">Drag and drop a leaf photo here</p>
      <p className="text-sm text-gray-500">JPEG, PNG or WebP, up to {MAX_MB} MB</p>
      <input
        ref={input} id="leaf-file" type="file" accept={TYPES.join(',')} className="sr-only"
        onChange={(e) => { accept(e.target.files?.[0]); e.target.value = '' }} disabled={disabled}
      />
      <button
        type="button" disabled={disabled} onClick={() => input.current?.click()}
        className="mt-4 rounded-lg bg-forest-800 px-5 py-2.5 font-medium text-white hover:bg-forest-900 disabled:opacity-50"
      >
        Choose a photo
      </button>
    </div>
  )
}
