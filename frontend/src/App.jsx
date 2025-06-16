import { useState } from 'react';
import { Box, Container, TextField, Button, Typography, Paper, CircularProgress } from '@mui/material';
import axios from 'axios';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await axios.post('http://localhost:5000/ask', { question });
      setResponse(result.data);
    } catch (err) {
      setError('Failed to get response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Agentic RAG Assistant
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
        <TextField
          fullWidth
          label="Ask your software engineering question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          variant="outlined"
          sx={{ mb: 2 }}
        />
        <Button 
          type="submit" 
          variant="contained" 
          fullWidth 
          disabled={loading || !question.trim()}
        >
          {loading ? <CircularProgress size={24} /> : 'Ask Question'}
        </Button>
      </Box>

      {error && (
        <Paper sx={{ p: 2, mb: 2, bgcolor: '#fff3f3' }}>
          <Typography color="error">{error}</Typography>
        </Paper>
      )}

      {response && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Response</Typography>
          <Typography variant="subtitle1" gutterBottom>
            <strong>Question:</strong> {response.question}
          </Typography>
          <Typography variant="body1" paragraph>
            <strong>Answer:</strong> {response.answer}
          </Typography>
          <Typography variant="body1">
            <strong>Critique:</strong> {response.critique}
          </Typography>
        </Paper>
      )}
    </Container>
  );
}

export default App;