import clsx from "clsx";

const styles: Record<string, { bg: string; text: string; emoji: string }> = {
  Low: { bg: "bg-mint/10 border-mint/50", text: "text-mint", emoji: "🟢" },
  Medium: { bg: "bg-amber/10 border-amber/50", text: "text-amber", emoji: "🟡" },
  High: { bg: "bg-coral/10 border-coral/50", text: "text-coral", emoji: "🔴" }
};

export default function Badge({ level }: { level: "Low" | "Medium" | "High" }) {
  const style = styles[level];
  return (
    <span
      className={clsx(
        "rounded-full border-2 px-3 py-1 text-xs font-semibold uppercase tracking-wide flex items-center gap-2",
        style.bg,
        style.text
      )}
    >
      <span>{style.emoji}</span>
      {level} risk
    </span>
  );
}
