import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();
  const [cremae, setCremae] = useState(null);
  const [crepag, setCrepag] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");
    fetchMetrics(token);
  }, []);

  const fetchMetrics = async (token) => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/metrics/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMetrics(res.data);
    } catch (err) {
      console.error("Error cargando métricas");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("cremae", cremae);
    formData.append("crepag", crepag);

    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/files/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      setMensaje(res.data.mensaje);
      setError("");
      fetchMetrics(localStorage.getItem("token"));
    } catch (err) {
      setError(err.response?.data?.error || "Error al subir archivos");
      setMensaje("");
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-4xl font-bold text-center mb-10">
        Panel de Administración
      </h1>

      <form
        className="bg-gray-800 p-8 rounded-lg shadow-lg max-w-xl mx-auto mb-12"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl font-semibold text-center mb-6">
          Subida de archivos DBF
        </h2>

        <div className="space-y-4">
          <input
            type="file"
            className="block w-full text-black"
            onChange={(e) => setCremae(e.target.files[0])}
          />
          <input
            type="file"
            className="block w-full text-black"
            onChange={(e) => setCrepag(e.target.files[0])}
          />
          <button className="bg-blue-600 hover:bg-blue-700 p-3 rounded w-full transition duration-200">
            Subir archivos
          </button>
          {mensaje && <p className="text-green-400">{mensaje}</p>}
          {error && <p className="text-red-400">{error}</p>}
        </div>
      </form>

      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <MetricCard
            title="Cantidad Créditos"
            value={metrics.cantidad_creditos}
            color="green"
          />
          <MetricCard
            title="Importe Créditos"
            value={`$${metrics.importe_creditos}`}
            color="blue"
          />
          <MetricCard
            title="Pagado"
            value={`$${metrics.pagado_creditos}`}
            color="purple"
          />
          <MetricCard
            title="Deuda Total"
            value={`$${metrics.deuda_creditos}`}
            color="yellow"
          />
          <MetricCard
            title="Créditos Atrasados"
            value={metrics.creditos_atrasados}
            color="red"
          />
          <MetricCard
            title="Importe Atrasado"
            value={`$${metrics.importe_atrasado}`}
            color="pink"
          />
          <MetricCard
            title="Tasa Recuperación"
            value={`${metrics.tasa_recuperacion}%`}
            color="cyan"
          />
          <MetricCard
            title="Clientes Pagadores"
            value={metrics.clientes_pagadores}
            color="emerald"
          />
          <MetricCard
            title="Clientes Remolones"
            value={metrics.clientes_remolones}
            color="amber"
          />
          <MetricCard
            title="Clientes Malos"
            value={metrics.clientes_malos}
            color="rose"
          />
          <MetricCard
            title="Tasa Reincidencia"
            value={`${metrics.tasa_reincidencia}%`}
            color="fuchsia"
          />
        </div>
      )}
    </div>
  );
}

function MetricCard({ title, value, color }) {
  return (
    <div
      className={`bg-${color}-600 p-6 rounded-lg shadow-lg transition duration-200`}
    >
      <h2 className="text-lg font-semibold mb-2">{title}</h2>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}
