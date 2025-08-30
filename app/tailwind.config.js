/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**"],
  theme: {
    extend: {
      extend: {
        animation: {
          'fade-out': 'fadeOut 10s ease-out forwards',
        },
        keyframes: {
          fadeOut: {
            '0%': {
              opacity: '1',
              transform: 'translateY(0)',
            },
            '100%': {
              opacity: '0',
              transform: 'translateY(-10px)',
            },
          },
        },
      },
      fontFamily: {
        'Roboto': ['Roboto'],
        'RobotoMono': ['Roboto Mono']
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui'),
    require('@tailwindcss/line-clamp'),

  ],
  daisyui: {
    themes: ["lofi", "dark", "cupcake", "retro", "dracula"],
  },
}

