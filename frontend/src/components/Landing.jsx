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


        {/* UPLOAD ICON */}

        <div
          className="upload-icon"
          style={{
            fontSize: "58px",
            lineHeight: "1",
            marginBottom: "22px"
          }}
        >
          🔍
        </div>


        {/* UPLOAD TITLE */}

        <h3
          style={{
            marginTop: 0,
            marginBottom: "10px"
          }}
        >
          Upload Marketplace Screenshot
        </h3>


        {/* UPLOAD INSTRUCTIONS */}

        <p
          style={{
            marginTop: 0,
            marginBottom: "12px"
          }}
        >
          Drag & Drop or click below to browse
        </p>


        {/* FILE INPUT */}

        <input
          type="file"
          accept="image/*"
          onChange={(e) => {
            handleUpload(e);
          }}
        />


        {/* SUPPORTED PRODUCTS */}

        <div className="supported-products">

          <h3>
            Version 1 Supported Products
          </h3>

          <ul>

            <li>
              📱 Phones
            </li>

            <li>
              💻 Laptops & Tablets
            </li>

            <li>
              🎮 Gaming Consoles
            </li>

          </ul>

        </div>


      </div>

    </>

  );

}

export default Landing;