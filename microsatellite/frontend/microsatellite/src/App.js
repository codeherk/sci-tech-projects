import { useState, useEffect } from "react";
import MicrosatelliteCard from "./components/MicrosatelliteCard.js";
import MicrosatelliteForm from "./components/MicrosatelliteForm";

function App() {
  const [microsatellites, setMicrosatellites] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [showForm, setShowForm] = useState(false);

  const fetchMicrosatellites = async () => {
    const res = await fetch("http://localhost:5000/microsatellites");
    const data = await res.json();
    setMicrosatellites(data);
  };

  useEffect(() => {

    fetchMicrosatellites();
  }, []);

// Define a state for the form data
const [formData, setFormData] = useState({
  name: "",
  repeatNumber: "",
  base: "",
});

// Define a function to handle form submission
const handleAddMicrosatellite = async (event) => {
  event.preventDefault();
  try {
    // Send POST request with form data
    const response = await fetch('http://localhost:5000/microsatellites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
    if (!response.ok) {
      throw new Error('Failed to add microsatellite');
    }
    // Update microsatellite list
    fetchMicrosatellites();
    // Hide the form
    setShowForm(false);
  } catch (error) {
    console.error(error);
  }
};
  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredMicrosatellites = microsatellites.filter((microsatellite) =>
    microsatellite.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-5 sm:px-6 lg:px-8">
      <div className="">
        <div className="flex items-center justify-between my-4">
          <h1 className="text-3xl font-bold">Microsatellites</h1>
          <button
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            onClick={() => setShowForm(true)}
          >
            Add Microsatellite
          </button>
        </div>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search Microsatellite"
            value={searchTerm}
            onChange={handleSearch}
            className="block w-full h-10 pl-2 sm:text-sm rounded-sm border-1 border-black "
          />
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredMicrosatellites.map((microsatellite) => (
            <MicrosatelliteCard key={microsatellite.id} microsatellite={microsatellite} />
          ))}
        </div>
      </div>
      <div className="mt-10">
        {/* // Pass down form data and functions as props to MicrosatelliteForm */}
        {showForm && <MicrosatelliteForm formData={formData} setFormData={setFormData} onSubmit={handleAddMicrosatellite} />}
      </div>
    </div>
  );
}

export default App;