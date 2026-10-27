export default function ConfidenceIndicator({ value, status }) {
  const pct = Math.round(value * 100)
  const color = status === 'confident' ? 'bg-leaf-500' : 'bg-amber-500'
  return (
    <div>
      <div className="flex justify-between text-sm">
        <span className="font-medium">Model confidence score</span>
        <span>{pct}%</span>
      </div>
      <div className="mt-1 h-2.5 rounded-full bg-gray-200" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
        <div className={`h-2.5 rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <p className="mt-1 text-xs text-gray-500">A score, not proof that the result is correct.</p>
    </div>
  )
}
