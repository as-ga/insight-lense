/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        slate: {
          750: "#1d293d",
        },
        purple: {
          950: "#2d1b4e",
        },
      },
      animation: {
        "slide-in-down": "slideInDown 0.5s ease-out",
        "fade-in": "fadeIn 0.3s ease-out",
        glow: "glow 2s ease-in-out infinite",
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      backdropBlur: {
        xs: "2px",
      },
      boxShadow: {
        glow: "0 0 20px rgba(139, 92, 246, 0.3)",
        "glow-lg": "0 0 30px rgba(139, 92, 246, 0.4)",
      },
    },
  },
  plugins: [],
  darkMode: "class",
};
