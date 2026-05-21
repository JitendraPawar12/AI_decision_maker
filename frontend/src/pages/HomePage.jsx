import { useState } from "react";
import ProductForm from "../components/ProductForm";
import ResultPanel from "../components/ResultPanel";
import { compareProduct } from "../api";

export default function HomePage() {
  const [product, setProduct] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!product.trim()) {
      setError("Please enter a product name.");
      return;
    }

    setLoading(true);
    try {
      const response = await compareProduct(product.trim());
      setResult(response);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setError(detail || err?.message || "Unable to fetch recommendation.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <header>
        <h1>Buy / Wait Advisor</h1>
        <p>Enter a product name to receive a BUY or WAIT recommendation backed by market data.</p>
      </header>

      <ProductForm
        product={product}
        onProductChange={(event) => setProduct(event.target.value)}
        onSubmit={handleSubmit}
        loading={loading}
      />

      {error && <p className="error-message">{error}</p>}
      <ResultPanel result={result} />
    </main>
  );
}
