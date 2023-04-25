function MicrosatelliteCard({ microsatellite }) {
    return (
      <div className="bg-white overflow-hidden shadow rounded-sm">
        <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-bold leading-6 text-gray-900">{microsatellite.name}</h3>
            <p className="mt-1 text-sm text-gray-500">{microsatellite.base.repeat(microsatellite.repeats)}</p>
        </div>
        <div className="flex items-center justify-between py-2 bg-gray-200">
            <p className="text-start ml-6 text-sm  text-gray-500">({microsatellite.base}){microsatellite.repeats}</p>
            <p className="text-end mr-6 text-sm text-gray-500">ID: {microsatellite.id}</p>
        </div>
      </div>
    );
  }
  
  export default MicrosatelliteCard;
  