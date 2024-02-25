export const API_BASE_URL =
  process.env.NODE_ENV === "production"
    ? "http://3.8.144.109/api/v1"
    : "http://localhost:8080/api/v1";
