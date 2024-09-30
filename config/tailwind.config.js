/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html', // Django templates folder
    '../**/templates/**/*.html',
    './node_modules/flowbite/**/*.js',
    './templates/**/*.html',  // Ensure this is the correct path to your Django templates
    './frontend/**/*.html',   // If you have any frontend templates
    './frontend/**/*.js',     // In case you're using JavaScript with Tailwind classes
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
