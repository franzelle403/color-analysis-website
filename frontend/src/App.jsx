import { useState } from "react";
import "./App.css";

function App() {
  const [started, setStarted] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    // Check that the uploaded file is an image
    if (!file.type.startsWith("image/")) {
      setError("Please upload an image file.");
      return;
    }

    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
    setError("");
  };

  const analyzeImage = async () => {
    if (!selectedFile) {
      setError("Please choose a photo first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("The server returned an error.");
      }

      const data = await response.json();

      if (data.success) {
        setResult(data);
      } else {
        setError(data.message);
      }
    } catch (error) {
      console.error(error);
      setError(
        "We couldn't connect to the analysis server. Make sure your backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {!started ? (

        /* =========================
           LANDING PAGE
        ========================= */

        <main className="hero">
          <div className="hero-content">

            <p className="eyebrow">
              PERSONALIZED COLOR ANALYSIS
            </p>

            <h1>
              Find the colors
              <br />
              <span>made for you.</span>
            </h1>

            <p className="subtitle">
              Discover your skin tone, undertone, and best-matching
              makeup shades with AI-powered color analysis.
            </p>

            <button
              className="primary-button"
              onClick={() => setStarted(true)}
            >
              Start Your Analysis
            </button>

            <p className="small-text">
              Takes less than 2 minutes · No makeup required
            </p>

          </div>
        </main>

      ) : (

        /* =========================
           ANALYSIS PAGE
        ========================= */

        <main className="analysis-page">

          <div className="analysis-card">

            <p className="eyebrow">
              STEP 1 OF 3
            </p>

            <h2>
              Let's find your colors.
            </h2>

            <p className="description">
              Upload a clear photo of your face so our system
              can analyze your coloring and recommend makeup shades.
            </p>


            {/* =========================
                UPLOAD AREA
            ========================= */}

            {!preview && (

              <div className="upload-box">

                <div className="upload-icon">
                  +
                </div>

                <h3>
                  Upload your photo
                </h3>

                <p>
                  Use a clear photo taken in natural lighting.
                </p>

                <label className="secondary-button">
                  Choose Photo

                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    hidden
                  />

                </label>

              </div>

            )}


            {/* =========================
                IMAGE PREVIEW
            ========================= */}

            {preview && (

              <div className="preview-section">

                <img
                  src={preview}
                  alt="Selected selfie"
                  className="photo-preview"
                />

                <p className="file-name">
                  {selectedFile.name}
                </p>

                <div className="button-row">

                  <label className="secondary-button">

                    Choose Another

                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileChange}
                      hidden
                    />

                  </label>

                  <button
                    className="primary-button"
                    onClick={analyzeImage}
                    disabled={loading}
                  >
                    {loading
                      ? "Analyzing..."
                      : "Analyze My Photo"}
                  </button>

                </div>

              </div>

            )}


            {/* =========================
                ERROR
            ========================= */}

            {error && (

              <div className="error-message">
                {error}
              </div>

            )}


{/* =========================
    BACKEND RESULT
========================= */}

{result && result.analysis && (
  <>
    <div className="result-box">

      <div className="success-icon">
        ✓
      </div>

      <p className="eyebrow">
        YOUR COLOR PROFILE
      </p>

      <h3>
        Your analysis is ready.
      </h3>

      <div className="profile-grid">

        <div className="profile-item">
          <span>Skin Depth</span>
          <strong>
            {result.analysis.skin_depth}
          </strong>
        </div>

        <div className="profile-item">
          <span>Undertone</span>
          <strong>
            {result.analysis.undertone}
          </strong>
        </div>

        <div className="profile-item">
          <span>Contrast</span>
          <strong>
            {result.analysis.contrast}
          </strong>
        </div>

        <div className="profile-item">
          <span>Lighting</span>
          <strong>
            {result.analysis.lighting}
          </strong>
        </div>

        <div className="profile-item">
          <span>Photo Quality</span>
          <strong>
            {result.analysis.image_quality}
          </strong>
        </div>

        <div className="profile-item">
          <span>Confidence</span>
          <strong>
            {result.analysis.confidence
              ? `${Math.round(
                  result.analysis.confidence * 100
                )}%`
              : "N/A"}
          </strong>
        </div>

        {result.analysis.season && (
          <div className="profile-item">
            <span>Color Season</span>
            <strong>
              {result.analysis.season}
            </strong>
          </div>
        )}

      </div>

    </div>


    {/* =========================
        MAKEUP RECOMMENDATIONS
    ========================= */}

    <div className="recommendations-section">

      <p className="eyebrow">
        YOUR MAKEUP MATCHES
      </p>

      <h2>
        Recommended makeup for you
      </h2>

      {result.makeup_recommendations &&
      result.makeup_recommendations.length > 0 ? (

        <div className="makeup-grid">

          {result.makeup_recommendations.map(
            (product) => (

              <div
                className="makeup-card"
                key={product.id}
              >

                {product.image_url ? (
                  <img
                    src={product.image_url}
                    alt={`${product.brand} ${product.product_name}`}
                    className="makeup-image"
                  />
                ) : (
                  <div className="makeup-image-placeholder">
                    No image
                  </div>
                )}

                <div className="makeup-card-content">

                  <span className="makeup-category">
                    {product.category}
                  </span>

                  <h3>
                    {product.brand}
                  </h3>

                  <p className="makeup-name">
                    {product.product_name}
                  </p>

                  <p>
                    Shade:{" "}
                    <strong>
                      {product.shade}
                    </strong>
                  </p>

                  <div className="makeup-tags">

                    {product.season && (
                      <span>
                        {product.season}
                      </span>
                    )}

                    {product.undertone && (
                      <span>
                        {product.undertone}
                      </span>
                    )}

                    {product.depth && (
                      <span>
                        {product.depth}
                      </span>
                    )}

                    {product.chroma && (
                      <span>
                        {product.chroma}
                      </span>
                    )}

                  </div>

                  {product.price !== null &&
                    product.price !== undefined && (
                    <p className="makeup-price">
                      ₱{Number(
                        product.price
                      ).toFixed(2)}
                    </p>
                  )}

                  {product.buy_url && (
                    <a
                      href={product.buy_url}
                      target="_blank"
                      rel="noreferrer"
                      className="buy-button"
                    >
                      Buy Now
                    </a>
                  )}

                </div>

              </div>
            )
          )}

        </div>

      ) : (

        <div className="no-recommendations">
          No makeup recommendations were found
          for this color profile yet.
        </div>

      )}

    </div>
  </>
)}

            <button
              className="back-button"
              onClick={() => {
                setStarted(false);
                setSelectedFile(null);
                setPreview(null);
                setResult(null);
                setError("");
              }}
            >
              ← Back
            </button>

          </div>

        </main>

      )}

    </div>
  );
}

export default App;