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


  // --------------------------------
  // STATUS
  // --------------------------------

  let status = "Strong Listing";
  let statusColor = "#22c55e";
  let statusIcon = "🟢";

  if (score < 75) {
    status = "Review Carefully";
    statusColor = "#f59e0b";
    statusIcon = "🟡";
  }

  if (score < 50) {
    status = "High Risk";
    statusColor = "#ef4444";
    statusIcon = "🔴";
  }


  // --------------------------------
  // PRODUCT ICON
  // --------------------------------

  function productIcon(name = "") {

    const product = name.toLowerCase();

    if (product.includes("iphone")) return "📱";
    if (product.includes("ipad")) return "📱";

    if (product.includes("macbook")) return "💻";
    if (product.includes("surface")) return "💻";
    if (product.includes("dell")) return "💻";
    if (product.includes("hp")) return "💻";
    if (product.includes("lenovo")) return "💻";

    if (product.includes("playstation")) return "🎮";
    if (product.includes("xbox")) return "🎮";
    if (product.includes("switch")) return "🎮";
    if (product.includes("steam deck")) return "🎮";

    if (product.includes("airpods")) return "🎧";
    if (product.includes("watch")) return "⌚";

    return "📦";
  }


  // --------------------------------
  // NORMALIZE REASONS
  // --------------------------------

  const normalizedReasons = (
    scout.reasons || []
  ).map((reason) => {

    if (typeof reason === "string") {
      return {
        type: "positive",
        text: reason
      };
    }

    return reason;
  });


  // --------------------------------
  // REMOVE GENERIC INSIGHTS
  // --------------------------------

  const usefulReasons = normalizedReasons.filter(
    (reason) => {

      const text = (
        reason?.text || ""
      ).toLowerCase();

      if (
        text.includes(
          "product successfully identified"
        )
      ) {
        return false;
      }

      return true;
    }
  );


  // --------------------------------
  // SPLIT POSITIVE / WARNING
  // --------------------------------

  let warnings = usefulReasons.filter(
    (reason) => reason?.type === "warning"
  );

  let positives = usefulReasons.filter(
    (reason) => reason?.type !== "warning"
  );


  // --------------------------------
  // PRIORITY
  // --------------------------------

  const warningPriority = [
    "damage",
    "cracked",
    "broken",
    "significantly below",
    "below the typical",
    "paid-off",
    "outstanding balance",
    "functionality",
    "unlocked",
    "battery",
    "configuration",
    "accessories",
    "storage",
    "limited product"
  ];


  const positivePriority = [
    "unlocked",
    "battery information",
    "storage capacity",
    "paid off",
    "functionality",
    "price falls",
    "model configuration",
    "console configuration",
    "carrier",
    "condition",
    "detailed product",
    "useful product"
  ];


  function priorityScore(reason, list) {

    const text = (
      reason?.text || ""
    ).toLowerCase();

    const index = list.findIndex(
      (keyword) => text.includes(keyword)
    );

    return index === -1 ? 999 : index;
  }


  warnings = warnings
    .sort(
      (a, b) =>
        priorityScore(a, warningPriority) -
        priorityScore(b, warningPriority)
    )
    .slice(0, 4);


  positives = positives
    .sort(
      (a, b) =>
        priorityScore(a, positivePriority) -
        priorityScore(b, positivePriority)
    )
    .slice(0, 5);


  // --------------------------------
  // CLEANER DISPLAY WORDING
  // --------------------------------

  function cleanInsight(text = "") {

    const replacements = {
      "Seller states that the phone is unlocked.":
        "Phone is listed as unlocked.",

      "Battery information is provided (89%).":
        "Battery information provided: 89%.",

      "Storage capacity is identified (256GB).":
        "Storage identified: 256GB.",

      "Seller provides information about device functionality.":
        "Seller reports the device is functioning normally.",

      "Price falls within the expected market range.":
        "Price falls within the expected market range.",

      "Paid-off status is not specified.":
        "Verify that the phone is fully paid off.",

      "Device functionality is not explicitly confirmed.":
        "Verify full device functionality.",

      "Console functionality is not explicitly confirmed.":
        "Verify full console functionality.",

      "Included accessories are not clearly described.":
        "Confirm which accessories are included.",

      "Exact console configuration is not specified.":
        "Confirm the exact console configuration."
    };

    return replacements[text] || text;
  }


  // --------------------------------
  // INSIGHT ROW
  // --------------------------------

  function InsightRow({
    icon,
    text
  }) {

    return (
      <div
        style={{
          display: "flex",
          alignItems: "flex-start",
          gap: "10px",
          width: "100%",
          marginBottom: "12px",
          textAlign: "left"
        }}
      >

        <span
          style={{
            flexShrink: 0,
            width: "24px",
            textAlign: "center",
            lineHeight: "1.5"
          }}
        >
          {icon}
        </span>

        <span
          style={{
            flex: 1,
            lineHeight: "1.5",
            textAlign: "left"
          }}
        >
          {cleanInsight(text)}
        </span>

      </div>
    );
  }


  // --------------------------------
  // PAGE
  // --------------------------------

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
          {statusIcon} {status}
        </h2>


        <hr />


        {/* PRODUCT */}

        <div className="result-section">

          <h4>
            {productIcon(
              listing.product_name
            )} Product
          </h4>

          <p>
            {listing.product_name ||
              "Unknown"}
          </p>

        </div>


        {/* PRICE */}

        <div className="result-section">

          <h4>
            💲 Asking Price
          </h4>

          <p>
            {listing.asking_price
              ? `$${listing.asking_price}`
              : "Not detected from screenshot"}
          </p>

        </div>


        {/* CONDITION */}

        <div className="result-section">

          <h4>
            📦 Condition
          </h4>

          <p>
            {listing.condition ||
              "Not specified"}
          </p>

        </div>


        {/* RECOMMENDATION */}

        <div
          className="recommendation"
          style={{
            borderLeft:
              `6px solid ${statusColor}`
          }}
        >

          <h4>
            🛡 Scout Recommendation
          </h4>

          <p>
            {scout.recommendation ||
              "Review the listing carefully before purchasing."}
          </p>

        </div>


        {/* POSITIVE SIGNALS */}

        {positives.length > 0 && (

          <div
            className="result-section"
            style={{
              width: "100%",
              boxSizing: "border-box"
            }}
          >

            <h4
              style={{
                marginBottom: "18px"
              }}
            >
              Positive Signals
            </h4>

            <div
              style={{
                width: "100%",
                maxWidth: "390px",
                margin: "0 auto"
              }}
            >

              {positives.map(
                (reason, index) => (

                  <InsightRow
                    key={index}
                    icon="✅"
                    text={reason.text}
                  />

                )
              )}

            </div>

          </div>

        )}


        {/* THINGS TO VERIFY */}

        {warnings.length > 0 && (

          <div
            className="result-section"
            style={{
              width: "100%",
              boxSizing: "border-box"
            }}
          >

            <h4
              style={{
                marginBottom: "18px"
              }}
            >
              Things to Verify
            </h4>

            <div
              style={{
                width: "100%",
                maxWidth: "390px",
                margin: "0 auto"
              }}
            >

              {warnings.map(
                (reason, index) => (

                  <InsightRow
                    key={index}
                    icon="⚠️"
                    text={reason.text}
                  />

                )
              )}

            </div>

          </div>

        )}


        {/* BUTTON */}

        <button onClick={onReset}>

          ✨ Analyze Another Listing

        </button>


      </div>

    </>

  );

}


export default Results;