/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: "#0f172a",
          primary: "#3b82f6",
          accent: "#6366f1",
        },
        health: {
          green: "#22c55e",
          yellow: "#eab308",
          red: "#ef4444",
        }
      }
    },
  },
  plugins: [],
}
