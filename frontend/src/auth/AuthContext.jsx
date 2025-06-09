import { createContext, useState, useEffect, useContext } from "react";
import { getToken, saveToken, logout as logoutFn } from "./Auth.jsx";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = getToken();
    setIsAuthenticated(!!token);
  }, []);

  const login = (token) => {
    saveToken(token);
    setIsAuthenticated(true);
  };

  const logout = () => {
    logoutFn(); // elimina el token y redirige
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
