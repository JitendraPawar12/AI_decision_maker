export default function ResultPanel({ result }) {
  if (!result) {
    return null;
  }

  return (
    <section className="result-panel">
      <h2>Recommendation</h2>
      <div className="result-card">
        <p className="decision">Decision: <strong>{result.decision}</strong></p>
        <p>Confidence: {Math.round(result.confidence * 100)}%</p>
        <p>Reason: {result.reason}</p>
        <div className="box">
          <h3>Market Maturity</h3>
          <p>Seller count: {result.market_maturity.seller_count}</p>
          <p>Listing count: {result.market_maturity.listing_count}</p>
          <p>Price spread: ${result.market_maturity.price_spread}</p>
          <p>Is mature: {result.market_maturity.is_mature ? "Yes" : "No"}</p>
        </div>
        <div className="box">
          <h3>Price Analysis</h3>
          <p>Best price: ${result.price_analysis.best_price}</p>
          <p>Average price: ${result.price_analysis.average_price}</p>
          <p>Median price: ${result.price_analysis.median_price}</p>
          <p>Price position: {result.price_analysis.price_position}</p>
        </div>
        <div className="box">
          <h3>Seller prices</h3>
          {result.listings.length > 0 ? (
            <ul className="seller-list">
              {result.listings.map((listing, index) => (
                <li key={index}>
                  <strong>{listing.seller}</strong> — ${listing.price.toFixed(2)}
                  <div className="listing-title">{listing.title}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p>No seller listings available.</p>
          )}
        </div>
        <div className="box conclusion-box">
          <h3>Final Conclusion</h3>
          <p>{result.conclusion}</p>
        </div>
        <div className="box explanation-box">
          <h3>AI Explanation</h3>
          <p>{result.explanation}</p>
        </div>
      </div>
    </section>
  );
}
