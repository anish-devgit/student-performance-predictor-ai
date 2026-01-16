'use client'

import { useTheme } from 'next-themes'
import { useEffect, useState } from 'react'

export default function ThemeToggle() {
  const [mounted, setMounted] = useState(false)
  const { theme, setTheme } = useTheme()

  useEffect(() => {
    setMounted(true)
  }, [])

  const handleToggle = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark'
    console.log('Switching theme to:', newTheme)
    setTheme(newTheme)
  }

  if (!mounted) return null

  return (
    <button
      onClick={handleToggle}
      className="fixed top-6 right-6 z-50 p-3 bg-gray-200 dark:bg-gray-700 rounded-lg text-lg font-bold hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      aria-label="Toggle theme"
    >
      {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
    </button>
  )
}
