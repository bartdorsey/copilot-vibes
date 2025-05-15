import type { Pet, Owner } from "./schemas";
import { useEffect, useState } from "react";
import { fetchPets, fetchOwners } from "./api";
import { PetArraySchema } from "./schemas";
import { Card } from "./Card";

export function PetList() {
  const [pets, setPets] = useState<Pet[]>([]);
  const [owners, setOwners] = useState<Owner[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedPetId, setExpandedPetId] = useState<number | null>(null);

  useEffect(() => {
    Promise.all([fetchPets(), fetchOwners()])
      .then(([petData, ownerData]) => {
        const parsed = PetArraySchema.safeParse(petData);
        if (!parsed.success) {
          console.error(
            "PetArraySchema validation error",
            parsed.error,
            petData
          );
          throw new Error(
            "Invalid pets data from API: " + JSON.stringify(petData)
          );
        }
        setPets(
          parsed.data.map((pet) => ({ ...pet, species: pet.species ?? "" }))
        );
        setOwners(ownerData);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  function getOwnerName(owner_id: number) {
    const owner = owners.find((o) => o.id === owner_id);
    return owner ? owner.name : `Owner #${owner_id}`;
  }

  if (loading) return <div>Loading pets...</div>;
  if (error) return <div className="text-red-600">Error: {error}</div>;

  return (
    <main
      className="w-full flex flex-col items-center"
      style={{ background: "var(--ctp-mocha-base)", minHeight: "100vh" }}
    >
      <h2 className="text-[1.2rem] font-semibold mb-4">Pets</h2>
      <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 w-full max-w-3xl">
        {pets.map((pet) => {
          const expanded = expandedPetId === pet.id;
          return (
            <Card
              key={pet.id}
              expanded={expanded}
              onToggle={() => setExpandedPetId(expanded ? null : pet.id)}
              header={
                <>
                  {pet.photo_filename && (
                    <img
                      src={`http://localhost:8000/images/${pet.photo_filename}`}
                      alt={pet.name}
                      className="w-full h-40 object-cover rounded mb-2 border border-gray-200 bg-gray-50"
                      loading="lazy"
                    />
                  )}
                  <header className="flex items-center gap-2 mb-1">
                    <span className="text-lg font-bold text-green-700">
                      {pet.name}
                    </span>
                    <span className="text-xs text-gray-500">#{pet.id}</span>
                  </header>
                  <div className="text-gray-700 text-base">
                    <span className="font-medium">Species:</span>{" "}
                    {pet.species || (
                      <span className="italic text-gray-400">Unknown</span>
                    )}
                  </div>
                  <div className="text-gray-700 text-base">
                    <span className="font-medium">Owner:</span>{" "}
                    {getOwnerName(pet.owner_id)}
                  </div>
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
                  aria-label="Pet details"
                >
                  {pet.breed && (
                    <div>
                      <span className="font-medium">Breed:</span> {pet.breed}
                    </div>
                  )}
                  {pet.color && (
                    <div>
                      <span className="font-medium">Color:</span> {pet.color}
                    </div>
                  )}
                  {pet.age !== undefined &&
                    pet.age !== null &&
                    pet.age !== 0 && (
                      <div>
                        <span className="font-medium">Age:</span> {pet.age}{" "}
                        year(s)
                      </div>
                    )}
                  {pet.weight !== undefined &&
                    pet.weight !== null &&
                    pet.weight !== 0 && (
                      <div>
                        <span className="font-medium">Weight:</span>{" "}
                        {pet.weight} kg
                      </div>
                    )}
                  {pet.gender && (
                    <div>
                      <span className="font-medium">Gender:</span> {pet.gender}
                    </div>
                  )}
                  {pet.birthdate && (
                    <div>
                      <span className="font-medium">Birthdate:</span>{" "}
                      {pet.birthdate}
                    </div>
                  )}
                  {pet.is_vaccinated !== undefined && (
                    <div>
                      <span className="font-medium">Vaccinated:</span>{" "}
                      {pet.is_vaccinated ? "Yes" : "No"}
                    </div>
                  )}
                  {pet.description && (
                    <div>
                      <span className="font-medium">Description:</span>{" "}
                      {pet.description}
                    </div>
                  )}
                  {pet.date_added && (
                    <div>
                      <span className="font-medium">Added:</span>{" "}
                      {(() => {
                        const d = new Date(pet.date_added as string);
                        return d.toLocaleString(undefined, {
                          year: "numeric",
                          month: "short",
                          day: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        });
                      })()}
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
