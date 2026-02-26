export default function HighlightText({
  text,
  highlights
}: {
  text: string;
  highlights: string[];
}) {
  if (!highlights.length) {
    return <span>{text}</span>;
  }

  const escaped = highlights.map((term) =>
    term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
  );
  const pattern = new RegExp(`(${escaped.join("|")})`, "gi");
  const parts = text.split(pattern);

  return (
    <span>
      {parts.map((part, idx) => {
        const isHit = highlights.some(
          (term) => term.toLowerCase() === part.toLowerCase()
        );
        if (!isHit) {
          return <span key={idx}>{part}</span>;
        }
        return (
          <mark key={idx} className="rounded bg-gradient-to-r from-coral/25 to-orange/25 px-1.5 py-0.5 text-coral font-semibold">
            {part}
          </mark>
        );
      })}
    </span>
  );
}
