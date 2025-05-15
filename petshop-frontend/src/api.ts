// Utility functions for interacting with the FastAPI backend
// Handles API requests for owners and pets

export const API_BASE_URL = "http://localhost:8000"; // Adjust if backend runs elsewhere

export async function fetchOwners() {
  const res = await fetch(`${API_BASE_URL}/owners`);
  if (!res.ok) throw new Error("Failed to fetch owners");
  return res.json();
}

export async function createOwner(data: {
  name: string;
  email?: string | null;
  phone?: string | null;
  address?: string | null;
  city?: string | null;
  state?: string | null;
  zip_code?: string | null;
  country?: string | null;
  date_of_birth?: string | null;
}) {
  const res = await fetch(`${API_BASE_URL}/owners`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create owner");
  return res.json();
}

export async function fetchPets() {
  const res = await fetch(`${API_BASE_URL}/pets`, {
    headers: { Accept: "application/json" },
  });
  let data;
  try {
    data = await res.json();
  } catch (e) {
    throw new Error(
      "API did not return valid JSON. Response: " + (await res.text?.())
    );
  }
  if (!res.ok) {
    let errMsg = "Failed to fetch pets";
    if (data && typeof data === "object" && data.detail) {
      errMsg = data.detail;
    } else if (typeof data === "string") {
      errMsg = data;
    }
    throw new Error(errMsg);
  }
  if (!Array.isArray(data)) {
    throw new Error(
      "API did not return a list of pets. Got: " + JSON.stringify(data)
    );
  }
  return data.map((pet: any) => ({
    ...pet,
    photo_filename: pet.photo_filename ?? null,
    species: pet.species ?? null,
  }));
}

export async function createPet(data: {
  name: string;
  species?: string;
  owner_id: number;
  age?: number;
  breed?: string;
  color?: string;
  weight?: number;
  description?: string;
  gender?: string;
  is_vaccinated?: boolean;
  birthdate?: string;
  photoFile?: File | null;
}) {
  const formData = new FormData();
  formData.append("name", data.name);
  formData.append("owner_id", String(data.owner_id));
  if (data.species) formData.append("species", data.species);
  if (data.age !== undefined) formData.append("age", String(data.age));
  if (data.breed) formData.append("breed", data.breed);
  if (data.color) formData.append("color", data.color);
  if (data.weight !== undefined) formData.append("weight", String(data.weight));
  if (data.description) formData.append("description", data.description);
  if (data.gender) formData.append("gender", data.gender);
  if (data.is_vaccinated !== undefined)
    formData.append("is_vaccinated", String(data.is_vaccinated));
  if (data.birthdate) formData.append("birthdate", data.birthdate);
  if (data.photoFile) {
    formData.append("photo", data.photoFile);
  }
  const res = await fetch(`${API_BASE_URL}/pets`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Failed to create pet");
  return res.json();
}
