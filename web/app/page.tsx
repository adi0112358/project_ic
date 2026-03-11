import Link from "next/link";

export default function HomePage() {
  return (
    <section>
      <div className="hero">
        <div>
          <div className="badge">Decision-support only</div>
          <h1>Fungal infection risk analysis for people with type 2 diabetes.</h1>
          <p>
            Upload your lab report and a skin image to get a structured assessment of diabetes status,
            fungal infection likelihood, type, and severity. Results are grounded in your data and
            explained in plain language.
          </p>
          <div className="cta-row">
            <Link className="button" href="/upload">Start analysis</Link>
            <Link className="button secondary" href="/chat">Ask the assistant</Link>
          </div>
        </div>
        <div>
          <div className="card">
            <h3>What this does</h3>
            <p>Parses key lab markers, reviews skin images, and fuses evidence into a single report.</p>
          </div>
          <div className="card" style={{ marginTop: 12 }}>
            <h3>What this does not</h3>
            <p>No prescriptions or diagnoses. Always confirm with a clinician.</p>
          </div>
        </div>
      </div>

      <div className="card-grid">
        <div className="card">
          <h3>Report extraction</h3>
          <p>OCR-ready pipeline turns reports into structured lab values for modeling.</p>
        </div>
        <div className="card">
          <h3>Image analysis</h3>
          <p>Classifies likely fungal type and flags image quality issues.</p>
        </div>
        <div className="card">
          <h3>Fusion scoring</h3>
          <p>Combines labs and image cues into a calibrated risk score.</p>
        </div>
        <div className="card">
          <h3>Chat assistant</h3>
          <p>Explains results, highlights risk, and suggests next steps.</p>
        </div>
      </div>
    </section>
  );
}
