export const API_BASE_URL =
  process.env.NODE_ENV === "production"
    ? "http://16.171.10.73/api/v1"
    : "http://localhost:5000/api/v1";
