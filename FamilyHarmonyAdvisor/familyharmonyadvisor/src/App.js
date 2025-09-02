import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
// import ChatInterface from './components/ChatInterface';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './components/Login';

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
    // <ThemeProvider theme={theme}>
    //   <CssBaseline />
    //   <ChatInterface />
    // </ThemeProvider>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/login" element={<Login />} />
              {/* <Route path="/register" element={<Register />} /> */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    {/* <Dashboard /> */}
                  </ProtectedRoute>
                }
              />
              {/* <Route path="/" element={<Navigate to="/dashboard" replace />} /> */}
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
