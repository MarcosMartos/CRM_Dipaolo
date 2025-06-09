import { useState } from "react";
import { loginUser } from "../api/Api.jsx";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser(form);
      login(res.data.token); // Guardamos token en el context
      navigate("/dashboard");
    } catch (err) {
      setError("Credenciales inválidas");
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex justify-center items-center">
      <form className="bg-gray-800 p-8 rounded" onSubmit={handleSubmit}>
        <h2 className="text-2xl mb-4 font-bold">Login</h2>
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
        <button className="bg-green-600 w-full p-2 rounded">Ingresar</button>
      </form>
    </div>
  );
}
