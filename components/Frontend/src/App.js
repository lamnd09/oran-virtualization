import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';

function App() {
  const [times, setTimes] = useState([]);
  const [bandwidths, setBandwidths] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await fetch("/api/metrics");
      const data = await res.json();
      // Extract time and bandwidth
      const t = data.map(d => new Date(d.timestamp));
      const bw = data.map(d => d.ue_bandwidth);
      setTimes(t);
      setBandwidths(bw);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const chartData = {
    labels: times.map(time => time.toLocaleTimeString()),
    datasets: [{
      label: 'UE Bandwidth (Mbps)',
      data: bandwidths,
      fill: false,
      borderColor: 'blue'
    }]
  };

  return (
    <div style={{width: '600px', margin: '50px auto'}}>
      <h1>UE Bandwidth Over Time</h1>
      <Line data={chartData}/>
    </div>
  );
}

export default App;
