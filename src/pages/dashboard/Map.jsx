import 'mapbox-gl/dist/mapbox-gl.css';
import { useState } from 'react';
import Map, { Marker, NavigationControl, Popup } from 'react-map-gl';
import locationIcon from 'src/assets/images/icons/location.svg'; // Import your SVG icon

const MAPBOX_TOKEN = 'pk.eyJ1IjoicGF0aXdhdC1qdW1zaWwwNSIsImEiOiJjbTBpMmkzaXEwaTZ1MmtvbTFseTZucnFyIn0.1Ca7HKT3rotKyqN171kL3A';

// Northern rain station data
const northernRainStations = [
  { id: 1, name: '300201-แม่ฮ่องสอน จ.แม่ฮ่องสอน', latitude: 19.2998309, longitude: 97.9727042 },
  { id: 2, name: '300202-แม่สะเรียง จ.แม่ฮ่องสอน', latitude: 18.176337999999987, longitude: 97.93079749999998 },
  { id: 3, name: '303201-เชียงราย จ.เชียงราย', latitude: 19.96143679999998, longitude: 99.88151050000002 },
  { id: 4, name: '303301-เชียงราย สกษ. จ.เชียงราย', latitude: 19.85937730000001, longitude: 99.77436599999999 },
  { id: 5, name: '310201-พะเยา จ.พะเยา', latitude: 19.193108400000007, longitude: 99.88365150000003 },
  { id: 6, name: '327301-แม่โจ้ สกษ. จ.เชียงใหม่', latitude: 18.906795100000004, longitude: 99.0051879 },
  { id: 7, name: '327501-เชียงใหม่ จ.เชียงใหม่', latitude: 18.77137420000001, longitude: 98.9692197 },
  { id: 8, name: '328201-ลำปาง จ.ลำปาง', latitude: 18.278367700000025, longitude: 99.50654250000001 },
  { id: 9, name: '328301-ลำปาง สกษ. จ.ลำปาง', latitude: 18.3258388888889, longitude: 99.30154444444443 },
  { id: 10, name: '329201-ลำพูน จ.ลำพูน', latitude: 18.5666311, longitude: 99.03847839999999 },
  { id: 11, name: '330201-แพร่ จ.แพร่', latitude: 18.12877699999999, longitude: 100.16234579999998 },
  { id: 12, name: '331201-น่าน จ.น่าน', latitude: 18.767119399999974, longitude: 100.7635503 },
  { id: 13, name: '331301-น่าน สกษ. จ.น่าน', latitude: 18.86360199999999, longitude: 100.74175699999998 },
  { id: 14, name: '331401-ท่าวังผา จ.น่าน', latitude: 19.123156300000012, longitude: 100.8133438 },
  { id: 15, name: '331402-ทุ่งช้าง จ.น่าน', latitude: 19.408473800000003, longitude: 100.88256119999997 },
  { id: 16, name: '351201-อุตรดิตถ์ จ.อุตรดิตถ์', latitude: 17.62465, longitude: 100.0969889 },
  { id: 17, name: '373201-สุโขทัย จ.สุโขทัย', latitude: 17.107038699999993, longitude: 99.80028749999998 },
  { id: 18, name: '373301-ศรีสำโรง สกษ. จ.สุโขทัย', latitude: 17.16136050000001, longitude: 99.86169329999998 },
  { id: 19, name: '376201-ตาก จ.ตาก', latitude: 16.879968100000003, longitude: 99.1403971 },
  { id: 20, name: '376202-แม่สอด จ.ตาก', latitude: 16.702767299999998, longitude: 98.5418696 },
  { id: 21, name: '376203-เขื่อนภูมิพล จ.ตาก', latitude: 17.243999499999997, longitude: 99.0023395 },
  { id: 22, name: '376301-ดอยมูเซอร์ สกษ. จ.ตาก', latitude: 16.752454900000004, longitude: 98.93555209999998 },
  { id: 23, name: '376401-อุ้มผาง จ.ตาก', latitude: 16.02567790000002, longitude: 98.85978689999996 },
  { id: 24, name: '378201-พิษณุโลก จ.พิษณุโลก', latitude: 16.796090700000004, longitude: 100.27659579999998 },
  { id: 25, name: '379201-เพชรบูรณ์ จ.เพชรบูรณ์', latitude: 16.434612599999987, longitude: 101.1520701 },
  { id: 26, name: '379401-หล่มสัก จ.เพชรบูรณ์', latitude: 16.773966800000004, longitude: 101.24527260000002 },
  { id: 27, name: '379402-วิเชียรบุรี จ.เพชรบูรณ์', latitude: 15.656986600000009, longitude: 101.10556869999998 },
  { id: 28, name: '380201-กำแพงเพชร จ.กำแพงเพชร', latitude: 16.486695499999993, longitude: 99.52690690000003 },
  { id: 29, name: '386301-พิจิตร สกษ. จ.พิจิตร', latitude: 16.338582600000016, longitude: 100.3671231 },
  { id: 30, name: '327202-ดอยอ่างขาง จ.เชียงใหม่', latitude: 19.93279550000003, longitude: 99.04536520000002 },
  { id: 31, name: '328202-เถิน จ.ลำปาง', latitude: 17.636657100000022, longitude: 99.24480409999998 }
];

const MapboxComponent = () => {
  const [viewState, setViewState] = useState({
    latitude: 17.9883,
    longitude: 98.9817,
    zoom: 6.7
  });

  const [hoverInfo, setHoverInfo] = useState(null);

  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <Map
        {...viewState}
        onMove={(evt) => setViewState(evt.viewState)}
        mapboxAccessToken={MAPBOX_TOKEN}
        mapStyle="mapbox://styles/mapbox/streets-v11"
      >
        <NavigationControl position="top-right" />

        {northernRainStations.map((station) => (
          <Marker key={station.id} latitude={station.latitude} longitude={station.longitude} offsetLeft={-20} offsetTop={-40}>
            <div
              onMouseEnter={() => setHoverInfo(station)}
              onMouseLeave={() => setHoverInfo(null)}
              style={{ cursor: 'pointer' }} // เปลี่ยนรูปแบบเมาส์
            >
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
