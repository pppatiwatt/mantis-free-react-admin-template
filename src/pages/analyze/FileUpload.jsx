import UploadOutlined from '@ant-design/icons/UploadOutlined';
import { Alert, Box, Button, Typography } from '@mui/material';
import { useState } from 'react';

// ==============================|| FILE UPLOAD COMPONENT ||============================== //
export default function FileUpload() {
  const [files, setFiles] = useState({
    humidity: null,
    rainfall: null,
    maxTemperature: null,
    minTemperature: null,
    panEvaporation: null
  });
  const [error, setError] = useState('');

  const fileTypes = [
    { name: 'ความชื้นสัมพัทธ์', key: 'humidity' },
    { name: 'ปริมาณน้ำฝน', key: 'rainfall' },
    { name: 'อุณหภูมิสูงสุด', key: 'maxTemperature' },
    { name: 'อุณหภูมิต่ำสุด', key: 'minTemperature' },
    { name: 'น้ำระเหยถาด', key: 'panEvaporation' }
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

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        อัพโหลดไฟล์ข้อมูล
      </Typography>
      {fileTypes.map((type) => (
        <Box key={type.key} my={2}>
          <input
            accept=".csv"
            style={{ display: 'none' }}
            id={`upload-${type.key}`}
            type="file"
            onChange={(e) => handleFileChange(e, type.key)}
          />
          <label htmlFor={`upload-${type.key}`}>
            <Button
              variant="outlined"
              component="span"
              startIcon={<UploadOutlined />}
              sx={{
                width: '100%',
                textAlign: 'left',
                padding: '10px',
                borderColor: '#424242', // กรอบสีเทาเข้ม
                color: '#424242', // ตัวหนังสือสีเทาเข้ม
                '&:hover': {
                  borderColor: '#212121', // สีกรอบเข้มขึ้นเมื่อ hover
                  backgroundColor: '#e0e0e0' // สีพื้นหลังเมื่อ hover
                }
              }}
            >
              อัพโหลด {type.name}
            </Button>
          </label>
          {files[type.key] && (
            <Typography variant="body2" sx={{ mt: 1 }}>
              ไฟล์ที่เลือก: {files[type.key].name}
            </Typography>
          )}
        </Box>
      ))}
      {error && <Alert severity="error">{error}</Alert>}
    </Box>
  );
}
