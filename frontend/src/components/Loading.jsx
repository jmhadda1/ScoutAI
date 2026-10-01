import { useEffect, useState } from "react";

function Loading({ file }) {

  const [step, setStep] = useState(0);

  const steps = [
    "Uploading Screenshot...",
    "Reading Marketplace Listing...",
    "Running AI Analysis...",
    "Calculating Scout Score..."
  ];

  useEffect(() => {

    const interval = setInterval(() => {

      setStep((current) => {

        if (current >= steps.length - 1) {

          clearInterval(interval);

          return current;

        }

        return current + 1;

      });

    }, 900);

    return () => clearInterval(interval);

  }, []);

  return (

    <>

      <h1>Scout AI</h1>

      <h2>Analyzing Listing</h2>

      <div className="upload-card">

        {file && (

          <img

            src={URL.createObjectURL(file)}

            alt="Preview"

            style={{

              width: "100%",

              borderRadius: "15px",

              marginBottom: "25px"

            }}

          />

        )}

        <div className="spinner"></div>

        <div className="steps">

          {steps.map((text, index) => (

            <p

              key={index}

              style={{

                opacity: index <= step ? 1 : .35,

                fontWeight: index === step ? 700 : 400,

                transition: ".3s"

              }}

            >

              {index < step ? "✅ " : "⏳ "}

              {text}

            </p>

          ))}

        </div>

      </div>

    </>

  );

}

export default Loading;