/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/index.html",          // public 디렉토리의 index.html
    "./src/**/*.{vue,js,ts,jsx,tsx}" // src 내부의 모든 Vue 및 JS/TS 파일
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};