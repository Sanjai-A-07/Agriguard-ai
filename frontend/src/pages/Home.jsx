import { Link } from 'react-router-dom'
import { Camera, Cpu, BookOpenCheck } from 'lucide-react'
import DisclaimerBanner from '../components/DisclaimerBanner.jsx'

const steps = [
  { Icon: Camera, title: 'Photograph a leaf', text: 'Take a clear, well-lit photo of a single tomato leaf.' },
  { Icon: Cpu, title: 'AI checks it', text: 'A trained model compares it with five supported tomato leaf categories.' },
  { Icon: BookOpenCheck, title: 'Read safe guidance', text: 'See symptoms, prevention and next steps, plus when to ask an expert.' },
]

export default function Home() {
  return (
    <div className="space-y-12">
      <section className="rounded-3xl bg-forest-900 px-6 py-12 text-center text-white">
        <h1 className="text-4xl font-bold">Smarter Crop Care. Stronger Farming.</h1>
        <p className="mx-auto mt-4 max-w-2xl text-cream-100">
          Crop diseases are costly when they are noticed late, and expert advice is not always nearby.
          AgriGuard AI gives a quick, first-look check of tomato leaf photos.
        </p>
        <Link to="/detect" className="mt-6 inline-block rounded-lg bg-leaf-500 px-6 py-3 font-semibold text-white hover:bg-leaf-600">
          Detect Crop Disease
        </Link>
      </section>

      <section aria-labelledby="how">
        <h2 id="how" className="text-2xl font-bold text-forest-900">How it works</h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-3">
          {steps.map(({ Icon, title, text }) => (
            <div key={title} className="rounded-2xl bg-white p-5 shadow-sm">
              <Icon className="h-7 w-7 text-leaf-500" aria-hidden="true" />
              <h3 className="mt-3 font-semibold text-forest-900">{title}</h3>
              <p className="mt-1 text-sm text-gray-600">{text}</p>
            </div>
          ))}
        </div>
      </section>

      <section aria-labelledby="crops">
        <h2 id="crops" className="text-2xl font-bold text-forest-900">Supported crops</h2>
        <p className="mt-2 text-sm text-gray-600">
          Tomato: healthy, early blight, late blight, bacterial spot, leaf mould. More crops are planned; other crops and diseases are not supported.
        </p>
      </section>

      <DisclaimerBanner />
    </div>
  )
}
