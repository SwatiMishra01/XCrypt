import React, { useState } from "react";
import "./App.css";

function App() {
  const [encryptKey, setEncryptKey] = useState("");
  const [plaintext, setPlaintext] = useState("");
  const [ciphertext, setCiphertext] = useState("");
  const [encryptMessage, setEncryptMessage] = useState("");

  const [decryptKey, setDecryptKey] = useState("");
  const [decryptCiphertext, setDecryptCiphertext] = useState("");
  const [decryptedText, setDecryptedText] = useState("");
  const [decryptMessage, setDecryptMessage] = useState("");
  const [decryptError, setDecryptError] = useState("");

  // Encrypt
  const handleEncrypt = async () => {
    if (!encryptKey || !plaintext) {
      alert("Enter both key and plaintext!");
      return;
    }
    const response = await fetch("http://localhost:5000/encrypt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plaintext, key: encryptKey }),
    });
    const data = await response.json();
    if (data.ciphertext) {
      setCiphertext(data.ciphertext);
      setEncryptMessage("✅ Encryption completed successfully!");
    }
  };

  // Decrypt
  const handleDecrypt = async () => {
    if (!decryptKey || !decryptCiphertext) {
      alert("Enter both key and ciphertext!");
      return;
    }
    const response = await fetch("http://localhost:5000/decrypt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ciphertext: decryptCiphertext, key: decryptKey }),
    });
    const data = await response.json();
    if (data.error) {
      setDecryptError("❌ " + data.error);
      setDecryptedText("");
      setDecryptMessage("");
    } else {
      setDecryptedText(data.plaintext);
      setDecryptMessage("✅ Decryption completed successfully!");
      setDecryptError("");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial", maxWidth: "600px", margin: "auto" }}>
      <h1>Xycrypt - Encryption & Decryption Tool</h1>

      {/* Encryption */}
      <div style={{ marginBottom: "2rem", padding: "1rem", border: "1px solid #ccc", borderRadius: "8px" }}>
        <h2>Encryption</h2>
        <input
          type="text"
          placeholder="Encryption Key"
          value={encryptKey}
          onChange={(e) => setEncryptKey(e.target.value)}
          style={{ marginRight: "1rem", width: "200px" }}
        />
        <input
          type="text"
          placeholder="Plaintext"
          value={plaintext}
          onChange={(e) => setPlaintext(e.target.value)}
          style={{ marginRight: "1rem", width: "200px" }}
        />
        <button onClick={handleEncrypt}>Encrypt</button>
        {encryptMessage && <p style={{ color: "green" }}>{encryptMessage}</p>}
        {ciphertext && (
          <div>
            <strong>Encryption Result:</strong>
            <p>
              {ciphertext}{" "}
              <button onClick={() => navigator.clipboard.writeText(ciphertext)}>Copy</button>
            </p>
          </div>
        )}
      </div>

      {/* Decryption */}
      <div style={{ padding: "1rem", border: "1px solid #ccc", borderRadius: "8px" }}>
        <h2>Decryption</h2>
        <input
          type="text"
          placeholder="Decryption Key"
          value={decryptKey}
          onChange={(e) => setDecryptKey(e.target.value)}
          style={{ marginRight: "1rem", width: "200px" }}
        />
        <input
          type="text"
          placeholder="Ciphertext"
          value={decryptCiphertext}
          onChange={(e) => setDecryptCiphertext(e.target.value)}
          style={{ marginRight: "1rem", width: "200px" }}
        />
        <button onClick={handleDecrypt}>Decrypt</button>
        {decryptMessage && <p style={{ color: "green" }}>{decryptMessage}</p>}
        {decryptError && <p style={{ color: "red" }}>{decryptError}</p>}
        {decryptedText && (
          <div>
            <strong>Decryption Result:</strong>
            <p>
              {decryptedText}{" "}
              <button onClick={() => navigator.clipboard.writeText(decryptedText)}>Copy</button>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
