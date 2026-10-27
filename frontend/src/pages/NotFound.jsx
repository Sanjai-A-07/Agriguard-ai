import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="py-16 text-center">
      <h1 className="text-3xl font-bold text-forest-900">Page not found</h1>
      <Link to="/" className="mt-4 inline-block text-leaf-600 underline">Back to home</Link>
    </div>
  )
}
