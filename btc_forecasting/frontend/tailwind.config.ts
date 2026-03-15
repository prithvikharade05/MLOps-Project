import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        futuristic: {
          bg: 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%)',
          neon: '#00f5ff',
          glass: 'rgba(255, 255,255, 0.1)',
          glow: 'rgba(0, 245, 255, 0.5)',
        },
      },
      keyframes: {
        "futuristic-glow": {
          "0%, 100%": { boxShadow: "0 0 5px #00f5ff, 0 0 10px #00f5ff, 0 0 15px #00f5ff" },
          "50%": { boxShadow: "0 0 20px #00f5ff, 0 0 30px #00f5ff, 0 0 40px #00f5ff" },
        },
      },
      animation: {
        "futuristic-glow": "futuristic-glow 2s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config

