import 'mapbox-gl/dist/mapbox-gl.css';
import { useEffect, useState } from 'react';
import Map, { Marker, NavigationControl, Popup } from 'react-map-gl';
import locationIcon from 'src/assets/images/icons/location.svg';

const MAPBOX_TOKEN = 'pk.eyJ1IjoicGF0aXdhdC1qdW1zaWwwNSIsImEiOiJjbTBpMmkzaXEwaTZ1MmtvbTFseTZucnFyIn0.1Ca7HKT3rotKyqN171kL3A';

const MapboxComponent = () => {
  const [viewState, setViewState] = useState({
    latitude: 17.9883,
    longitude: 98.9817,
    zoom: 6.7
  });

  const [hoverInfo, setHoverInfo] = useState(null);
  const [northernRainStations, setNorthernRainStations] = useState([]);

  useEffect(() => {
    // Load data from JSON file
    import('/src/assets/northernRainStations.json')
      .then((data) => setNorthernRainStations(data.default))
      .catch((error) => console.error('Failed to load station data:', error));
  }, []);

  return (
    <div style={{ width: '100%', height: '100vh', borderRadius: '7px', overflow: 'hidden' }}>
      <Map
        {...viewState}
        onMove={(evt) => setViewState(evt.viewState)}
        mapboxAccessToken={MAPBOX_TOKEN}
        mapStyle="mapbox://styles/mapbox/streets-v11"
      >
        <NavigationControl position="top-right" />

        {northernRainStations.map((station) => (
          <Marker key={station.id} latitude={station.latitude} longitude={station.longitude} offsetLeft={-20} offsetTop={-40}>
            <div onMouseEnter={() => setHoverInfo(station)} onMouseLeave={() => setHoverInfo(null)} style={{ cursor: 'pointer' }}>
              <img src={locationIcon} alt={station.name} style={{ width: '20px', height: '20px' }} />
            </div>
          </Marker>
        ))}

        {hoverInfo && (
          <Popup latitude={hoverInfo.latitude} longitude={hoverInfo.longitude} closeButton={false} closeOnClick={false} anchor="top">
            <div>{hoverInfo.name}</div>
          </Popup>
        )}
      </Map>
    </div>
  );
};

export default MapboxComponent;
