import clsx from "clsx";

const styles: Record<string, string> = {
  Low: "bg-mint/10 text-mint border-mint/30",
  Medium: "bg-amber/10 text-amber border-amber/30",
  High: "bg-alert/10 text-alert border-alert/30"
};

export default function Badge({ level }: { level: "Low" | "Medium" | "High" }) {
  return (
    <span
      className={clsx(
        "rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide",
        styles[level]
      )}
    >
      {level} risk
    </span>
  );
}
