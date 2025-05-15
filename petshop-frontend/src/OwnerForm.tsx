import { useState } from "react";
import { createOwner } from "./api";

export function OwnerForm({ onCreated }: { onCreated?: () => void }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [zipCode, setZipCode] = useState("");
  const [country, setCountry] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await createOwner({
        name,
        email: email || undefined,
        phone: phone || undefined,
        address: address || undefined,
        city: city || undefined,
        state: state || undefined,
        zip_code: zipCode || undefined,
        country: country || undefined,
        date_of_birth: dateOfBirth || undefined,
      });
      setName("");
      setEmail("");
      setPhone("");
      setAddress("");
      setCity("");
      setState("");
      setZipCode("");
      setCountry("");
      setDateOfBirth("");
      onCreated?.();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-2 bg-[#f8f9fa] p-6 rounded-lg shadow-md max-w-[320px]"
    >
      <h3 className="text-[1.2rem] font-semibold mb-2">Add Owner</h3>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Owner name"
        required
        className="px-2 py-2 border border-gray-300 rounded text-base"
        style={{ fontSize: "1rem" }}
      />
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        type="email"
        className="px-2 py-2 border border-gray-300 rounded text-base"
      />
      <input
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        placeholder="Phone"
        type="tel"
        className="px-2 py-2 border border-gray-300 rounded text-base"
      />
      <input
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        placeholder="Address"
        className="px-2 py-2 border border-gray-300 rounded text-base"
      />
      <input
        value={city}
        onChange={(e) => setCity(e.target.value)}
        placeholder="City"
        className="px-2 py-2 border border-gray-300 rounded text-base"
      />
      <input
        value={state}
        onChange={(e) => setState(e.target.value)}
        placeholder="State"
        className="px-2 py-2 border border-gray-300 rounded text-base"
      />
      <input
        value={zipCode}
        onChange={(e) => setZipCode(e.target.value)}
        placeholder="ZIP Code"
        className="px-2 py-2 border border-gray-300 rounded text-base"
      />
      <input
        value={country}
        onChange={(e) => setCountry(e.target.value)}
        placeholder="Country"
        className="px-2 py-2 border border-gray-300 rounded text-base"
      />
      <input
        value={dateOfBirth}
        onChange={(e) => setDateOfBirth(e.target.value)}
        placeholder="Date of Birth"
        type="date"
        className="px-2 py-2 border border-gray-300 rounded text-base"
      />
      <button
        type="submit"
        disabled={loading}
        className="bg-[#2563eb] text-white rounded px-4 py-2 text-[1rem] transition-colors disabled:bg-blue-300 disabled:cursor-not-allowed"
      >
        {loading ? "Adding..." : "Add Owner"}
      </button>
      {error && (
        <div className="text-[#dc2626] text-[0.95rem] mt-2">{error}</div>
      )}
    </form>
  );
}
