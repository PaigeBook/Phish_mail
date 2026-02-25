import { predictRequestSchema, predictResponseSchema } from "./schema";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function analyzeEmail(payload: unknown) {
  const parsed = predictRequestSchema.parse(payload);
  const response = await fetch(`${API_BASE}/api/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(parsed)
  });

  if (!response.ok) {
    throw new Error("Prediction failed");
  }

  const json = await response.json();
  return predictResponseSchema.parse(json);
}
