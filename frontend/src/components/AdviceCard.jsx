function Section({ title, items }) {
  if (!items?.length) return null
  return (
    <section className="mt-4">
      <h3 className="font-semibold text-forest-900">{title}</h3>
      <ul className="mt-1 list-disc space-y-1 pl-5 text-sm">{items.map((t) => <li key={t}>{t}</li>)}</ul>
    </section>
  )
}

export default function AdviceCard({ guidance }) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      <h2 className="text-lg font-bold text-forest-900">About: {guidance.disease_name}</h2>
      <Section title="Symptoms to look for" items={guidance.symptoms} />
      <Section title="Prevention" items={guidance.prevention} />
      <Section title="General management" items={guidance.management_guidance} />
      <Section title="Safe next steps" items={guidance.next_steps} />
      {guidance.review_status !== 'reviewed' && (
        <p className="mt-4 rounded-lg bg-amber-50 p-3 text-xs text-amber-900">
          This guidance is a draft and has not yet been verified by an agricultural expert.
        </p>
      )}
      <p className="mt-3 text-xs text-gray-500">Sources: {guidance.sources.join('; ')}</p>
    </div>
  )
}
