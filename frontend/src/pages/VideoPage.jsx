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
  FormControlLabel,
  Checkbox,
  Slider,
  CircularProgress,
} from '@mui/material';
import LoadingButton from '@mui/lab/LoadingButton';
import DescriptionIcon from '@mui/icons-material/Description';
import MovieIcon from '@mui/icons-material/Movie';

function VideoPage() {
  const navigate = useNavigate();
  const [scenarioText, setScenarioText] = useState('');
  const [subtitles, setSubtitles] = useState(true);
  const [duration, setDuration] = useState(10);
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');
  const [error, setError] = useState('');

  const handleCreateVideo = async () => {
    setLoading(true);
    setError('');
    setVideoUrl('');

    try {
      const response = await fetch('http://localhost:8000/api/video/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scenario: scenarioText,
          with_subtitles: subtitles,
          duration: duration,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'エラーが発生しました。');
      }

      // Poll for video completion
      const taskId = data.task_id;
      await pollVideoStatus(taskId);
    } catch (err) {
      setError('エラーが発生しました。');
      console.error(err);
      setLoading(false);
    }
  };

  const pollVideoStatus = async (taskId) => {
    const maxAttempts = 60;
    let attempts = 0;

    const checkStatus = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/video/status/${taskId}`);
        const data = await response.json();

        if (data.status === 'completed') {
          setVideoUrl(`http://localhost:8000${data.video_url}`);
          setLoading(false);
        } else if (data.status === 'failed') {
          setError('エラーが発生しました。');
          setLoading(false);
        } else {
          attempts++;
          if (attempts < maxAttempts) {
            setTimeout(checkStatus, 2000);
          } else {
            setError('エラーが発生しました。');
            setLoading(false);
          }
        }
      } catch (err) {
        setError('エラーが発生しました。');
        setLoading(false);
      }
    };

    checkStatus();
  };

  return (
    <Box sx={{ pb: 7 }}>
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          動画作成
        </Typography>

        <Box sx={{ mt: 3 }}>
          <TextField
            fullWidth
            multiline
            rows={6}
            label="シナリオテキスト"
            placeholder="動画にするシナリオを入力してください..."
            value={scenarioText}
            onChange={(e) => setScenarioText(e.target.value)}
            disabled={loading}
          />

          <Box sx={{ mt: 3 }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={subtitles}
                  onChange={(e) => setSubtitles(e.target.checked)}
                  disabled={loading}
                />
              }
              label="字幕をつける"
            />
          </Box>

          <Box sx={{ mt: 3 }}>
            <Typography gutterBottom>動画の長さ: {duration}秒</Typography>
            <Slider
              value={duration}
              onChange={(e, newValue) => setDuration(newValue)}
              min={0}
              max={20}
              step={1}
              marks
              valueLabelDisplay="auto"
              disabled={loading}
            />
          </Box>

          <Box sx={{ mt: 2 }}>
            <LoadingButton
              variant="contained"
              loading={loading}
              onClick={handleCreateVideo}
              disabled={!scenarioText.trim()}
              fullWidth
            >
              Create Video
            </LoadingButton>
          </Box>
        </Box>

        {loading && (
          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>
            <CircularProgress />
            <Typography variant="body2" sx={{ mt: 2 }}>
              動画を生成中...
            </Typography>
          </Box>
        )}

        {videoUrl && (
          <Box sx={{ mt: 3 }}>
            <Alert severity="success" sx={{ mb: 2 }}>
              動画が正常に作成されました。
            </Alert>
            <Paper elevation={2} sx={{ p: 2 }}>
              <video controls width="100%" src={videoUrl}>
                お使いのブラウザは動画タグをサポートしていません。
              </video>
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
          value={1}
          onChange={(event, newValue) => {
            if (newValue === 0) navigate('/scenario');
          }}
        >
          <BottomNavigationAction label="シナリオ作成" icon={<DescriptionIcon />} />
          <BottomNavigationAction label="動画作成" icon={<MovieIcon />} />
        </BottomNavigation>
      </Paper>
    </Box>
  );
}

export default VideoPage;
