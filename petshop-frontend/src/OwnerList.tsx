import type { Owner } from "./schemas";
import { useEffect, useState } from "react";
import { fetchOwners } from "./api";
import { Card } from "./Card";

export function OwnerList() {
  const [owners, setOwners] = useState<Owner[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedOwnerId, setExpandedOwnerId] = useState<number | null>(null);

  useEffect(() => {
    fetchOwners()
      .then(setOwners)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading owners...</div>;
  if (error) return <div className="text-red-600">Error: {error}</div>;

  return (
    <main
      className="w-full flex flex-col items-center"
      style={{ background: "var(--ctp-mocha-base)", minHeight: "100vh" }}
    >
      <h2 className="text-[1.2rem] font-semibold mb-4">Owners</h2>
      <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 w-full max-w-3xl">
        {owners.map((owner) => {
          const expanded = expandedOwnerId === owner.id;
          return (
            <Card
              key={owner.id}
              expanded={expanded}
              onToggle={() => setExpandedOwnerId(expanded ? null : owner.id)}
              header={
                <>
                  <header className="flex items-center gap-2 mb-1">
                    <span className="text-lg font-bold text-green-700">
                      {owner.name}
                    </span>
                    <span className="text-xs text-gray-500">#{owner.id}</span>
                  </header>
                  {owner.email && (
                    <div className="text-gray-700 text-base">
                      <span className="font-medium">Email:</span> {owner.email}
                    </div>
                  )}
                  {owner.phone && (
                    <div className="text-gray-700 text-base">
                      <span className="font-medium">Phone:</span> {owner.phone}
                    </div>
                  )}
                </>
              }
              className={expanded ? "ring-2 ring-green-400" : ""}
              indicatorColor="text-green-700"
              ringColor="ring-2 ring-green-400"
            >
              {expanded && (
                <section
                  className="mt-2 text-sm text-gray-700 space-y-1 animate-expand"
                  style={{
                    animation: "expandFadeIn 0.3s cubic-bezier(.4,2,.6,1)",
                  }}
                  aria-label="Owner details"
                >
                  {owner.address && (
                    <div>
                      <span className="font-medium">Address:</span>{" "}
                      {owner.address}
                    </div>
                  )}
                  {owner.city && (
                    <div>
                      <span className="font-medium">City:</span> {owner.city}
                    </div>
                  )}
                  {owner.state && (
                    <div>
                      <span className="font-medium">State:</span> {owner.state}
                    </div>
                  )}
                  {owner.zip_code && (
                    <div>
                      <span className="font-medium">ZIP Code:</span>{" "}
                      {owner.zip_code}
                    </div>
                  )}
                  {owner.country && (
                    <div>
                      <span className="font-medium">Country:</span>{" "}
                      {owner.country}
                    </div>
                  )}
                  {owner.date_of_birth && (
                    <div>
                      <span className="font-medium">Date of Birth:</span>{" "}
                      {owner.date_of_birth}
                    </div>
                  )}
                </section>
              )}
            </Card>
          );
        })}
      </section>
    </main>
  );
}
