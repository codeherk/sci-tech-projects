const MicrosatelliteForm = ({ formData, setFormData, onSubmit }) => {
    const handleChange = (event) => {
        const { name, value } = event.target;
        console.log(name,value);
        setFormData((prevData) => ({ ...prevData, [name]: value }));
    };
  
    return (
        <form onSubmit={onSubmit}>
        <div className="mb-4">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="name">
            Name
            </label>
            <input
            className="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="name"
            name="name"
            type="text"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            required
            />
        </div>
        <div className="mb-4">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="repeatNumber">
            Repeat Number
            </label>
            <input
            className="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="repeatNumber"
            name="repeatNumber"
            type="number"
            placeholder="Repeat Number"
            value={formData.repeatNumber}
            onChange={handleChange}
            required
            />
        </div>
        <div className="mb-4">
            <label className="block text-gray-700 font-bold mb-2" htmlFor="base">
            Base
            </label>
            <input
            className="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="base"
            name="base"
            type="text"
            placeholder="Base"
            value={formData.base}
            onChange={handleChange}
            required
            />
        </div>
        <div className="flex items-center justify-between">
            <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
            >
            Submit
            </button>
        </div>
        </form>
    );
};

export default MicrosatelliteForm;
