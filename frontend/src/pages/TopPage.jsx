import { Link } from 'react-router-dom';
import { Container, Typography, Box, Card, CardContent, CardActionArea } from '@mui/material';
import MovieIcon from '@mui/icons-material/Movie';
import DescriptionIcon from '@mui/icons-material/Description';

function TopPage() {
  return (
    <Container maxWidth="md" sx={{ mt: 8 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          ビデオ作成アプリケーション
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
          このアプリケーションは、ユーザーがシナリオを作成し、それに基づいて動画を生成するためのものです。
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', gap: 3, justifyContent: 'center', flexWrap: 'wrap' }}>
        <Card sx={{ minWidth: 250, flex: 1, maxWidth: 300 }}>
          <CardActionArea component={Link} to="/scenario" sx={{ height: '100%', p: 3 }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <DescriptionIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="div" gutterBottom>
                1. シナリオ作成
              </Typography>
              <Typography variant="body2" color="text.secondary">
                シナリオ作成ページへ
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>

        <Card sx={{ minWidth: 250, flex: 1, maxWidth: 300 }}>
          <CardActionArea component={Link} to="/video" sx={{ height: '100%', p: 3 }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <MovieIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="div" gutterBottom>
                2. 動画作成
              </Typography>
              <Typography variant="body2" color="text.secondary">
                動画作成ページへ
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      </Box>
    </Container>
  );
}

export default TopPage;
