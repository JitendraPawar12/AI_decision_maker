import axios from "axios";

const DEFAULT_BACKEND_URL = "http://localhost:8000/api";
const FALLBACK_BACKEND_URL = "http://127.0.0.1:8001/api";
const BASE_URL = import.meta.env.VITE_BACKEND_URL || DEFAULT_BACKEND_URL;

export async function compareProduct(product) {
  try {
    const response = await axios.post(`${BASE_URL}/compare`, { product }, { timeout: 60000 });
    return response.data;
  } catch (error) {
    if (BASE_URL !== FALLBACK_BACKEND_URL) {
      const response = await axios.post(`${FALLBACK_BACKEND_URL}/compare`, { product }, { timeout: 60000 });
      return response.data;
    }
    throw error;
  }
}
