import React, { useState } from 'react';
import axios from 'axios';
import { 
  Button, 
  Typography, 
  Box, 
  CircularProgress, 
  Alert, 
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Grid,
  Input
} from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const FileUpload = () => {
  const [files, setFiles] = useState({
    rainfall_file: null,
    evaporation_file: null,
    temperature_max_file: null,
    temperature_min_file: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);

  const fileTypes = [
    { name: 'ปริมาณน้ำฝน', key: 'rainfall_file' },
    { name: 'น้ำระเหยถาด', key: 'evaporation_file' },
    { name: 'อุณหภูมิสูงสุด', key: 'temperature_max_file' },
    { name: 'อุณหภูมิต่ำสุด', key: 'temperature_min_file' }
  ];

  const handleFileChange = (event, fileType) => {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.csv')) {
      setFiles((prevFiles) => ({ ...prevFiles, [fileType]: file }));
      setError('');
    } else {
      setError('กรุณาอัพโหลดไฟล์ CSV เท่านั้น');
    }
  };

  const handleUploadAndProcess = async () => {
    if (!Object.values(files).every(file => file)) {
      setError('กรุณาเลือกไฟล์ให้ครบทั้ง 4 ไฟล์');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    Object.entries(files).forEach(([key, file]) => {
      formData.append(key, file);
    });

    try {
      const response = await axios.post('http://localhost:8000/upload-and-process/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResults(response.data);
    } catch (error) {
      if (error.response) {
        setError(`Error: ${error.response.data.detail}`);
      } else {
        setError('An error occurred while uploading and processing the files');
      }
    } finally {
      setLoading(false);
    }
  };

  const renderTable = () => {
    if (!results) return null;
    return (
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>วันที่</TableCell>
              <TableCell align="right">ค่าจริง</TableCell>
              <TableCell align="right">ค่าพยากรณ์</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {results.dates.map((date, index) => (
              <TableRow key={`${date}-${index}`}>
                <TableCell component="th" scope="row">{date}</TableCell>
                <TableCell align="right">{results.actual_values[index].toFixed(2)}</TableCell>
                <TableCell align="right">{results.predictions[index].toFixed(2)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

  const renderChart = () => {
    if (!results) return null;
    const data = results.dates.map((date, index) => ({
      date,
      actual: results.actual_values[index],
      predicted: results.predictions[index]
    }));

    return (
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="actual" stroke="#8884d8" name="ค่าจริง" />
          <Line type="monotone" dataKey="predicted" stroke="#82ca9d" name="ค่าพยากรณ์" />
        </LineChart>
      </ResponsiveContainer>
    );
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        อัพโหลดไฟล์ข้อมูลและพยากรณ์
      </Typography>
      <Grid container spacing={2}>
        {fileTypes.map((type) => (
          <Grid item xs={12} sm={6} key={type.key}>
            <Input
              type="file"
              inputProps={{
                accept: '.csv',
                id: `upload-${type.key}`
              }}
              onChange={(e) => handleFileChange(e, type.key)}
              style={{ display: 'none' }}
            />
            <label htmlFor={`upload-${type.key}`}>
              <Button
                variant="outlined"
                component="span"
                fullWidth
              >
                อัพโหลด {type.name}
              </Button>
            </label>
            {files[type.key] && (
              <Typography variant="body2" sx={{ mt: 1 }}>
                ไฟล์ที่เลือก: {files[type.key].name}
              </Typography>
            )}
          </Grid>
        ))}
      </Grid>
      <Button
        onClick={handleUploadAndProcess}
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        disabled={loading || !Object.values(files).every(file => file)}
      >
        {loading ? <CircularProgress size={24} /> : 'อัพโหลดและประมวลผล'}
      </Button>
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {results && (
        <Box mt={4}>
          <Typography variant="h6" gutterBottom>ผลการพยากรณ์</Typography>
          <Typography gutterBottom>MSE: {results.mse.toFixed(4)}</Typography>
          {renderTable()}
          <Box mt={4}>
            <Typography variant="subtitle1" gutterBottom>กราฟแสดงผลการพยากรณ์</Typography>
            {renderChart()}
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default FileUpload;