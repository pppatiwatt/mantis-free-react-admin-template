// material-ui
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputAdornment from '@mui/material/InputAdornment';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import OutlinedInput from '@mui/material/OutlinedInput';

// assets
import SearchOutlined from '@ant-design/icons/SearchOutlined';
import { useEffect, useRef, useState } from 'react';

// ==============================|| HEADER CONTENT - SEARCH ||============================== //

export default function Search() {
  const [searchTerm, setSearchTerm] = useState('');
  const [northernRainStations, setNorthernRainStations] = useState([]);
  const [filteredStations, setFilteredStations] = useState([]);

  const inputRef = useRef(null); // สร้าง ref เพื่อเก็บ reference ของ input

  useEffect(() => {
    // Load data from JSON file
    import('/src/assets/northernRainStations.json')
      .then((data) => {
        setNorthernRainStations(data.default);
      })
      .catch((error) => console.error('Failed to load station data:', error));
  }, []);

  useEffect(() => {
    // Filter stations based on search term
    if (searchTerm) {
      setFilteredStations(northernRainStations.filter((station) => station.name.toLowerCase().includes(searchTerm.toLowerCase())));
    } else {
      setFilteredStations([]); // Clear filtered stations if search is empty
    }
  }, [searchTerm, northernRainStations]);

  const handleBlur = (event) => {
    // Check if the clicked element is not inside the search component
    if (inputRef.current && !inputRef.current.contains(event.target)) {
      setFilteredStations([]); // Clear filtered stations when clicking outside
    }
  };

  const handleStationClick = (stationName) => {
    setSearchTerm(stationName); // Set the search term to the clicked station name
    setFilteredStations([]); // Clear the filtered stations after selection
  };

  return (
    <Box sx={{ width: '100%', ml: { xs: 0, md: 1 }, position: 'relative' }} onClick={handleBlur}>
      <FormControl sx={{ width: { xs: '100%', md: 240 }, pr: 1 }}>
        <OutlinedInput
          ref={inputRef} // ตั้งค่า ref ให้กับ OutlinedInput
          size="small"
          id="header-search"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          startAdornment={
            <InputAdornment position="start" sx={{ mr: -0.5 }}>
              <SearchOutlined />
            </InputAdornment>
          }
          aria-describedby="header-search-text"
          inputProps={{
            'aria-label': 'search'
          }}
          placeholder="ค้นหารายชื่อสถานี..."
        />
      </FormControl>
      {searchTerm &&
        filteredStations.length > 0 && ( // Show dropdown only when search term is not empty and there are results
          <Box
            sx={{
              mt: 1,
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: '4px',
              width: { xs: '100%', md: 240 },
              maxHeight: '200px',
              overflowY: 'auto',
              position: 'absolute',
              zIndex: 10,
              backgroundColor: 'white'
            }}
          >
            <List>
              {filteredStations.map((station) => (
                <ListItem button key={station.id} onClick={() => handleStationClick(station.name)}>
                  {' '}
                  {/* เพิ่ม onClick ที่นี่ */}
                  <ListItemText primary={station.name} />
                </ListItem>
              ))}
            </List>
          </Box>
        )}
    </Box>
  );
}
