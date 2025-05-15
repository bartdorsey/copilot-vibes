import React, { useRef } from "react";

interface PhotoUploadProps {
  value: File | null;
  previewUrl: string | null;
  onChange: (file: File | null) => void;
}

export function PhotoUpload({ value, previewUrl, onChange }: PhotoUploadProps) {
  const [dragActive, setDragActive] = React.useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Use a key to reset the file input when value changes (e.g., after submit)
  const inputKey = value ? value.name + value.size : "empty";

  function handlePhotoChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] || null;
    onChange(file);
  }

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0] || null;
    onChange(file);
  }
  function handleDragOver(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragActive(true);
  }
  function handleDragLeave(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setDragActive(false);
  }

  return (
    <div
      className={`flex flex-col items-center justify-center border-2 border-dashed rounded-md p-4 mb-2 transition-colors ${
        dragActive ? "border-green-500 bg-green-50" : "border-gray-300 bg-white"
      }`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      style={{ cursor: "pointer" }}
      onClick={() => inputRef.current?.click()}
    >
      {previewUrl ? (
        <img
          src={previewUrl}
          alt="Preview"
          className="max-h-32 object-contain mb-2 rounded"
        />
      ) : (
        <span className="text-gray-500">
          Drag & drop a photo here, or click to select
        </span>
      )}
      <input
        key={inputKey}
        ref={inputRef}
        id="photo-input"
        type="file"
        name="photo"
        accept="image/*"
        className="hidden"
        onChange={handlePhotoChange}
      />
    </div>
  );
}
