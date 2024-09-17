import React, { useState, useEffect } from 'react';
import { messageService } from '../services/messageService';
import ComposeMessage from './ComposeMessage';
import './MessageInbox.css';

interface Message {
  id: number;
  subject: string;
  content: string;
  sender: string;
  timestamp: string;
  is_read: boolean;
}

const MessageInbox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isComposing, setIsComposing] = useState(false);

  const fetchMessages = async () => {
    try {
      const response = await messageService.getInboxMessages();
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  const handleComposeClick = () => {
    setIsComposing(true);
  };

  const handleCloseCompose = () => {
    setIsComposing(false);
  };

  const handleMessageSent = () => {
    fetchMessages();
    setIsComposing(false);
  };

  return (
    <div className="message-inbox">
      <div className="message-inbox-header">
        <h2>Inbox</h2>
        <button className="compose-button" onClick={handleComposeClick}>Compose New Message</button>
      </div>
      {isComposing && (
        <ComposeMessage onClose={handleCloseCompose} onMessageSent={handleMessageSent} />
      )}
      <div className="message-list">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.is_read ? 'read' : 'unread'}`}>
            <h3 className="message-subject">{message.subject}</h3>
            <p className="message-sender">From: {message.sender}</p>
            <p className="message-content">{message.content}</p>
            <small className="message-timestamp">{new Date(message.timestamp).toLocaleString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MessageInbox;