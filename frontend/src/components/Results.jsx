import { useState, useEffect } from "react";

function AnimatedScore({ score }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    let current = 0;

    const timer = setInterval(() => {
      current += 2;

      if (current >= score) {
        current = score;
        clearInterval(timer);
      }

      setDisplay(current);
    }, 20);

    return () => clearInterval(timer);
  }, [score]);

  let color = "#22c55e";

  if (score < 75) color = "#f59e0b";
  if (score < 50) color = "#ef4444";

  return (
    <div
      className="confidence-score"
      style={{ background: color }}
    >
      {display}
    </div>
  );
}

function Results({ analysis, onReset }) {

  const listing = analysis?.listing || {};
  const scout = analysis?.scout || {};

  const score = scout.score ?? 0;

  let status = "Recommended";
  let statusColor = "#22c55e";
  let icon = "🟢";

  if (score < 75) {
    status = "Review Carefully";
    statusColor = "#f59e0b";
    icon = "🟡";
  }

  if (score < 50) {
    status = "High Risk";
    statusColor = "#ef4444";
    icon = "🔴";
  }

  function productIcon(name = "") {

    const product = name.toLowerCase();

    if (product.includes("iphone")) return "📱";
    if (product.includes("macbook")) return "💻";
    if (product.includes("playstation")) return "🎮";
    if (product.includes("xbox")) return "🎮";
    if (product.includes("switch")) return "🎮";
    if (product.includes("airpods")) return "🎧";
    if (product.includes("watch")) return "⌚";

    return "📦";

  }

  return (

    <>

      <h1>Scout AI</h1>

      <h2>AI Purchase Analysis</h2>

      <div className="results-card">

        <AnimatedScore score={score} />

        <h2
          style={{
            marginTop: 20,
            color: statusColor
          }}
        >
          {icon} {status}
        </h2>

        <hr />

        <div className="result-section">

          <h4>

            {productIcon(listing.product_name)} Product

          </h4>

          <p>{listing.product_name || "Unknown"}</p>

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
          className="recommendation"
          style={{
            borderLeft: `6px solid ${statusColor}`
          }}
        >

          <h4>🛡 Scout Recommendation</h4>

          <p>

            {scout.recommendation}

          </p>

        </div>

        <div className="result-section">

          <h4>Purchase Insights</h4>

          <ul>

            {(scout.reasons || []).map((reason, index) => (

              <li key={index}>

                ✅ {reason}

              </li>

            ))}

          </ul>

        </div>

        <button onClick={onReset}>

          ✨ Analyze Another Listing

        </button>

      </div>

    </>

  );

}

export default Results;