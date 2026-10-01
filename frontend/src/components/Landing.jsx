function Landing({ handleUpload }) {

  return (

    <>

      <h1>Scout AI</h1>

      <h2>Buy Used Tech Smarter.</h2>

      <p>

        Upload a Facebook Marketplace screenshot and receive an AI-powered
        purchase analysis before contacting the seller.

      </p>

      <div className="upload-card">

        <div className="upload-icon">

          🔍

        </div>

        <h3 style={{ marginBottom: "10px" }}>

          Upload Marketplace Screenshot

        </h3>

        <p style={{ marginTop: 0 }}>

          Drag & Drop or click below to browse

        </p>

        <input

          type="file"

          accept="image/*"

          onChange={(e) => {

            handleUpload(e);

          }}

        />

        <div className="supported-products">

          <h3>

            Version 1 Supported Products

          </h3>

          <ul>

            <li>📱 iPhone</li>

            <li>💻 MacBook</li>

            <li>🎮 PlayStation</li>

            <li>📱 Samsung Galaxy</li>

            <li>⌚ Apple Watch</li>

            <li>🎧 AirPods</li>

          </ul>

        </div>

      </div>

    </>

  );

}

export default Landing;