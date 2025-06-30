// src/api.js
import axios from "axios";
import { toast } from "react-toastify";

const api = axios.create({
  baseURL: "http://localhost:5000",
});

// Inyectar token si existe
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Manejo de errores
api.interceptors.response.use(
  (res) => res,
  (error) => {
    const msg = error.response?.data?.error || "Error del servidor";
    toast.error(msg);
    return Promise.reject(error);
  }
);

export default api;
