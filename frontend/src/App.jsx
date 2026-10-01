import { useState } from "react";

import "./App.css";

import Landing from "./components/Landing";
import Loading from "./components/Loading";
import Results from "./components/Results";

function App() {

  const [screen, setScreen] = useState("landing");

  const [selectedFile, setSelectedFile] = useState(null);

  const [analysis, setAnalysis] = useState(null);

  async function handleUpload(event) {

    const file = event.target.files[0];

    if (!file) return;

    setSelectedFile(file);

    setScreen("loading");

    try {

      const formData = new FormData();

      formData.append("file", file);

      const response = await fetch(

        "http://127.0.0.1:8000/analyze",

        {

          method: "POST",

          body: formData

        }

      );

      const data = await response.json();

      console.log(data);

      setAnalysis(data);

      setScreen("results");

    }

    catch (err) {

      console.error(err);

      alert("Unable to analyze screenshot.");

      setScreen("landing");

    }

  }

  return (

    <div className="app">

      {screen === "landing" && (

        <Landing handleUpload={handleUpload} />

      )}

      {screen === "loading" && (

        <Loading file={selectedFile} />

      )}

      {screen === "results" && (

        <Results

          analysis={analysis}

          onReset={() => {

            setSelectedFile(null);

            setAnalysis(null);

            setScreen("landing");

          }}

        />

      )}

    </div>

  );

}

export default App;