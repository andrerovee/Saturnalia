import { useState, useEffect } from "react";
import './App.css';


function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [color, setColor] = useState("");

  // Recuperiamo tutti gli items dal backend
  const fetchItems = () => {
    fetch("http://127.0.0.1:8000/items")
      .then(res => res.json())
      .then(setItems)
      .catch(console.error);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const createItem = () => {
    if (!name || !price) return;

    fetch("http://127.0.0.1:8000/items", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, price: parseFloat(price), color }),
    })
      .then(() => {
        setName("");
        setPrice("");
        setColor("");
        fetchItems();
      })
      
  };

  const deleteItem = (item_id) => {
    fetch(`http://127.0.0.1:8000/items/${item_id}`, { method: "DELETE" })
      .then(() => fetchItems())
      .catch(console.error);
  };

  return (
    <div className="App">
      <h1>Items</h1>

      <div className="input-container" >
        <input placeholder="Nome" value={name} onChange={e => setName(e.target.value)}/>
        <input placeholder="Prezzo" type="number" value={price} onChange={e => setPrice(e.target.value)} />
        <input placeholder="Colore" value={color} onChange={e => setColor(e.target.value)} />
        <button onClick={createItem}>Aggiungi</button>
      </div>

      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} - {item.price}€ {item.color && `(${item.color})`}
            <button onClick={() => deleteItem(item.id)}>Elimina</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
