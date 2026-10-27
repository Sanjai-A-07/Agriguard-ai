export default function LoadingSpinner({ label = 'Loading…' }) {
  return (
    <div role="status" className="flex items-center gap-3 text-forest-800">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-leaf-500 border-t-transparent" />
      <span>{label}</span>
    </div>
  )
}
