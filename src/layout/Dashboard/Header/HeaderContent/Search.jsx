import SearchOutlined from '@ant-design/icons/SearchOutlined';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputAdornment from '@mui/material/InputAdornment';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import OutlinedInput from '@mui/material/OutlinedInput';
import { useEffect, useRef, useState } from 'react';

export default function Search() {
  const [searchTerm, setSearchTerm] = useState('');
  const [northernRainStations, setNorthernRainStations] = useState([]);
  const [filteredStations, setFilteredStations] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(-1); // State สำหรับเก็บดัชนีของสถานีที่เลือก

  const inputRef = useRef(null);

  useEffect(() => {
    // Load data from JSON file
    import('/src/assets/northernRainStations.json')
      .then((data) => {
        setNorthernRainStations(data.default);
      })
      .catch((error) => console.error('Failed to load station data:', error));
  }, []);

  useEffect(() => {
    if (searchTerm) {
      setFilteredStations(northernRainStations.filter((station) => station.name.toLowerCase().includes(searchTerm.toLowerCase())));
    } else {
      setFilteredStations([]);
    }
    setSelectedIndex(-1); // Reset selected index เมื่อมีการค้นหาใหม่
  }, [searchTerm, northernRainStations]);

  const handleBlur = (event) => {
    if (inputRef.current && !inputRef.current.contains(event.target)) {
      setFilteredStations([]);
    }
  };

  const handleStationClick = (stationName) => {
    setSearchTerm(stationName);
    setTimeout(() => {
      setFilteredStations([]);
    }, 100); // หน่วงเวลา 100ms เพื่อซ่อนรายการสถานี
  };

  const handleKeyDown = (event) => {
    if (event.key === 'ArrowDown') {
      // เลื่อนลงในลิสต์
      setSelectedIndex((prevIndex) => (prevIndex < filteredStations.length - 1 ? prevIndex + 1 : prevIndex));
    } else if (event.key === 'ArrowUp') {
      // เลื่อนขึ้นในลิสต์
      setSelectedIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : prevIndex));
    } else if (event.key === 'Enter' && selectedIndex >= 0) {
      // กด Enter เพื่อเลือกสถานีที่กำลังไฮไลท์
      handleStationClick(filteredStations[selectedIndex].name);
    }
  };

  return (
    <Box sx={{ width: '100%', ml: { xs: 0, md: 1 }, position: 'relative' }} onClick={handleBlur}>
      <FormControl sx={{ width: { xs: '100%', md: 240 }, pr: 1 }}>
        <OutlinedInput
          ref={inputRef}
          size="small"
          id="header-search"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyDown={handleKeyDown} // จับ event เมื่อกดปุ่ม
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
      {searchTerm && filteredStations.length > 0 && (
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
            {filteredStations.map((station, index) => (
              <ListItem
                button
                key={station.id}
                selected={index === selectedIndex} // เพิ่มการไฮไลท์เมื่อเลือก
                onClick={() => handleStationClick(station.name)}
              >
                <ListItemText primary={station.name} />
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Box>
  );
}
