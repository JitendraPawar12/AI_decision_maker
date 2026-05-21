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
        {result.sale_event && (
          <div className="box sale-box">
            <h3>Upcoming sale alert</h3>
            <p>{result.sale_event}</p>
          </div>
        )}
        {result.major_site_listings && result.major_site_listings.length > 0 && (
          <div className="box major-site-box">
            <h3>Amazon/Flipkart/Other Indian store offers</h3>
            <p>Direct online store listings from major Indian marketplaces:</p>
            <ul className="seller-list">
              {result.major_site_listings.map((listing, index) => (
                <li key={`major-${index}`}>
                  <strong>{listing.site}</strong> — {listing.seller} — ${listing.price.toFixed(2)}
                  <div className="listing-title">{listing.title}</div>
                  {listing.link && (
                    <div className="listing-link">
                      <a href={listing.link} target="_blank" rel="noreferrer">View offer</a>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
        {result.local_market_listings && result.local_market_listings.length > 0 && (
          <div className="box local-market-box">
            <h3>Other Indian marketplace offers</h3>
            <p>Local marketplace listings from Facebook, OLX, Quikr, or similar sellers:</p>
            <ul className="seller-list">
              {result.local_market_listings.map((listing, index) => (
                <li key={`local-${index}`}>
                  <strong>{listing.site}</strong> — {listing.seller} — ${listing.price.toFixed(2)}
                  <div className="listing-title">{listing.title}</div>
                  {listing.link && (
                    <div className="listing-link">
                      <a href={listing.link} target="_blank" rel="noreferrer">View offer</a>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
        {result.other_listings && result.other_listings.length > 0 && (
          <div className="box fallback-box">
            <h3>Fallback offers</h3>
            <p>Other relevant offers prioritized after major Indian stores:</p>
            <ul className="seller-list">
              {result.other_listings.map((listing, index) => (
                <li key={`other-${index}`}>
                  <strong>{listing.site}</strong> — {listing.seller} — ${listing.price.toFixed(2)}
                  <div className="listing-title">{listing.title}</div>
                  {listing.link && (
                    <div className="listing-link">
                      <a href={listing.link} target="_blank" rel="noreferrer">View offer</a>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
        {!(result.major_site_listings?.length > 0 || result.local_market_listings?.length > 0 || result.other_listings?.length > 0) && (
          <div className="box">
            <h3>Seller prices</h3>
            {result.listings.length > 0 ? (
              <ul className="seller-list">
                {result.listings.map((listing, index) => (
                  <li key={index}>
                    <strong>{listing.seller}</strong> ({listing.site}) — ${listing.price.toFixed(2)}
                    <div className="listing-title">{listing.title}</div>
                    {listing.link && (
                      <div className="listing-link">
                        <a href={listing.link} target="_blank" rel="noreferrer">View offer</a>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No seller listings available.</p>
            )}
          </div>
        )}
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
