// /** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        nunito: ['"Nunito"', 'sans-serif'],
        montserrat: ['"Montserrat"', 'sans-serif'],
        winky: ['"Winky Sans"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}