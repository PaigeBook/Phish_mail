import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./features/**/*.{ts,tsx}",
    "./shared/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0b0f14",
        ash: "#e7e9ee",
        bone: "#f9fafb",
        alert: "#c2342b",
        amber: "#d9a441",
        mint: "#1f8f79"
      },
      boxShadow: {
        lift: "0 16px 50px rgba(12, 18, 28, 0.12)"
      }
    }
  },
  plugins: []
};

export default config;
