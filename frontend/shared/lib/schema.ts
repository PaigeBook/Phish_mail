import { z } from "zod";

export const predictRequestSchema = z.object({
  body: z.string().min(1),
  headers: z.string().optional().nullable()
});

export const featureContributionSchema = z.object({
  feature: z.string(),
  contribution: z.number()
});

export const explanationSchema = z.object({
  reasons: z.array(z.string()),
  top_features: z.array(featureContributionSchema),
  suspicious_terms: z.array(z.string()),
  stats: z.record(z.any())
});

export const predictResponseSchema = z.object({
  prediction: z.enum(["phishing", "legitimate"]),
  confidence: z.number(),
  risk_level: z.enum(["Low", "Medium", "High"]),
  explanation: explanationSchema
});

export type PredictRequest = z.infer<typeof predictRequestSchema>;
export type PredictResponse = z.infer<typeof predictResponseSchema>;
