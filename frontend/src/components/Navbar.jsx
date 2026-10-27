import { Link, NavLink } from 'react-router-dom'
import { Leaf } from 'lucide-react'

export default function Navbar() {
  const link = ({ isActive }) =>
    `rounded px-3 py-2 text-sm font-medium ${isActive ? 'bg-leaf-100 text-forest-900' : 'text-forest-800 hover:bg-cream-100'}`
  return (
    <header className="border-b border-cream-100 bg-white">
      <nav className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3" aria-label="Main">
        <Link to="/" className="flex items-center gap-2 text-lg font-bold text-forest-900">
          <Leaf className="h-6 w-6 text-leaf-500" aria-hidden="true" /> AgriGuard AI
        </Link>
        <div className="flex gap-1">
          <NavLink to="/" end className={link}>Home</NavLink>
          <NavLink to="/detect" className={link}>Detect</NavLink>
        </div>
      </nav>
    </header>
  )
}
