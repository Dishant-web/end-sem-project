import { WebSocketServer } from 'ws';
import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();
const port = 3000;

// Serve static files
app.use(express.static('public'));

// Start HTTP server
const server = app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

// Create WebSocket server
const wss = new WebSocketServer({ server });

// Store connected clients
const clients = new Set();

// Handle WebSocket connections
wss.on('connection', (ws) => {
  clients.add(ws);

  ws.on('message', (message) => {
    // Broadcast message to all connected clients
    const data = JSON.parse(message);
    const broadcastData = JSON.stringify({
      type: 'message',
      username: data.username,
      content: data.content,
      timestamp: new Date().toLocaleTimeString()
    });

    clients.forEach((client) => {
      if (client.readyState === 1) {
        client.send(broadcastData);
      }
    });
  });

  ws.on('close', () => {
    clients.delete(ws);
  });
});