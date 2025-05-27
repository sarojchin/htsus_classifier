import React, { useState } from "react";

export default function App() {   
  const [description, setDescription] = useState("");
  const [classification, setClassification] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
<<<<<<< HEAD
      const render_api_url = "https://htsus-classifier-2.onrender.com"
      const response = await fetch(render_api_url + "/classify", {
=======
      const response = await fetch("http://localhost:8000/classify", {    
>>>>>>> main
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description }),
      }); 
          
      if (!response.ok) {
        throw new Error("API error");
      }

      const data = await response.json();
      setClassification(data.classification);

    } catch (err) {
      setError("Failed to classify product.");
    } finally {
      setLoading(false);  
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "2rem auto", fontFamily: "Arial" }}>
      <h1>Product Classification</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="desc">Product Description:</label>
        <textarea
          id="desc"   
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={4}
          style={{ width: "100%", padding: 8, marginTop: 4, marginBottom: 12 }}
          placeholder="Enter product description here..."
          required
        />
        <button type="submit" disabled={loading} style={{ padding: "8px 16px" }}>
          {loading ? "Classifying..." : "Classify"}
        </button>
      </form>

      {
        <div style={{ marginTop: 24, padding: 16, border: "1px solid #ccc" }}>
          <strong>Classification Code:</strong> {classification}
        </div>
      }

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
