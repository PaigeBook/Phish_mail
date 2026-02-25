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
        <p className="text-sm text-ink/60">
          Run an analysis to see results.
        </p>
      </Card>
    );
  }

  return (
    <Card className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-ink/50">
            Prediction
          </p>
          <h3 className="text-2xl font-semibold capitalize text-ink">
            {result.prediction}
          </h3>
        </div>
        <Badge level={result.risk_level} />
      </div>

      <ConfidenceGauge value={result.confidence} />

      <div>
        <p className="text-xs uppercase tracking-wide text-ink/50">Reasons</p>
        <ul className="mt-2 space-y-1 text-sm">
          {result.explanation.reasons.map((reason) => (
            <li key={reason}>- {reason}</li>
          ))}
        </ul>
      </div>

      <div>
        <p className="text-xs uppercase tracking-wide text-ink/50">
          Suspicious terms
        </p>
        <p className="mt-2 rounded-xl bg-ash/30 p-3 text-sm">
          <HighlightText
            text={result.explanation.suspicious_terms.join(", ") || "None"}
            highlights={result.explanation.suspicious_terms}
          />
        </p>
      </div>

      <div>
        <p className="text-xs uppercase tracking-wide text-ink/50">
          Top features
        </p>
        <div className="mt-2 space-y-1 text-sm">
          {result.explanation.top_features.length ? (
            result.explanation.top_features.map((feat) => (
              <div key={feat.feature} className="flex justify-between">
                <span>{feat.feature}</span>
                <span className="text-ink/60">
                  {feat.contribution.toFixed(3)}
                </span>
              </div>
            ))
          ) : (
            <p className="text-ink/60">Not available for this model.</p>
          )}
        </div>
      </div>
    </Card>
  );
}
