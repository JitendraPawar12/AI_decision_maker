import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000/api";

export async function compareProduct(product) {
  const response = await axios.post(`${BASE_URL}/compare`, { product });
  return response.data;
}
