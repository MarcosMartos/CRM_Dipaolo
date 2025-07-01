import { useEffect, useState } from "react";
import api from "../api";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

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
  const [view, setView] = useState("creditos");

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

  const barData = {
    labels: [
      "Importe total",
      "Importe pagado",
      "Importe atrasado",
      "Importe deuda",
    ],
    datasets: [
      {
        label: "Importe ($)",
        data: [
          creditos.importe_total_creditos_activos,
          creditos.importe_pagado_creditos_activos,
          creditos.importe_atrasado_creditos_activos,
          creditos.importe_deuda_creditos_activos,
        ],
        backgroundColor: ["#60a5fa", "#34d399", "#f87171", "#fbbf24"],
      },
    ],
  };

  const pieData = {
    labels: ["% Pagado", "% Deuda"],
    datasets: [
      {
        label: "Distribución",
        data: [
          creditos.porcentaje_pagado_creditos_activos,
          creditos.porcentaje_deuda_creditos_activos,
        ],
        backgroundColor: ["#34d399", "#f87171"],
      },
    ],
  };

  const clientesPieData = {
    labels: Object.keys(clientes),
    datasets: [
      {
        label: "% Clientes",
        data: Object.values(clientes).map((c) => c.porcentaje),
        backgroundColor: ["#60a5fa", "#34d399", "#f87171", "#fbbf24"],
      },
    ],
  };

  const clientesBarData = {
    labels: Object.keys(clientes),
    datasets: [
      {
        label: "Cantidad",
        data: Object.values(clientes).map((c) => c.cantidad),
        backgroundColor: "#406B69",
      },
    ],
  };

  const kpis = [
    {
      label: "Créditos activos",
      value: creditos.creditos_activos,
    },
    {
      label: "Cuotas totales",
      value: creditos.cuotas_totales_creditos_activos,
    },
    {
      label: "% Cuotas pagadas",
      value: `${creditos.porcentaje_cuotas_pagadas_creditos_activos.toFixed(
        2
      )}%`,
    },
    {
      label: "% Cuotas no pagadas",
      value: `${creditos.porcentaje_cuotas_no_pagadas_creditos_activos.toFixed(
        2
      )}%`,
    },
    {
      label: "% Atrasado",
      value: `${creditos.porcentaje_atrasado_creditos_activos.toFixed(2)}%`,
    },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Panel de métricas</h1>

      <div className="mb-6">
        <button
          className={`px-4 py-2 rounded mr-4 ${
            view === "creditos" ? "bg-[#406B69] text-white" : "bg-white border"
          }`}
          onClick={() => setView("creditos")}
        >
          Ver Créditos
        </button>
        <button
          className={`px-4 py-2 rounded ${
            view === "clientes" ? "bg-[#406B69] text-white" : "bg-white border"
          }`}
          onClick={() => setView("clientes")}
        >
          Ver Clientes
        </button>
      </div>

      {view === "creditos" ? (
        <>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            {kpis.map((kpi, index) => (
              <div
                key={index}
                className="bg-white p-4 rounded shadow text-center"
              >
                <p className="text-sm text-gray-500">{kpi.label}</p>
                <p className="text-lg font-bold text-[#406B69]">{kpi.value}</p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div className="bg-white p-6 rounded shadow">
              <h2 className="text-xl font-semibold mb-4">Importes</h2>
              <Bar
                data={barData}
                options={{
                  responsive: true,
                  plugins: { legend: { position: "top" } },
                }}
              />
            </div>
            <div className="bg-white p-6 rounded shadow">
              <h2 className="text-xl font-semibold mb-4">Distribución Pagos</h2>
              <Pie
                data={pieData}
                options={{
                  responsive: true,
                  plugins: { legend: { position: "bottom" } },
                }}
              />
            </div>
          </div>
        </>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-xl font-semibold mb-4">
              Distribución de Clientes
            </h2>
            <Pie
              data={clientesPieData}
              options={{
                responsive: true,
                plugins: { legend: { position: "bottom" } },
              }}
            />
          </div>
          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-xl font-semibold mb-4">Cantidad de Clientes</h2>
            <Bar
              data={clientesBarData}
              options={{
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                  y: { beginAtZero: true },
                },
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
