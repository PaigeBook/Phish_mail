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
        <p className="text-xs uppercase tracking-[0.3em] text-alert">Threat Lens</p>
        <h1 className="text-4xl font-semibold text-ink">
          Phishing Email Detector
        </h1>
        <p className="max-w-2xl text-base text-ink/70">
          Analyze incoming messages, assess risk, and surface suspicious signals
          with a production-ready ML pipeline.
        </p>
      </header>

      <section className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
        <Card className="space-y-4">
          <div>
            <p className="text-xs uppercase tracking-wide text-ink/50">Headers</p>
            <textarea
              value={headers}
              onChange={(event) => setHeaders(event.target.value)}
              className="mt-2 h-24 w-full rounded-xl border border-ash/60 bg-white/80 p-3 text-sm"
              placeholder="Optional raw headers"
            />
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-ink/50">Email body</p>
            <textarea
              value={body}
              onChange={(event) => setBody(event.target.value)}
              className="mt-2 h-48 w-full rounded-xl border border-ash/60 bg-white/80 p-3 text-sm"
              placeholder="Paste the email content here"
            />
          </div>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={mutation.isPending || !body.trim()}
            className="rounded-xl bg-ink px-5 py-3 text-sm font-semibold text-white transition hover:bg-ink/90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {mutation.isPending ? "Analyzing..." : "Analyze Email"}
          </button>
          {mutation.isError && (
            <p className="text-sm text-alert">Prediction failed. Try again.</p>
          )}
        </Card>

        <ResultCard result={mutation.data ?? null} />
      </section>

      <section className="grid gap-6 lg:grid-cols-[1fr_1fr]">
        <Card>
          <p className="text-xs uppercase tracking-wide text-ink/50">
            Highlighted analysis
          </p>
          <div className="mt-3 rounded-xl bg-white/80 p-4 text-sm leading-6">
            <HighlightText text={body || "No email loaded."} highlights={suspiciousTerms} />
          </div>
        </Card>

        <Card>
          <p className="text-xs uppercase tracking-wide text-ink/50">History</p>
          <div className="mt-4 space-y-3 text-sm">
            {history.length ? (
              history.map((item, idx) => (
                <div
                  key={`${item.prediction}-${idx}`}
                  className="rounded-xl border border-ash/50 bg-white/70 p-3"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold capitalize">
                      {item.prediction}
                    </span>
                    <span className="text-ink/60">
                      {(item.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <p className="text-xs text-ink/60">{item.risk_level} risk</p>
                </div>
              ))
            ) : (
              <p className="text-ink/60">No history yet.</p>
            )}
          </div>
        </Card>
      </section>
    </main>
  );
}
