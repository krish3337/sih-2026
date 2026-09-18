export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        government: {
          blue: '#1a365d',
          lightBlue: '#2b6cb0',
          bg: '#f7fafc',
          border: '#e2e8f0',
          text: '#2d3748',
        }
      }
    },
  },
  plugins: [],
}
