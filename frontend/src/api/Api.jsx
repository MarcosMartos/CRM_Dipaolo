import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5000", // URL de tu backend
});

// Agregar un interceptor para agregar el token a cada request
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Registro de usuarios
export const registerUser = (data) => API.post("/auth/register", data);

// Login de usuarios
export const loginUser = (data) => API.post("/auth/login", data);

// Ejemplo de obtener métricas protegidas
export const getMetrics = () => API.get("/metrics");
