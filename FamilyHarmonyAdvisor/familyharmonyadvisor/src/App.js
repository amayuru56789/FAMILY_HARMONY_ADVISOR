import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ChatInterface from './components/ChatInterface';

const theme = createTheme({
  palette: {
    primary: {
      main: '#4a6fa5',
      light: '#7895c7',
      dark: '#2a4d7f',
    },
    secondary: {
      main: '#6d987a',
      light: '#9bc0a7',
      dark: '#427351',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ChatInterface />
    </ThemeProvider>
  );
}

export default App;
