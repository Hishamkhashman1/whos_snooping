import { useEffect, useState } from "react";

const emptyState = {
  subnet: "",
  devices: [],
};

export default function App() {
  const [data, setData] = useState(emptyState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [lastScan, setLastScan] = useState("");

  const runScan = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/scan");
      if (!res.ok) {
        const detail = await res.json().catch(() => ({}));
        throw new Error(detail.detail || "Scan failed");
      }
      const json = await res.json();
      setData(json);
      setLastScan(new Date().toLocaleString());
    } catch (err) {
      setError(err.message || "Scan failed");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runScan();
  }, []);

  return (
    <div className="page">
      <header className="hero">
        <div>
          <h1>Who's Snooping</h1>
          <p>See every device currently connected to your network.</p>
        </div>
        <button className="scan-btn" onClick={runScan} disabled={loading}>
          {loading ? "Scanning..." : "Scan Now"}
        </button>
      </header>

      <section className="meta">
        <div>
          <span className="label">Subnet</span>
          <span className="value">{data.subnet || "—"}</span>
        </div>
        <div>
          <span className="label">Last Scan</span>
          <span className="value">{lastScan || "—"}</span>
        </div>
        <div>
          <span className="label">Devices</span>
          <span className="value">{data.devices.length}</span>
        </div>
      </section>

      {error ? (
        <div className="error">{error}</div>
      ) : (
        <section className="table">
          <div className="row header">
            <span>IP</span>
            <span>MAC</span>
            <span>Vendor</span>
            <span>Hostname</span>
          </div>
          {data.devices.map((device) => (
            <div className="row" key={`${device.ip}-${device.mac}`}>
              <span>{device.ip}</span>
              <span>{device.mac}</span>
              <span>{device.vendor || "Unknown"}</span>
              <span>{device.hostname || "—"}</span>
            </div>
          ))}
          {data.devices.length === 0 && (
            <div className="empty">No devices found.</div>
          )}
        </section>
      )}
    </div>
  );
}
