import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"; // Import obligatorio de estilos

export default function Login() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validaciones de entrada
    if (!email.trim()) {
      toast.error("El campo de email no puede estar vacío.");
      return;
    }

    if (!email.includes("@") || !/\S+@\S+\.\S+/.test(email)) {
      toast.error("Por favor, ingresa un email válido.");
      return;
    }

    if (!password.trim()) {
      toast.error("El campo de contraseña no puede estar vacío.");
      return;
    }

    if (password.length < 6) {
      toast.error("La contraseña debe tener al menos 6 caracteres.");
      return;
    }

    // Intentar login
    try {
      await login(email, password);
      toast.success("Inicio de sesión exitoso!");
    } catch (err) {
      toast.error("Email o contraseña incorrectos.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#406B69]">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded shadow-md w-80"
      >
        {/* Contenedor de notificaciones */}
        <ToastContainer position="top-center" autoClose={3000} />

        <div>
          <img
            className="w-24 mx-auto mb-6"
            src="../../public/loguito.webp"
            alt="Logo de la empresa"
          />
        </div>
        <h2 className="text-xl font-bold mb-4">Iniciar sesión</h2>
        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 border mb-4"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          className="w-full p-2 border mb-4"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          type="submit"
          className="w-full bg-[#214b47] hover:bg-[#253f3d] text-white p-2 rounded"
        >
          Entrar
        </button>
      </form>
    </div>
  );
}
