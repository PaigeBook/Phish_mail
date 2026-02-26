"use client";

import { useMemo, useState } from "react";

import Card from "../../shared/components/Card";
import ResultCard from "../../shared/components/ResultCard";
import HighlightText from "../../shared/components/HighlightText";
import { useAnalyzeEmail } from "../../shared/hooks/useAnalyzeEmail";
import { PredictResponse } from "../../shared/lib/schema";

export default function DetectorPage() {
  const [body, setBody] = useState("");
  const [headers, setHeaders] = useState("");
  const [history, setHistory] = useState<PredictResponse[]>([]);

  const mutation = useAnalyzeEmail();

  const suspiciousTerms = useMemo(
    () => mutation.data?.explanation.suspicious_terms ?? [],
    [mutation.data]
  );

  const handleSubmit = async () => {
    const result = await mutation.mutateAsync({ body, headers: headers || null });
    setHistory((prev) => [result, ...prev].slice(0, 5));
  };

  return (
    <main className="mx-auto max-w-6xl space-y-6 px-6 py-10">
      <header className="float-in flex flex-col gap-3">
        <p className="text-xs uppercase tracking-[0.3em] text-coral font-bold">🐠 Safe Harbor</p>
        <h1 className="text-4xl font-semibold text-ocean">
          Phishing Email Detector
        </h1>
        <p className="max-w-2xl text-base text-ocean/70">
          Keep your inbox safe from phishing nets! Analyze incoming messages, spot suspicious signals, and swim safely with our ML-powered guardian.
        </p>
      </header>

      <section className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
        <Card className="space-y-4">
          <div>
            <p className="text-xs uppercase tracking-wide text-mint/70 font-semibold">📧 Headers (Optional)</p>
            <textarea
              value={headers}
              onChange={(event) => setHeaders(event.target.value)}
              className="mt-2 h-24 w-full rounded-xl border-2 border-mint/30 bg-gradient-to-br from-blue-50 to-cyan-50 p-3 text-sm text-ink placeholder-mint/50 focus:border-mint focus:outline-none transition"
              placeholder="Optional raw headers"
            />
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-mint/70 font-semibold">💬 Email body</p>
            <textarea
              value={body}
              onChange={(event) => setBody(event.target.value)}
              className="mt-2 h-48 w-full rounded-xl border-2 border-mint/30 bg-gradient-to-br from-blue-50 to-cyan-50 p-3 text-sm text-ink placeholder-mint/50 focus:border-mint focus:outline-none transition"
              placeholder="Paste the email content here"
            />
          </div>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={mutation.isPending || !body.trim()}
            className="w-full rounded-xl bg-gradient-to-r from-ocean to-mint px-5 py-3 text-sm font-semibold text-white transition hover:from-ocean/90 hover:to-mint/90 disabled:cursor-not-allowed disabled:opacity-50 shadow-md hover:shadow-lg"
          >
            {mutation.isPending ? "🐟 Analyzing..." : "🔍 Analyze Email"}
          </button>
          {mutation.isError && (
            <p className="text-sm text-coral">Prediction failed. Try again.</p>
          )}
        </Card>

        <ResultCard result={mutation.data ?? null} />
      </section>

      <section className="grid gap-6 lg:grid-cols-[1fr_1fr]">
        <Card>
          <p className="text-xs uppercase tracking-wide text-mint/70 font-semibold">
            🔎 Suspicious Signals
          </p>
          <div className="mt-3 rounded-xl bg-gradient-to-br from-blue-50 to-cyan-50 p-4 text-sm leading-6">
            <HighlightText text={body || "No email loaded."} highlights={suspiciousTerms} />
          </div>
        </Card>

        <Card>
          <p className="text-xs uppercase tracking-wide text-mint/70 font-semibold">📚 Your Journey</p>
          <div className="mt-4 space-y-3 text-sm">
            {history.length ? (
              history.map((item, idx) => (
                <div
                  key={`${item.prediction}-${idx}`}
                  className={`rounded-xl border-2 p-3 transition ${
                    item.prediction === "phishing"
                      ? "border-coral/40 bg-gradient-to-r from-coral/5 to-orange-50"
                      : "border-mint/40 bg-gradient-to-r from-mint/5 to-cyan-50"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className={`font-semibold capitalize ${item.prediction === "phishing" ? "text-coral" : "text-mint"}`}>
                      {item.prediction === "phishing" ? "🚨 Phishing" : "✅ Safe"}
                    </span>
                    <span className="text-ink/60 font-semibold">
                      {(item.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <p className="text-xs text-ink/60 mt-1">{item.risk_level} risk</p>
                </div>
              ))
            ) : (
              <p className="text-mint/60">No history yet. Start analyzing! 🐠</p>
            )}
          </div>
        </Card>
      </section>
    </main>
  );
}
