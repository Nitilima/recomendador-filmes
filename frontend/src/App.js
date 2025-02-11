import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Container, Typography, Card, CardContent, Grid } from '@mui/material';

function App() {
  const [query, setQuery] = useState(''); // Estado para o termo de pesquisa
  const [movies, setMovies] = useState([]); // Estado para os filmes encontrados
  const [error, setError] = useState(''); // Estado para mensagens de erro

  const handleSearch = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/buscar-filmes?query=${query}`);
      setMovies(response.data);
      setError('');
    } catch (err) {
      setError('Nenhum filme encontrado.');
      setMovies([]);
    }
  };

  return (
    <Container>
      <Typography variant="h3" align="center" gutterBottom>
        Busca de Filmes
      </Typography>

      {/* Barra de pesquisa */}
      <Grid container spacing={2} alignItems="center" justifyContent="center">
        <Grid item>
          <TextField
            label="Pesquisar filmes"
            variant="outlined"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </Grid>
        <Grid item>
          <Button variant="contained" color="primary" onClick={handleSearch}>
            Buscar
          </Button>
        </Grid>
      </Grid>

      {/* Mensagem de erro */}
      {error && (
        <Typography variant="body1" color="error" align="center" style={{ marginTop: '20px' }}>
          {error}
        </Typography>
      )}

      {/* Lista de filmes */}
      <Grid container spacing={3} style={{ marginTop: '20px' }}>
        {movies.map((movie) => (
          <Grid item key={movie.id} xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  {movie.nome}
                </Typography>
                <Typography color="textSecondary">
                  Ano: {movie.ano}
                </Typography>
                <Typography color="textSecondary">
                  Gênero: {movie.genero}
                </Typography>
                <Typography color="textSecondary">
                  Avaliação: {movie.avaliacao}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default App;