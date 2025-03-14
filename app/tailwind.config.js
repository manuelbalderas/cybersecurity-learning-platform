/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui'),
  ],
  daisyui: {
    themes: ["lofi", "dark", "cupcake", "retro"],
  },
}

