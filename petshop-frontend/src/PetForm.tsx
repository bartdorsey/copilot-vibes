import { useEffect, useState } from "react";
import { createPet, fetchOwners } from "./api";
import { OwnerArraySchema } from "./schemas";
import type { Owner } from "./schemas";
import { useActionState } from "react";
import { PhotoUpload } from "./PhotoUpload";

export function PetForm({ onCreated }: { onCreated?: () => void }) {
  const [error, setError] = useState<string | null>(null);
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [photoPreview, setPhotoPreview] = useState<string | null>(null);

  // Patch formAction to use photoFile from state
  const [, formAction, pending] = useActionState(
    async (_state: any, formData: FormData) => {
      setError(null);
      try {
        const name = formData.get("name") as string;
        const species = formData.get("species") as string;
        const owner_id = Number(formData.get("owner_id"));
        const age = Number(formData.get("age"));
        const breed = formData.get("breed") as string;
        const color = formData.get("color") as string;
        const weight = Number(formData.get("weight"));
        const birthdate = formData.get("birthdate") as string;
        const gender = formData.get("gender") as string;
        const description = formData.get("description") as string;
        const is_vaccinated = formData.get("is_vaccinated") === "true";
        await createPet({
          name,
          species,
          owner_id,
          photoFile,
          age,
          breed,
          color,
          weight,
          birthdate,
          gender,
          description,
          is_vaccinated,
        });
        setPhotoFile(null);
        setPhotoPreview(null);
        onCreated?.();
        return { success: true };
      } catch (e: any) {
        setError(e.message);
        return { error: e.message };
      }
    },
    { success: false }
  );

  const [owners, setOwners] = useState<Owner[]>([]);
  useEffect(() => {
    fetchOwners()
      .then((data) => {
        const parsed = OwnerArraySchema.safeParse(data);
        if (!parsed.success) throw new Error("Invalid owners data from API");
        setOwners(parsed.data);
      })
      .catch((e) => setError(e.message));
  }, []);

  return (
    <form
      action={formAction}
      className="flex flex-col gap-2 bg-[#f8f9fa] p-6 rounded-lg shadow-md max-w-[320px]"
    >
      <h3 className="text-[1.2rem] font-semibold mb-2">Add Pet</h3>
      <input
        name="name"
        placeholder="Pet name"
        required
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <input
        name="species"
        placeholder="Species"
        required
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <select
        name="owner_id"
        required
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      >
        <option value="">Select owner</option>
        {owners.map((owner) => (
          <option key={owner.id} value={owner.id}>
            {owner.name}
          </option>
        ))}
      </select>
      <input
        name="age"
        type="number"
        placeholder="Age (years)"
        min={0}
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <input
        name="breed"
        placeholder="Breed"
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <input
        name="color"
        placeholder="Color"
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <input
        name="weight"
        type="number"
        step="0.01"
        placeholder="Weight (kg)"
        min={0}
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <input
        name="birthdate"
        type="date"
        placeholder="Birthdate"
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <select
        name="gender"
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
        defaultValue=""
      >
        <option value="">Gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="unknown">Unknown</option>
      </select>
      <input
        name="description"
        placeholder="Description"
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <label className="flex items-center gap-2">
        <input type="checkbox" name="is_vaccinated" value="true" />
        Vaccinated
      </label>
      <PhotoUpload
        value={photoFile}
        previewUrl={photoPreview}
        onChange={(file) => {
          setPhotoFile(file);
          if (file) {
            setPhotoPreview(URL.createObjectURL(file));
          } else {
            setPhotoPreview(null);
          }
        }}
      />
      <button
        type="submit"
        disabled={pending}
        className="bg-[#059669] text-white rounded px-4 py-2 text-[1rem] transition-colors disabled:bg-green-300 disabled:cursor-not-allowed"
      >
        {pending ? "Adding..." : "Add Pet"}
      </button>
      {error && (
        <div className="text-[#dc2626] text-[0.95rem] mt-2">{error}</div>
      )}
    </form>
  );
}
