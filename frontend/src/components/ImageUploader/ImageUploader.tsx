import React, { useState } from "react";

import api from "../../api";

import "./ImageUploader.css";

function ImageUploader() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    // Client-side validation
    if (!file) return;

    if (!["image/jpeg", "image/png", "image/gif"].includes(file.type)) {
      setError("Invalid file type. Only JPEG, PNG, and GIF are allowed.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      // 5MB limit
      setError("File size exceeds 5MB limit.");
      return;
    }

    setSelectedFile(file);
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);

    try {
      // Get pre-signed URL from backend
      const response = await api.post("/image/uploadURL", {
        fileName: selectedFile.name,
        fileType: selectedFile.type,
      });

      if (!response) throw new Error("Failed to get upload URL");

      const { presignedUrl, fileUrl } = response.data;

      // Upload directly to S3 using the pre-signed URL
      const upload = async (chunk: ArrayBuffer) => {
        const chunkResponse = await fetch(presignedUrl, {
          method: "PUT",
          body: chunk,
          headers: { "Content-Type": selectedFile.type },
        });
        if (chunkResponse.status !== 200) {
          throw new Error("Upload failed");
        }
      };

      const chunks = await selectedFile.arrayBuffer();
      const chunkSize = 1024 * 1024; // 1MB
      const totalChunks = Math.ceil(chunks.byteLength / chunkSize);

      for (let i = 0; i < totalChunks; i++) {
        const chunk = chunks.slice(i * chunkSize, (i + 1) * chunkSize);
        await upload(chunk);
        setUploadProgress(((i + 1) / totalChunks) * 100);
      }

      // Notify backend of successful upload
      await fetch("/api/confirmUpload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fileUrl }),
      });

      // Handle successful upload (e.g., display image, update UI)
      console.log("Upload successful:", fileUrl);
    } catch (err: any) {
      setError("Upload failed: " + err.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="imageUploader">
      <label className="fileInputLabel">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z"
            fill="currentColor"
          />
        </svg>
        이미지 선택
        <input type="file" onChange={handleFileChange} accept="image/*" />
      </label>

      {selectedFile && (
        <div className="previewContainer">
          <img
            className="imagePreview"
            src={URL.createObjectURL(selectedFile)}
            alt="Preview"
          />
          <div className="fileName">{selectedFile.name}</div>
        </div>
      )}

      {isUploading && (
        <div className="progressContainer">
          <div
            className="progressBar"
            style={{ width: `${uploadProgress}%` }}
          ></div>
        </div>
      )}

      {error && <div className="errorMessage">{error}</div>}

      <button
        className="uploadButton"
        onClick={handleUpload}
        disabled={!selectedFile || isUploading}
      >
        {isUploading ? "업로드 중..." : "이미지 업로드"}
      </button>
    </div>
  );
}

export default ImageUploader;
