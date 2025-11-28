import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [terreni, setTerreni] = useState([]);

  // Campi del form
  const [codiceNome, setCodiceNome] = useState("");
  const [area, setArea] = useState("");
  const [comune, setComune] = useState("");
  const [sezione, setSezione] = useState("");
  const [foglio, setFoglio] = useState("");
  const [particella, setParticella] = useState("");
  const [superficie_m2, setSuperficie_m2] = useState("");

  // ID del terreno in fase di modifica
  const [editingId, setEditingId] = useState(null);

  // Fetch dei terreni
  const fetchTerreni = () => {
    fetch("http://127.0.0.1:8000/terreni")
      .then((res) => res.json())
      .then(setTerreni)
      .catch(console.error);
  };

  useEffect(() => {
    fetchTerreni();
  }, []);

  // Submit del form (POST o PUT)
  const handleSubmit = () => {
    if (!codiceNome || !area || !comune) return;

    const body = {
  codice_nome: codiceNome,
  comune: comune,
  area_coltivata_m2: Number(area),
  superficie_tot: Number(area),
  particelle: [
    {
      id: editingId,  // <- importantissimo
      comune: comune,
      sezione: sezione || null,
      foglio: Number(foglio),
      particella: Number(particella),
      superficie_m2: Number(superficie_m2 || area)
    },
  ],
};

    if (editingId) {
      // MODIFICA con PUT
      fetch(`http://127.0.0.1:8000/terreni/${editingId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      })
        .then(() => {
          fetchTerreni();
          setEditingId(null);
        })
        .catch(console.error);
    } else {
      // CREAZIONE con POST
      fetch("http://127.0.0.1:8000/terreni", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      })
        .then(() => fetchTerreni())
        .catch(console.error);
    }

    resetForm();
  };

  const resetForm = () => {
    setCodiceNome("");
    setArea("");
    setComune("");
    setSezione("");
    setFoglio("");
    setParticella("");
    setSuperficie_m2("");
  };

  // Inizia modifica
  const startEditing = (t, p = null) => {
    setEditingId(t.id);
    setCodiceNome(t.codice_nome);
    setArea(t.area_coltivata_m2);
    setComune(p?.comune || t.comune);
    setSezione(p?.sezione || "");
    setFoglio(p?.foglio || "");
    setParticella(p?.particella || "");
    setSuperficie_m2(p?.superficie_m2 || t.area_coltivata_m2);
  };

  // DELETE
  const delete_terreno = (id) => {
    fetch(`http://127.0.0.1:8000/terreni/${id}`, {
      method: "DELETE",
    })
      .then(() => fetchTerreni())
      .catch(console.error);
  };

  return (
    <div className="App">
      <h1>{editingId ? "Modifica Terreno" : "Aggiungi Terreno"}</h1>

      <div className="input-container">
        <input placeholder="Codice nome" value={codiceNome} onChange={(e) => setCodiceNome(e.target.value)} />
        <input placeholder="Area" type="number" value={area} onChange={(e) => setArea(e.target.value)} />

        <h3>Particella</h3>
        <input placeholder="Comune" value={comune} onChange={(e) => setComune(e.target.value)} />
        <input placeholder="Sezione" value={sezione} onChange={(e) => setSezione(e.target.value)} />
        <input placeholder="Foglio" type="number" value={foglio} onChange={(e) => setFoglio(e.target.value)} />
        <input placeholder="Particella" type="number" value={particella} onChange={(e) => setParticella(e.target.value)} />
        <input placeholder="Superficie totale" type="number" value={superficie_m2} onChange={(e) => setSuperficie_m2(e.target.value)} />

        <button onClick={handleSubmit}>{editingId ? "Salva Modifica" : "Aggiungi Terreno"}</button>
      </div>

      <div style={{ padding: "20px" }}>
        <h1>Lista Terreni</h1>
        {terreni.length === 0 ? (
          <p>Nessun terreno trovato.</p>
        ) : (
          <table border="1" cellPadding="5" style={{ borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Codice Nome</th>
                <th>Area Coltivata (m²)</th>
                <th>Comune</th>
                <th>Sezione</th>
                <th>Foglio</th>
                <th>Particella</th>
                <th>Superficie totale (m²)</th>
                <th>Azioni</th>
              </tr>
            </thead>
            <tbody>
              {terreni.map((t) =>
                t.particelle?.length > 0 ? (
                  t.particelle.map((p) => (
                    <tr key={`row-${t.id}-${p.id}`}>
                      <td>{t.id}</td>
                      <td>{t.codice_nome}</td>
                      <td>{t.area_coltivata_m2}</td>
                      <td>{t.comune}</td>
                      <td>{p.sezione || "-"}</td>
                      <td>{p.foglio}</td>
                      <td>{p.particella}</td>
                      <td>{p.superficie_m2}</td>
                      <td>
                        <button onClick={() => startEditing(t, p)}>Modifica</button>
                        <button onClick={() => delete_terreno(t.id)}>Elimina</button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr key={`row-${t.id}`}>
                    <td>{t.id}</td>
                    <td>{t.codice_nome}</td>
                    <td>{t.area_coltivata_m2}</td>
                    <td>{t.comune}</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>-</td>
                    <td>
                      <button onClick={() => startEditing(t)}>Modifica</button>
                      <button onClick={() => delete_terreno(t.id)}>Elimina</button>
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;

