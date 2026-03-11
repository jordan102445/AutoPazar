module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/*.py"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Manrope", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      boxShadow: {
        soft: "0 18px 48px rgba(15, 23, 42, 0.08)"
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms")
  ]
};

