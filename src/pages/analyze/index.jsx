import { Grid, Paper, Typography } from '@mui/material';
import FileUpload from './FileUpload';
import SalesChart from './SalesChart';

// Placeholder component (ไม่เปลี่ยนแปลง)
const PlaceholderComponent = ({ title }) => (
  <Paper
    sx={{
      p: 2,
      height: '200px',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      border: '1px solid #e0e0e0',
      boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.1)'
    }}
  >
    <Typography variant="h6">{title} (Placeholder)</Typography>
  </Paper>
);

// ==============================|| ANALYZE PAGE ||============================== //
export default function AnalyzePage() {
  return (
    <Grid container spacing={3}>
      {/* row 1 - File Upload */}
      <Grid item xs={12}>
        <Typography variant="h5" gutterBottom>
          File Upload
        </Typography>
        <Paper sx={{ p: 2, border: '1px solid #e0e0e0', boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.1)' }}>
          <FileUpload />
        </Paper>
      </Grid>

      {/* row 2 - Sales Chart */}
      <Grid item xs={12} md={8}>
        <Typography variant="h5" gutterBottom>
          Random Forest SPI
        </Typography>
        <SalesChart />
      </Grid>
    </Grid>
  );
}
