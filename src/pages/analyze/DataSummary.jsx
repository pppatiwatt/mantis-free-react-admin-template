import { Card, CardContent, Grid, Typography } from '@mui/material';

const DataSummary = () => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="div">
          Data Summary
        </Typography>
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6">Total Records</Typography>
            <Typography variant="h4">10,234</Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6">Average Value</Typography>
            <Typography variant="h4">$45.67</Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6">Highest Value</Typography>
            <Typography variant="h4">$1,234.56</Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6">Lowest Value</Typography>
            <Typography variant="h4">$0.99</Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default DataSummary;
