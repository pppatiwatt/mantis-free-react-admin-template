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
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [isFocused, setIsFocused] = useState(false);

  const inputRef = useRef(null);
  const listItemRefs = useRef([]);

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
      setIsFocused(false);
    }
  };

  const handleFocus = () => {
    setIsFocused(true);
  };

  const handleStationClick = (stationName) => {
    setSearchTerm(stationName);
    setFilteredStations([]);
    setIsFocused(false);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'ArrowDown') {
      setSelectedIndex((prevIndex) => {
        const newIndex = prevIndex < filteredStations.length - 1 ? prevIndex + 1 : prevIndex;
        if (listItemRefs.current[newIndex]) {
          listItemRefs.current[newIndex].scrollIntoView({ block: 'nearest' });
        }
        return newIndex;
      });
    } else if (event.key === 'ArrowUp') {
      setSelectedIndex((prevIndex) => {
        const newIndex = prevIndex > 0 ? prevIndex - 1 : prevIndex;
        if (listItemRefs.current[newIndex]) {
          listItemRefs.current[newIndex].scrollIntoView({ block: 'nearest' });
        }
        return newIndex;
      });
    } else if (event.key === 'Enter' && selectedIndex >= 0) {
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
          onFocus={handleFocus}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyDown={handleKeyDown}
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
      {isFocused && searchTerm && filteredStations.length > 0 && (
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
                ref={(el) => (listItemRefs.current[index] = el)}
                selected={index === selectedIndex}
                onClick={() => handleStationClick(station.name)}
                sx={{
                  '&:hover': {
                    backgroundColor: 'rgba(128, 128, 128, 0.1)'
                  },
                  '&.Mui-selected': {
                    backgroundColor: 'rgba(128, 128, 128, 0.1)'
                  },
                  '&.Mui-selected:hover': {
                    backgroundColor: 'rgba(128, 128, 128, 0.15)'
                  }
                }}
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
