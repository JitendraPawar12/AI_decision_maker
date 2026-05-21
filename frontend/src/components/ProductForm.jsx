export default function ProductForm({ product, onProductChange, onSubmit, loading }) {
  return (
    <form onSubmit={onSubmit} className="product-form">
      <label htmlFor="product" className="form-label">
        Enter product name
      </label>
      <input
        id="product"
        type="text"
        value={product}
        onChange={onProductChange}
        placeholder="e.g. iPhone 15"
        className="text-input"
      />
      <button type="submit" disabled={loading} className="submit-button">
        {loading ? "Checking..." : "Get Recommendation"}
      </button>
    </form>
  );
}
