// src/pages/Upload.jsx
import { useState } from "react";
import { toast, ToastContainer } from "react-toastify";
import api from "../api";

export default function Upload() {
  const [cremae, setCremae] = useState(null);
  const [crepag, setCrepag] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!cremae || !crepag) {
      toast.error("Debés seleccionar ambos archivos (cremae y crepag)");
      return;
    }

    const formData = new FormData();
    formData.append("cremae", cremae);
    formData.append("crepag", crepag);

    setLoading(true);

    try {
      await api.post("/files/upload", formData);
      toast.success("Archivos cargados correctamente");

      const res = await api.post("/admin/cargar_datos");
      toast.success(
        res.data?.mensaje || "Datos cargados en la base correctamente"
      );

      setCremae(null);
      setCrepag(null);
    } catch {
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 mb-10 px-4 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold mb-6">Subir archivos DBF</h1>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center justify-center space-y-6 bg-white p-6 rounded shadow"
      >
        <div>
          <label className="block font-medium text-gray-700 mb-1">
            Archivo cremae.dbf
          </label>
          <input
            className="bg-[#eeeeee] p-2 rounded-sm"
            type="file"
            onChange={(e) => setCremae(e.target.files[0])}
          />
        </div>
        <div>
          <label className="block font-medium text-gray-700 mb-1">
            Archivo crepag.dbf
          </label>
          <input
            className="bg-[#eeeeee] p-2 rounded-sm"
            type="file"
            onChange={(e) => setCrepag(e.target.files[0])}
          />
        </div>
        <button
          type="submit"
          className="bg-[#406B69] hover:bg-[#2c4b49] text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Cargando..." : "Cargar archivos"}
        </button>
      </form>
      <ToastContainer />
    </div>
  );
}
