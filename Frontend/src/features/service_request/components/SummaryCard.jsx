const SummaryCard = (props) => {
  return (
    <div className="summary-card">

      <h3>{props.title}</h3>

      <h1>{props.value}</h1>

      <p>{props.subtitle}</p>

    </div>
  );
};

export default SummaryCard;