import React, { useState } from "react";

function App() {
  const [plaintext, setPlaintext] = useState("");
  const [key, setKey] = useState("");
  const [ciphertext, setCiphertext] = useState("");

  const handleEncrypt = async () => {
    if (!plaintext || !key) {
      alert("Enter both plaintext and key!");
      return;
    }
    const response = await fetch("http://localhost:5000/encrypt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plaintext, key }),
    });
    const data = await response.json();
    setCiphertext(data.ciphertext);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Xycrypt Encryption Demo</h2>
      <input
        type="text"
        placeholder="Enter plaintext"
        value={plaintext}
        onChange={(e) => setPlaintext(e.target.value)}
        style={{ marginRight: "1rem" }}
      />
      <input
        type="text"
        placeholder="Enter key"
        value={key}
        onChange={(e) => setKey(e.target.value)}
        style={{ marginRight: "1rem" }}
      />
      <button onClick={handleEncrypt}>Encrypt</button>
      <div style={{ marginTop: "1rem" }}>
        <strong>Ciphertext: </strong>{ciphertext}
      </div>
    </div>
  );
}

export default App;
