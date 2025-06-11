import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const { token } = useAuth();

  useEffect(() => {
    if (!token) return;

    fetch("http://localhost:5000/metrics/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Error al cargar métricas");
        return res.json();
      })
      .then(setData)
      .catch(console.error);
  }, [token]);

  if (!data)
    return <div className="text-center mt-10">Cargando métricas...</div>;

  const Block = ({ title, children }) => (
    <div className="bg-white dark:bg-gray-900 rounded-2xl shadow p-6 w-full md:w-auto">
      <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-100">
        {title}
      </h3>
      <div className="space-y-1 text-sm text-gray-700 dark:text-gray-300">
        {children}
      </div>
    </div>
  );

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-800 dark:text-white">
        Dashboard de Métricas
      </h1>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        <Block title="Generales">
          <p>Cantidad total de créditos: {data.generales.cantidad_creditos}</p>
          <p>
            Importe total de créditos: $
            {data.generales.importe_total.toLocaleString()}
          </p>
        </Block>

        <Block title="Créditos Activos">
          <p>Cantidad: {data.activos.cantidad}</p>
          <p>
            Importe total: $
            {data.activos.importe_total != null
              ? data.activos.importe_total.toLocaleString()
              : "0"}
          </p>
          <p>Pagado: ${data.activos.pagado_total.toLocaleString()}</p>
          <p>Deuda: ${data.activos.deuda_total.toLocaleString()}</p>
          <p>% Pagado: {data.activos.porcentaje_pagado}%</p>
          <p>% Deuda: {data.activos.porcentaje_deuda}%</p>
        </Block>

        <Block title="Clientes por Estado">
          <p>
            Excelentes: {data.clientes.excelentes} (
            {data.clientes.porcentaje_excelentes}%)
          </p>
          <p>
            Buenos: {data.clientes.buenos} ({data.clientes.porcentaje_buenos}%)
          </p>
          <p>
            Remolones: {data.clientes.remolones} (
            {data.clientes.porcentaje_remolones}%)
          </p>
          <p>
            Malos: {data.clientes.malos} ({data.clientes.porcentaje_malos}%)
          </p>
        </Block>
      </div>
    </div>
  );
}
