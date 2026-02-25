import { vi } from "vitest";

import { analyzeEmail } from "../shared/lib/api";

const mockResponse = {
  prediction: "phishing",
  confidence: 0.92,
  risk_level: "High",
  explanation: {
    reasons: ["Suspicious keywords detected"],
    top_features: [],
    suspicious_terms: ["urgent"],
    stats: { phishing_score: 0.92 }
  }
};

test("analyzeEmail posts and parses response", async () => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => mockResponse
  }) as unknown as typeof fetch;

  const result = await analyzeEmail({ body: "urgent update", headers: null });
  expect(result.prediction).toBe("phishing");
});
