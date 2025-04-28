/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**"],
  theme: {
    extend: {
      fontFamily: {
        'Roboto': ['Roboto'],
        'RobotoMono': ['Roboto Mono']
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui'),
  ],
  daisyui: {
    themes: ["lofi", "dark", "cupcake", "retro", "dracula"],
  },
}

