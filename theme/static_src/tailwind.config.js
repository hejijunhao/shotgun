module.exports = {
    content: [
      '../../Reservations/templates/**/*.html',
      '../../Reservations/**/*.py',
      '../templates/**/*.html',
      '../../templates/**/*.html',
      './src/**/*.js',
      '../../node_modules/flowbite/**/*.js'
    ],
    theme: {
      extend: {},
    },
    plugins: [
        require('flowbite/plugin'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
  }