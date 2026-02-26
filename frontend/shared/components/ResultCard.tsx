import Badge from "./Badge";
import Card from "./Card";
import ConfidenceGauge from "./ConfidenceGauge";
import HighlightText from "./HighlightText";
import { PredictResponse } from "../lib/schema";

export default function ResultCard({
  result
}: {
  result: PredictResponse | null;
}) {
  if (!result) {
    return (
      <Card>
        <div className="flex flex-col items-center justify-center py-8 text-center">
          <p className="text-3xl mb-3">🐠</p>
          <p className="text-sm text-mint/60">
            Run an analysis to see results.
          </p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-mint/70 font-semibold">
            🎯 Prediction
          </p>
          <h3 className={`text-2xl font-semibold capitalize ${result.prediction === "phishing" ? "text-coral" : "text-mint"}`}>
            {result.prediction === "phishing" ? "🚨 Phishing" : "✅ Safe"}
          </h3>
        </div>
        <Badge level={result.risk_level} />
      </div>

      <ConfidenceGauge value={result.confidence} />

      <div>
        <p className="text-xs uppercase tracking-wide text-mint/70 font-semibold">⚠️ Warning Signs</p>
        <ul className="mt-2 space-y-1 text-sm text-ink/80">
          {result.explanation.reasons.map((reason) => (
            <li key={reason}>• {reason}</li>
          ))}
        </ul>
      </div>

      <div>
        <p className="text-xs uppercase tracking-wide text-mint/70 font-semibold">
          🎣 Phishing Bait Words
        </p>
        <p className="mt-2 rounded-xl bg-gradient-to-r from-coral/10 to-amber/10 border border-coral/20 p-3 text-sm">
          <HighlightText
            text={result.explanation.suspicious_terms.join(", ") || "None detected"}
            highlights={result.explanation.suspicious_terms}
          />
        </p>
      </div>

      <div>
        <p className="text-xs uppercase tracking-wide text-mint/70 font-semibold">
          🧬 Key Indicators
        </p>
        <div className="mt-2 space-y-1 text-sm text-ink/80">
          {result.explanation.top_features.length ? (
            result.explanation.top_features.map((feat) => (
              <div key={feat.feature} className="flex justify-between items-center py-1">
                <span className="font-medium">{feat.feature}</span>
                <span className="text-mint font-semibold">
                  {feat.contribution.toFixed(3)}
                </span>
              </div>
            ))
          ) : (
            <p className="text-mint/60">Not available for this model.</p>
          )}
        </div>
      </div>
    </Card>
  );
}
