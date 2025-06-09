import { useState } from "react";
import { registerUser } from "../api/Api.jsx";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ nombre: "", email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUser({ ...form, rol: "admin" }); // solo admin por ahora
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.error || "Error al registrar");
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex justify-center items-center">
      <form className="bg-gray-800 p-8 rounded" onSubmit={handleSubmit}>
        <h2 className="text-2xl mb-4 font-bold">Registro</h2>
        <input
          className="mb-2 p-2 w-full text-black"
          name="nombre"
          placeholder="Nombre"
          onChange={handleChange}
        />
        <input
          className="mb-2 p-2 w-full text-black"
          name="email"
          placeholder="Email"
          onChange={handleChange}
        />
        <input
          className="mb-2 p-2 w-full text-black"
          name="password"
          placeholder="Password"
          type="password"
          onChange={handleChange}
        />
        {error && <p className="text-red-500">{error}</p>}
        <button className="bg-blue-600 w-full p-2 rounded">Registrarse</button>
      </form>
    </div>
  );
}
