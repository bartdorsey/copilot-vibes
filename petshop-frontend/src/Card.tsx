import { ReactNode } from "react";

interface CardProps {
  expanded: boolean;
  onToggle: () => void;
  header: ReactNode;
  children: ReactNode;
  className?: string;
  indicatorColor?: string;
  ringColor?: string;
}

export function Card({
  expanded,
  onToggle,
  header,
  children,
  className = "",
  indicatorColor = "text-green-700",
  ringColor = "ring-green-400",
}: CardProps) {
  return (
    <article
      className={`bg-mocha-surface-light rounded-lg shadow p-5 flex flex-col gap-2 border border-gray-100 hover:shadow-lg transition-shadow cursor-pointer relative overflow-hidden group ${
        expanded ? ringColor : ""
      } ${className}`}
      onClick={onToggle}
      aria-expanded={expanded}
      tabIndex={0}
      role="button"
    >
      <div
        className={`absolute top-3 right-3 flex items-center gap-1 ${indicatorColor} text-xs font-semibold transition-opacity group-hover:opacity-100 opacity-80 pointer-events-none select-none z-10 bg-opacity-80 px-2 py-1 rounded shadow-sm`}
        aria-label={expanded ? "Hide details" : "Show details"}
        title={expanded ? "Hide details" : "Show details"}
      >
        <span className="inline-block w-4 h-4">
          {expanded ? (
            <svg viewBox="0 0 20 20" fill="currentColor">
              <circle
                cx="10"
                cy="10"
                r="9"
                stroke="currentColor"
                strokeWidth="2"
                fill={
                  indicatorColor === "text-green-700" ? "#059669" : "#89b4fa"
                }
              />
              <text x="10" y="15" textAnchor="middle" fontSize="12" fill="#fff">
                i
              </text>
            </svg>
          ) : (
            <svg
              viewBox="0 0 20 20"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <circle cx="10" cy="10" r="9" />
              <text
                x="10"
                y="15"
                textAnchor="middle"
                fontSize="12"
                fill={
                  indicatorColor === "text-green-700" ? "#059669" : "#89b4fa"
                }
              >
                i
              </text>
            </svg>
          )}
        </span>
        <span>{expanded ? "Hide details" : "Show details"}</span>
      </div>
      <div style={{ height: 28 }} />
      {header}
      {children}
    </article>
  );
}
