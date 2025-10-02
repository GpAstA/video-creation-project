import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  TextField,
  Box,
  Alert,
  Paper,
  BottomNavigation,
  BottomNavigationAction,
} from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';
import DescriptionIcon from '@mui/icons-material/Description';
import MovieIcon from '@mui/icons-material/Movie';

function ScenarioPage() {
  const navigate = useNavigate();
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [generatedScenario, setGeneratedScenario] = useState('');
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    setGeneratedScenario('');

    try {
      const response = await fetch('http://localhost:8000/api/scenario/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: inputText }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'エラーが発生しました。');
      }

      setGeneratedScenario(data.scenario);
    } catch (err) {
      setError('エラーが発生しました。');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ pb: 7 }}>
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          シナリオ作成
        </Typography>

        <Box sx={{ mt: 3 }}>
          <TextField
            fullWidth
            multiline
            rows={6}
            label="シナリオテキスト"
            placeholder="シナリオのアイデアを入力してください..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={loading}
          />

          <Box sx={{ mt: 2 }}>
            <LoadingButton
              variant="contained"
              loading={loading}
              onClick={handleGenerate}
              disabled={!inputText.trim()}
              fullWidth
            >
              Generate
            </LoadingButton>
          </Box>
        </Box>

        {generatedScenario && (
          <Box sx={{ mt: 3 }}>
            <Alert severity="success" sx={{ mb: 2 }}>
              シナリオが正常に作成されました。
            </Alert>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                生成されたシナリオ
              </Typography>
              <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                {generatedScenario}
              </Typography>
            </Paper>
          </Box>
        )}

        {error && (
          <Box sx={{ mt: 3 }}>
            <Alert severity="error">{error}</Alert>
          </Box>
        )}
      </Container>

      <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0 }} elevation={3}>
        <BottomNavigation
          value={0}
          onChange={(event, newValue) => {
            if (newValue === 1) navigate('/video');
          }}
        >
          <BottomNavigationAction label="シナリオ作成" icon={<DescriptionIcon />} />
          <BottomNavigationAction label="動画作成" icon={<MovieIcon />} />
        </BottomNavigation>
      </Paper>
    </Box>
  );
}

export default ScenarioPage;
