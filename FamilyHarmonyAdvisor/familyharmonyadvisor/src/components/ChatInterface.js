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
  Toolbar,
   Drawer,
  ListItemIcon,
  Divider,
  Button,
  useTheme,
  useMediaQuery
} from '@mui/material';
import { 
  Send as SendIcon, 
  Psychology as PsychologyIcon,Home as HomeIcon,
  History as HistoryIcon,
  Help as HelpIcon,
  Settings as SettingsIcon,
  AccountCircle as AccountIcon,
  Lightbulb as LightbulbIcon 
} from '@mui/icons-material';
import axios from 'axios';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const messagesEndRef = useRef(null);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

   // Sample conversation history for demo
  const [conversations, setConversations] = useState([
    { id: 1, title: "Financial stress discussion", date: "2 hours ago" },
    { id: 2, title: "Parenting advice", date: "Yesterday" },
    { id: 3, title: "Communication issues", date: "3 days ago" }
  ]);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

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

   const drawer = (
    <Box sx={{ overflow: 'auto' }}>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
        <PsychologyIcon color="primary" sx={{ fontSize: 32, mr: 1 }} />
        <Typography variant="h6" noWrap component="div">
          Harmony Advisor
        </Typography>
      </Box>
      <Divider />
      <List>
        <ListItem button>
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText primary="Home" />
        </ListItem>
        <ListItem button>
          <ListItemIcon>
            <HistoryIcon />
          </ListItemIcon>
          <ListItemText primary="History" />
        </ListItem>
        <ListItem button>
          <ListItemIcon>
            <HelpIcon />
          </ListItemIcon>
          <ListItemText primary="Help & Tips" />
        </ListItem>
        <ListItem button>
          <ListItemIcon>
            <SettingsIcon />
          </ListItemIcon>
          <ListItemText primary="Settings" />
        </ListItem>
      </List>
      <Divider />
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Recent Conversations
        </Typography>
        <List>
          {conversations.map(convo => (
            <ListItem button key={convo.id}>
              <ListItemIcon>
                <AccountIcon />
              </ListItemIcon>
              <ListItemText primary={convo.title} secondary={convo.date} />
            </ListItem>
          ))}
        </List>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      {/* Sidebar/Drawer */}
      <Box
        component="nav"
        sx={{ width: { md: 280 }, flexShrink: { md: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 280 },
          }}
        >
          {drawer}
        </Drawer>
        
        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 280 },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main content */}
      <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <AppBar 
          position="static" 
          color="default" 
          elevation={1}
          sx={{ 
            backgroundColor: 'white',
            borderBottom: '1px solid',
            borderColor: 'divider'
          }}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { md: 'none' } }}
            >
              <PsychologyIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: 'text.primary' }}>
              Family Harmony Advisor
            </Typography>
            <Button 
              color="primary" 
              startIcon={<LightbulbIcon />}
              variant="outlined"
              size="small"
            >
              Tips
            </Button>
          </Toolbar>
        </AppBar>

        <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2, backgroundColor: '#f9fafb' }}>
          {messages.length === 0 ? (
            <Box sx={{ 
              display: 'flex', 
              flexDirection: 'column', 
              alignItems: 'center', 
              justifyContent: 'center', 
              height: '100%',
              textAlign: 'center',
              maxWidth: 600,
              mx: 'auto',
              py: 8
            }}>
              <img 
                src="https://img.freepik.com/free-vector/family-therapy-session-abstract-concept-illustration_335657-3874.jpg" 
                alt="Family Harmony" 
                style={{ 
                  width: '100%', 
                  maxWidth: 300, 
                  marginBottom: 24,
                  borderRadius: 16
                }} 
              />
              <Typography variant="h5" gutterBottom color="primary">
                Welcome to Family Harmony Advisor
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                I'm here to help you navigate family challenges and improve communication. 
                Share what's on your mind, and let's work together towards solutions.
              </Typography>
              <Typography variant="body2" color="text.secondary">
                You can ask about conflict resolution, parenting advice, financial stress, or any other family matter.
              </Typography>
            </Box>
          ) : (
            <List>
              {messages.map((message) => (
                <ListItem key={message.id} alignItems="flex-start" sx={{ 
                  justifyContent: message.is_user ? 'flex-end' : 'flex-start' 
                }}>
                  {!message.is_user && (
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        <PsychologyIcon />
                      </Avatar>
                    </ListItemAvatar>
                  )}
                  <ListItemText
                    primary={message.text}
                    secondary={new Date(message.timestamp).toLocaleTimeString()}
                    sx={{ 
                      bgcolor: message.is_user ? 'primary.light' : 'grey.100',
                      p: 2,
                      borderRadius: 2,
                      maxWidth: '70%',
                      ml: message.is_user ? 'auto' : 0,
                      mr: message.is_user ? 0 : 'auto',
                      '& .MuiListItemText-primary': {
                        color: message.is_user ? 'white' : 'text.primary'
                      },
                      '& .MuiListItemText-secondary': {
                        color: message.is_user ? 'primary.100' : 'text.secondary'
                      }
                    }}
                  />
                  {message.is_user && (
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'grey.500', ml: 1 }}>
                        <AccountIcon />
                      </Avatar>
                    </ListItemAvatar>
                  )}
                </ListItem>
              ))}
              <div ref={messagesEndRef} />
            </List>
          )}
        </Box>

        <Box sx={{ 
          p: 2, 
          borderTop: '1px solid', 
          borderColor: 'divider',
          backgroundColor: 'white'
        }}>
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
              sx={{ 
                backgroundColor: 'primary.main',
                color: 'white',
                '&:hover': {
                  backgroundColor: 'primary.dark'
                },
                '&:disabled': {
                  backgroundColor: 'grey.300'
                }
              }}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default ChatInterface;