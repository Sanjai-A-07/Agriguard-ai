import { Info } from 'lucide-react'

export default function DisclaimerBanner({ children }) {
  return (
    <div role="note" className="flex gap-3 rounded-xl border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
      <Info className="mt-0.5 h-5 w-5 shrink-0" aria-hidden="true" />
      <p>{children || 'AgriGuard AI gives a preliminary, image-based result. It is not a diagnosis and does not replace an agricultural expert.'}</p>
    </div>
  )
}
