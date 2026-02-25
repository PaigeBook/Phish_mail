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
          <mark key={idx} className="rounded bg-alert/15 px-1 text-alert">
            {part}
          </mark>
        );
      })}
    </span>
  );
}
