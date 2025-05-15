import { z } from "zod";

export const PetSchema = z.object({
  id: z.number(),
  name: z.string(),
  species: z.string().nullable().optional(),
  owner_id: z.number(),
  age: z.number().nullable().optional(),
  breed: z.string().nullable().optional(),
  color: z.string().nullable().optional(),
  weight: z.number().nullable().optional(),
  description: z.string().nullable().optional(),
  gender: z.string().nullable().optional(),
  is_vaccinated: z.boolean().nullable().optional(),
  birthdate: z.string().nullable().optional(),
  date_added: z.string().nullable().optional(),
  photo_filename: z.string().nullable().optional(),
});

export const OwnerSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().nullable().optional(),
  phone: z.string().nullable().optional(),
  address: z.string().nullable().optional(),
  city: z.string().nullable().optional(),
  state: z.string().nullable().optional(),
  zip_code: z.string().nullable().optional(),
  country: z.string().nullable().optional(),
  date_of_birth: z.string().nullable().optional(),
});

export const PetArraySchema = z.array(PetSchema);
export const OwnerArraySchema = z.array(OwnerSchema);

export type Pet = z.infer<typeof PetSchema>;
export type Owner = z.infer<typeof OwnerSchema>;
