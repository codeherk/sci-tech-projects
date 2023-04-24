import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/microsatellites')
      .then(res => res.json())
      .then(data => setData(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-4">
      {data.map((item, index) => (
        <div key={index} className="mb-4 bg-gray-100 rounded-md p-4">
          <h2 className="text-lg font-medium mb-2">{item.name}</h2>
          <p className="text-gray-600 mb-1">ID: {item.id}</p>
          <p className="text-gray-600 mb-1">Base: {item.base}</p>
          <p className="text-gray-600 mb-1">Repeats: {item.repeats}</p>
          <p className="text-gray-600 mb-1">Microsatellite: {item.microsatellite}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
