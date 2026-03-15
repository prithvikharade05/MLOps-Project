/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      animation: {
        'glow': 'glow 1s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px #00ffff60, 0 0 10px #00ffff60, 0 0 15px #00ffff60' },
          '100%': { boxShadow: '0 0 20px #00ffff80, 0 0 30px #00ffff80, 0 0 40px #00ffff80' },
        }
      }
    },
  },
  plugins: [require("tailwindcss-animate")],
}

