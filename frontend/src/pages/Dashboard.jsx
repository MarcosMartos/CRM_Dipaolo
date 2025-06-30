// src/pages/Dashboard.jsx
import { useAuth } from "../context/AuthContext";
import { Link, Outlet } from "react-router-dom";

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-gray-800 text-white flex flex-col p-4">
        <h2 className="text-xl font-bold mb-6">Hola, {user?.nombre}</h2>
        <nav className="flex flex-col gap-2">
          <Link to="metrics" className="hover:bg-gray-700 p-2 rounded">
            Ver métricas
          </Link>
          <Link to="upload" className="hover:bg-gray-700 p-2 rounded">
            Cargar archivos
          </Link>
          <button
            onClick={logout}
            className="mt-auto bg-red-500 hover:bg-red-600 p-2 rounded"
          >
            Salir
          </button>
        </nav>
      </aside>

      <main className="flex-1 p-6 overflow-y-auto bg-gray-50">
        <Outlet />
      </main>
    </div>
  );
}
