import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  AppBar,
  Toolbar
} from '@mui/material';
import { Send as SendIcon, Psychology as PsychologyIcon } from '@mui/icons-material';
import axios from 'axios';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  // Initialize conversation
  useEffect(() => {
    const initializeConversation = async () => {
      try {
        const response = await axios.post('http://localhost:8000/api/conversations/', {
          session_id: `session_${Date.now()}`
        });
        setConversationId(response.data.id);
      } catch (error) {
        console.error('Error initializing conversation:', error);
      }
    };

    initializeConversation();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (input.trim() === '' || !conversationId) return;

    const userMessage = {
      text: input,
      is_user: true,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const response = await axios.post(
        `http://localhost:8000/api/conversations/${conversationId}/send_message/`,
        { message: input }
      );

      setMessages(prev => [...prev, response.data.ai_response]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        text: "Sorry, I'm having trouble connecting to the server. Please try again later.",
        is_user: false,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <AppBar position="static" color="primary">
        <Toolbar>
          <PsychologyIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Family Harmony Advisor
          </Typography>
        </Toolbar>
      </AppBar>

      <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
        <List>
          {messages.map((message, index) => (
            <ListItem key={index} alignItems="flex-start">
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: message.is_user ? 'primary.main' : 'secondary.main' }}>
                  {message.is_user ? 'U' : 'A'}
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={message.text}
                secondary={new Date(message.timestamp).toLocaleTimeString()}
                sx={{ 
                  bgcolor: message.is_user ? 'primary.light' : 'grey.100',
                  p: 1,
                  borderRadius: 2,
                  maxWidth: '70%',
                  ml: message.is_user ? 'auto' : 0,
                  mr: message.is_user ? 0 : 'auto'
                }}
              />
            </ListItem>
          ))}
          <div ref={messagesEndRef} />
        </List>
      </Box>

      <Box sx={{ p: 2, borderTop: '1px solid', borderColor: 'divider' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Describe your family concern..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          multiline
          maxRows={4}
          sx={{ mb: 1 }}
        />
        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
          <IconButton 
            color="primary" 
            onClick={handleSend}
            disabled={input.trim() === ''}
          >
            <SendIcon />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
};

export default ChatInterface;