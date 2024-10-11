import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function PredictionResult({ results }) {
  if (!results || results.length === 0) return null;

  return (
    <Box mt={4}>
      <Typography variant="h5" gutterBottom>ผลการพยากรณ์</Typography>
      {results.map((result, index) => (
        <Paper key={index} elevation={3} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6">{`สถานี: ${result.station}, ดัชนี: ${result.index_type}`}</Typography>
          <Typography>{`ค่า MSE: ${result.mse.toFixed(4)}`}</Typography>
          
          <Box mt={2}>
            <Typography variant="subtitle1">กราฟแสดงผลการพยากรณ์</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={result.dates.map((date, i) => ({
                  date,
                  actual: result.actual_values[i],
                  predicted: result.predictions[i]
                }))}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="actual" stroke="#8884d8" name="ค่าจริง" />
                <Line type="monotone" dataKey="predicted" stroke="#82ca9d" name="ค่าพยากรณ์" />
              </LineChart>
            </ResponsiveContainer>
          </Box>

          {result.feature_importance && (
            <Box mt={2}>
              <Typography variant="subtitle1">ความสำคัญของคุณลักษณะ</Typography>
              {Object.entries(result.feature_importance).map(([feature, importance]) => (
                <Typography key={feature}>{`${feature}: ${importance.toFixed(4)}`}</Typography>
              ))}
            </Box>
          )}
        </Paper>
      ))}
    </Box>
  );
}