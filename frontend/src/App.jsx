import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a file");
      return;
    }

    

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("https://ai-financial-document-intelligence-1.onrender.com/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Server error");
      }

      const data = await res.json();

      if (data.status !== "success") {
        alert(data.message || "Analysis failed");
        return;
      }

      
      setResult(data.extracted_data);

    } catch (err) {
      console.error(err);
      alert("Error analyzing document");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "Arial" }}>
      <h1>📄 AI Financial Document Intelligence Platform</h1>
      <p>
        Upload an invoice (image or PDF) to automatically extract financial data,
        confidence score, summary, and risk alerts.
      </p>

      <input
        type="file"
        accept=".png,.jpg,.jpeg,.pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Document"}
      </button>

      {/*  RESULTS */}
      {result && (
        <div style={{ marginTop: 30 }}>
          <h2>📊 Extracted Data</h2>

          <pre
            style={{
              background: "#f4f4f4",
              padding: 20,
              borderRadius: 8,
              overflowX: "auto",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
           <h3 style={{ marginTop: 20 }}>✏️ Review & Edit Extracted Data</h3>

    {Object.keys(result).map((key) =>
      typeof result[key] === "string" && (
        <div key={key} style={{ marginBottom: 10 }}>
          <label>
            <b>{key}</b>
          </label>
          <br />
          <input
            value={result[key] || ""}
            onChange={(e) =>
              setResult({ ...result, [key]: e.target.value })
            }
            style={{
              width: "100%",
              padding: 8,
              borderRadius: 6,
              border: "1px solid #ccc",
            }}
          />
        </div>
      )
    )}

          {/* Confidence */}
          <h3>
            Confidence Score:{" "}
            <span
              style={{
                fontWeight: "bold",
                color:
                  result.confidence > 0.75
                    ? "green"
                    : result.confidence > 0.5
                    ? "orange"
                    : "red",
              }}
            >
              {result.confidence}
            </span>
          </h3>

          <p>
            <b>Extraction Engine:</b> {result.extraction_method}
          </p>

          {/* AI Summary */}
          {result.summary && (
            <div
              style={{
                marginTop: 20,
                padding: 15,
                background: "#e8f4ff",
                borderRadius: 8,
              }}
            >
              <b>🧠 AI Summary</b>
              <p>{result.summary}</p>
            </div>
          )}

          {/* Risk Flags */}
          {result.risk_flags && result.risk_flags.length > 0 && (
            <div
              style={{
                marginTop: 20,
                padding: 15,
                background: "#fff3cd",
                borderRadius: 8,
              }}
            >
              <b>⚠️ Risk Alerts</b>
              <ul>
                {result.risk_flags.map((risk, index) => (
                  <li key={index}>{risk}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
