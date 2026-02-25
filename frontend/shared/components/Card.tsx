import type { ReactNode } from "react";

export default function Card({
  children,
  className = ""
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={`rounded-2xl bg-white/90 p-6 shadow-lift ${className}`}>
      {children}
    </div>
  );
}
