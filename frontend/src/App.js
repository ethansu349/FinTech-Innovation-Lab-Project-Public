import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import CircularProgress from '@mui/material/CircularProgress';
import TextareaAutosize from '@mui/material/TextareaAutosize';
import Alert from '@mui/material/Alert';
import { MenuItem } from '@mui/material';

function App() {
  const [ticker, setTicker] = useState('');
  const [selectedYear, setSelectedYear] = useState('');
  const [data, setData] = useState({});

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = () => {
    setIsLoading(true);
    fetch(`http://localhost:5000/getAnalysis/${ticker}`)
      .then(response => {
          console.log(response);
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          setData(data);
          setIsLoading(false);
          setSelectedYear(Object.keys(data)[0]);
      })
      .catch(error => {
          console.error('There was a problem with your fetch operation:', error);
          setIsLoading(false);
      }
    );
  };

  const handleClear = () => {
    setTicker('');
    setSelectedYear('');
    setData({});
  }

  return (
    <Box sx={{ 
      padding: 4,
      background: 'linear-gradient(to right, #9A72AC, #6A9CFC)',
      minHeight: '100vh',
      color: 'white',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'auto'
     }}>
      <Box sx={{
        width: '60%',
        justifyContent: 'center',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <Typography variant="h4" gutterBottom>
          Financial Analysis Dashboard
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, p: 2 }}>
          <label htmlFor="input-ticker">Input Ticker:</label>
          <TextField
            id="input-ticker"
            variant="outlined"
            size="small"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            style={{ flexGrow: 1 }}
          />
          <Button variant="contained" color="primary" onClick={handleSubmit} disabled={!ticker || isLoading}>
            Analyze
          </Button>
          <Button variant="outlined" color="secondary" onClick={handleClear} disabled={!ticker || isLoading}>
            Clear
          </Button>
        </Box>

        <Alert severity="info" sx={{ marginBottom: 2 }}>Please be patient after clicking "Analyze". Downloading 10-k data and analyzing it may take around 3 ~ 5 minutes. Analyzing the same company for multiple times will result in different analysis output due to uncertainty in LLM model.</Alert>

        <Box sx={{ margin: 2 }}>
          <TextField
            select
            label="Select a Year"
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            fullWidth
            sx={{ marginBottom: 2 }}
          >
            {Object.keys(data).map((year) => (
              <MenuItem key={year} value={year}>
                {year}
              </MenuItem>
            ))}
          </TextField>

          {
            isLoading ? <CircularProgress size={48} /> : (
              <Paper elevation={3} sx={{ padding: 2 }}>
                <Typography variant="h6">Sentiment Analysis:</Typography>
                
                  <TextField
                    label="Sentiment Analysis Result"
                    variant="outlined"
                    value={selectedYear ? data[selectedYear].sentimentAnalysis : ""}
                    fullWidth
                    InputProps={{
                      readOnly: true,
                      inputComponent: TextareaAutosize,
                      inputProps: { 
                        style: { resize: 'none', border: 'none', overflow: 'auto' },
                        minRows: 2,  // Minimum rows to show
                        maxRows: 2
                      }
                    }}
                    margin="normal"
                  />
                <Typography variant="h6">MDA Summary:</Typography>
                
                  <TextField
                      label="MDA Summary Result"
                      variant="outlined"
                      value={selectedYear ? data[selectedYear].mdaSummary : ""}
                      fullWidth
                      InputProps={{
                        readOnly: true,
                        inputComponent: TextareaAutosize,
                        inputProps: { 
                          style: { resize: 'none', border: 'none', overflow: 'auto' },
                          minRows: 2,  // Minimum rows to show
                          maxRows: 2
                        }
                      }}
                      margin="normal"
                  />
                
                <Typography variant="h6">Risk Summary:</Typography>
                
                  <TextField
                      label="Risk Summary Result"
                      variant="outlined"
                      value={selectedYear ? data[selectedYear].riskSummary : ""}
                      fullWidth
                      InputProps={{
                        readOnly: true,
                        inputComponent: TextareaAutosize,
                        inputProps: { 
                          style: { resize: 'none', border: 'none', overflow: 'auto' },
                          minRows: 2,  // Minimum rows to show
                          maxRows: 2
                        }
                      }}
                      margin="normal"
                      multiline
                  />
                
                <Typography variant="h6">Risk Factor Summary:</Typography>
                
                  <TextField
                      label="Risk Summary Result"
                      variant="outlined"
                      value={selectedYear ? data[selectedYear].riskFactorSummary : ""}
                      fullWidth
                      InputProps={{
                        readOnly: true,
                        inputComponent: TextareaAutosize,
                        inputProps: { 
                          style: { resize: 'none', border: 'none', overflow: 'auto' },
                          minRows: 2,  // Minimum rows to show
                          maxRows: 2
                        }
                      }}
                      margin="normal"
                  />
                
              </Paper>
            )
          }
        </Box>
      </Box>
    </Box>
  );
}

export default App;
