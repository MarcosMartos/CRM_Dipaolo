// src/auth/auth.js

// Guardar token
export const saveToken = (token) => {
  localStorage.setItem("token", token);
};

// Obtener token
export const getToken = () => {
  return localStorage.getItem("token");
};

// Eliminar token y hacer logout
export const logout = () => {
  localStorage.removeItem("token");
  window.location.href = "/"; // Redirigir al login
};

// Verificar si está autenticado
export const isAuthenticated = () => {
  return !!getToken();
};
