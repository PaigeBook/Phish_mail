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
        ink: "#0d3b66",
        ash: "#e8f4f8",
        bone: "#f0f9ff",
        alert: "#ff6b6b",
        amber: "#ffa500",
        mint: "#20b2aa",
        ocean: "#0077be",
        aqua: "#00d4ff",
        coral: "#ff8566",
        sand: "#f4a460",
        seaweed: "#2d6a4f"
      },
      boxShadow: {
        lift: "0 16px 50px rgba(12, 18, 28, 0.12)"
      }
    }
  },
  plugins: []
};

export default config;
