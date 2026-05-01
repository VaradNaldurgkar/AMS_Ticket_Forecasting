import "../css/ChannelBreakdown.css";

export default function ChannelBreakdown({ data }) {
  return (
    <div className="ccb-breakdown">
      <h4>Channel Breakdown</h4>

      {data.map(d => (
        <div key={d.callCode} className="ccb-breakdown-row">
          <span>{d.callCode}</span>
          <span>{d.count}</span>
          <span>{d.percentage}%</span>
        </div>
      ))}
    </div>
  );
}
``