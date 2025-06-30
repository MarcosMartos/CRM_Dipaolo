import { useEffect, useState } from "react";
import api from "../api";
// Componentes de react-chartjs-2
import { Bar, Pie } from "react-chartjs-2";

// Elementos y escalas de Chart.js
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

// Registrar los componentes de Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
);

export default function Metrics() {
  const [clientes, setClientes] = useState(null);
  const [creditos, setCreditos] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [resClientes, resCreditos] = await Promise.all([
          api.get("/api/metrics/clientes"),
          api.get("/api/metrics/creditos"),
        ]);
        setClientes(resClientes.data);
        setCreditos(resCreditos.data);
      } catch {
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <p className="text-gray-500">Cargando métricas...</p>;

  // Preparar datos para los gráficos
  const barData = {
    labels: Object.keys(clientes),
    datasets: [
      {
        label: "Cantidad",
        data: Object.values(clientes).map((v) =>
          typeof v === "object" ? v.cantidad : v
        ),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };

  const pieData = {
    labels: Object.keys(creditos),
    datasets: [
      {
        label: "Porcentaje",
        data: Object.values(creditos).map((v) =>
          typeof v === "object" ? v.porcentaje : v
        ),
        backgroundColor: ["#f87171", "#34d399", "#60a5fa", "#fbbf24"],
      },
    ],
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Panel de métricas</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white p-6 rounded shadow">
            <Bar
              data={barData}
              options={{
                responsive: true,
                plugins: { legend: { position: "top" } },
              }}
            />
          </div>
          <div className="bg-white p-6 rounded shadow">
            <Pie
              data={pieData}
              options={{
                responsive: true,
                plugins: { legend: { position: "bottom" } },
              }}
            />
          </div>
        </div>
        <div className="space-y-6">
          <Card title="Clientes" data={clientes} />
          <Card title="Créditos" data={creditos} />
        </div>
      </div>
    </div>
  );
}

function Card({ title, data }) {
  if (!data || Object.keys(data).length === 0)
    return (
      <div className="bg-white p-6 rounded shadow text-gray-500">
        No hay datos disponibles
      </div>
    );

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      <ul className="space-y-4">
        {Object.entries(data).map(([key, value]) => (
          <li key={key}>
            <p className="font-medium capitalize text-gray-700 mb-1">
              {key.replaceAll("_", " ")}:
            </p>
            {typeof value === "object" ? (
              <ul className="pl-4 text-sm text-gray-600 list-disc">
                {Object.entries(value).map(([subKey, subValue]) => (
                  <li key={subKey}>
                    {subKey}:{" "}
                    <span className="font-semibold">
                      {subKey.includes("porcentaje")
                        ? `${subValue.toFixed(2)}%`
                        : subValue}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <span className="font-semibold text-gray-800">{value}</span>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
