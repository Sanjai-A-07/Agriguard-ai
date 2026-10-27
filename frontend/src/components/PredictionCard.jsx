import { CheckCircle2, HelpCircle, ImageOff } from 'lucide-react'
import ConfidenceIndicator from './ConfidenceIndicator.jsx'

const VIEW = {
  confident: { Icon: CheckCircle2, label: 'Likely match', tone: 'text-leaf-600' },
  uncertain: { Icon: HelpCircle, label: 'Uncertain', tone: 'text-amber-700' },
  poor_image: { Icon: ImageOff, label: 'Photo quality too low', tone: 'text-amber-700' },
}

export default function PredictionCard({ result, imageUrl }) {
  const { Icon, label, tone } = VIEW[result.status]
  const title = result.status === 'confident' ? result.guidance?.disease_name : 'Unable to identify reliably'
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-4 sm:flex-row">
        <img src={imageUrl} alt="The leaf photo you uploaded" className="h-48 w-full rounded-xl object-cover sm:w-48" />
        <div className="flex-1 space-y-3">
          <p className={`flex items-center gap-2 text-sm font-semibold ${tone}`}>
            <Icon className="h-5 w-5" aria-hidden="true" /> {label}
          </p>
          <h2 className="text-2xl font-bold text-forest-900">{title}</h2>
          <p className="text-sm">{result.message}</p>
          <ConfidenceIndicator value={result.confidence} status={result.status} />
          {result.image_quality.warnings.length > 0 && (
            <p className="text-sm text-amber-800">Photo issues noticed: {result.image_quality.warnings.map((w) => w.replace('_', ' ')).join(', ')}.</p>
          )}
        </div>
      </div>
      {result.status !== 'confident' && (
        <p className="mt-4 text-sm">Please upload a clearer image or consult an agricultural expert.</p>
      )}
    </div>
  )
}
