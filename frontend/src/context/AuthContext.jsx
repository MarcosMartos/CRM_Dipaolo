import { createContext, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { toast } from "react-toastify";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const login = async (email, password) => {
    try {
      const res = await api.post("/auth/login", { email, password });
      const token = res.data.token;
      localStorage.setItem("token", token);

      // Opcional: decodificar el token para mostrar nombre de usuario
      const payload = JSON.parse(atob(token.split(".")[1]));
      setUser({ email: payload.sub });

      toast.success("Login exitoso");
      navigate("/dashboard");
    } catch (err) {
      toast.error("Credenciales inválidas");
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
