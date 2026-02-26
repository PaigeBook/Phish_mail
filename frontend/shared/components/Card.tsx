import type { ReactNode } from "react";

export default function Card({
  children,
  className = ""
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={`rounded-2xl bg-gradient-to-br from-white via-blue-50/50 to-cyan-50/30 backdrop-blur-sm border border-mint/10 p-6 shadow-lg ${className}`}>
      {children}
    </div>
  );
}
