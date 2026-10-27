export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        forest: { 900: '#14392a', 800: '#1b4d38', 700: '#23633f' },
        leaf: { 500: '#4c9a2a', 600: '#3f8222', 100: '#e4f1d8' },
        cream: { 50: '#fbf8ef', 100: '#f5efdc' },
      },
      fontFamily: { sans: ['Inter', 'Noto Sans Tamil', 'system-ui', 'sans-serif'] },
    },
  },
  plugins: [],
}
