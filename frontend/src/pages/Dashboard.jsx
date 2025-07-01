// src/pages/Dashboard.jsx
import { useAuth } from "../context/AuthContext";
import { Link, Outlet } from "react-router-dom";

export default function Dashboard() {
  const { logout } = useAuth();

  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-[#406B69] text-white flex flex-col p-4">
        <nav className="flex flex-col gap-2">
          <img
            className="w-32 mx-auto mb-2"
            src="../../public/loguito.webp"
            alt="logo de di paolo"
          />
          <Link to="metrics" className="hover:bg-[#2c4b49] p-2 rounded">
            Ver métricas
          </Link>
          <Link to="upload" className="hover:bg-[#213635] p-2 rounded">
            Cargar archivos
          </Link>
          <button
            onClick={logout}
            className="mt-auto bg-[#214b47] hover:bg-[#522f2f] p-2 rounded"
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
