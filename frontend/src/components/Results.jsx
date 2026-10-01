import { useState, useEffect } from "react";

function AnimatedScore({ score, color }) {
  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    let current = 0;

    const timer = setInterval(() => {
      current += 2;

      if (current >= score) {
        current = score;
        clearInterval(timer);
      }

      setDisplayScore(current);
    }, 20);

    return () => clearInterval(timer);
  }, [score]);

  return (
    <div
      className="confidence-score"
      style={{
        background: color,
      }}
    >
      {displayScore}
    </div>
  );
}

function Results({ analysis, onReset }) {
  const listing = analysis?.listing || {};
  const scout = analysis?.scout || {};

  const score = scout.score ?? 0;

  const scoreColor =
    score >= 85
      ? "#22c55e"
      : score >= 60
      ? "#f59e0b"
      : "#ef4444";

  const scoreLabel = scout.rating || "Analysis Complete";

  function getProductIcon(name = "") {
    const product = name.toLowerCase();

    if (product.includes("iphone")) return "📱";
    if (product.includes("macbook")) return "💻";
    if (product.includes("ps")) return "🎮";
    if (product.includes("playstation")) return "🎮";
    if (product.includes("airpods")) return "🎧";
    if (product.includes("watch")) return "⌚";

    return "📦";
  }

  return (
    <>
      <h1>Scout AI</h1>

      <h2>Purchase Confidence</h2>

      <p
  style={{
    marginTop: "8px",
    marginBottom: "20px",
    color: "#666",
    fontSize: "15px"
  }}
>
  AI-powered analysis of a Facebook Marketplace listing
</p>

      <div className="results-card">

        <AnimatedScore
          score={score}
          color={scoreColor}
        />

        <h3
          className="confidence-text"
          style={{
            color: scoreColor,
          }}
        >
          {scoreLabel}
        </h3>

        <hr />

        <div className="result-section">

          <h4>
            {getProductIcon(listing.product_name)} Product
          </h4>

          <p>
            {listing.product_name || "Unknown"}
          </p>

        </div>

        <div className="result-section">

          <h4>💲 Asking Price</h4>

          <p>
            {listing.asking_price
              ? `$${listing.asking_price}`
              : "Not detected"}
          </p>

        </div>

        <div className="result-section">

          <h4>📦 Condition</h4>

          <p>
            {listing.condition || "Unknown"}
          </p>

        </div>

        {listing.storage && (
          <div className="result-section">

            <h4>💾 Storage</h4>

            <p>{listing.storage}</p>

          </div>
        )}

<div
  className={`recommendation ${
    score >= 85
      ? "good"
      : score >= 60
      ? "warning"
      : "bad"
  }`}
>        
          <h4>🛡 Purchase Recommendation</h4>

          <p>
            {scout.recommendation ||
              "No recommendation available."}
          </p>

        </div>

        <div className="result-section">

          <h4>Purchase Insights</h4>

          <ul>

            {(scout.reasons || []).map(
              (reason, index) => (
                <li key={index}>
                  ✅ {reason}
                </li>
              )
            )}

          </ul>

        </div>

        <button onClick={onReset}>
          ✨ Analyze Another Listing
        </button>

      </div>
    </>
  );
}
<p
  style={{
    marginTop: "25px",
    fontSize: "13px",
    color: "#888",
    textAlign: "center"
  }}
>
  Scout AI provides decision support only.
  Always inspect items before purchasing.
</p>

export default Results;