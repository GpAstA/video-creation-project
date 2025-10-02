import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import TopPage from './pages/TopPage';
import ScenarioPage from './pages/ScenarioPage';
import VideoPage from './pages/VideoPage';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<TopPage />} />
          <Route path="/scenario" element={<ScenarioPage />} />
          <Route path="/video" element={<VideoPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
