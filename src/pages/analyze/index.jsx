import React, { useState } from 'react';
import { Grid, Paper, Typography } from '@mui/material';
import FileUpload from './FileUpload';
import PredictionResult from './PredictionResult';

export default function AnalyzePage() {
  const [predictionResults, setPredictionResults] = useState(null);

  const handlePredictionResult = (results) => {
    setPredictionResults(results);
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h5" gutterBottom>
          อัพโหลดไฟล์และพยากรณ์
        </Typography>
        <Paper sx={{ p: 2, border: '1px solid #e0e0e0', boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.1)' }}>
          <FileUpload onPredictionResult={handlePredictionResult} />
        </Paper>
      </Grid>
      
      {predictionResults && (
        <Grid item xs={12}>
          <PredictionResult results={predictionResults} />
        </Grid>
      )}
    </Grid>
  );
}