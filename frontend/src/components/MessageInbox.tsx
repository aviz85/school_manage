import React, { useState, useEffect } from 'react';
import { messageService } from '../services/messageService';
import ComposeMessage from './ComposeMessage';
import './MessageInbox.css';

interface Message {
  id: number;
  subject: string;
  content: string;
  sender: number;
  sender_username: string;
  timestamp: string;
  is_read: boolean;
}

const MessageInbox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isComposing, setIsComposing] = useState(false);
  const [expandedMessageId, setExpandedMessageId] = useState<number | null>(null);
  const [replyTo, setReplyTo] = useState<Message | null>(null);

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
    setReplyTo(null);
  };

  const handleCloseCompose = () => {
    setIsComposing(false);
    setReplyTo(null);
  };

  const handleMessageSent = () => {
    fetchMessages();
    setIsComposing(false);
    setReplyTo(null);
  };

  const toggleMessage = async (messageId: number) => {
    if (expandedMessageId === messageId) {
      setExpandedMessageId(null);
    } else {
      setExpandedMessageId(messageId);
      const message = messages.find(msg => msg.id === messageId);
      if (message && !message.is_read) {
        try {
          await messageService.markAsRead(messageId);
          setMessages(messages.map(msg => 
            msg.id === messageId ? { ...msg, is_read: true } : msg
          ));
        } catch (error) {
          console.error('Error marking message as read:', error);
        }
      }
    }
  };

  const handleReply = (message: Message) => {
    setReplyTo(message);
    setIsComposing(true);
  };

  return (
    <div className="message-inbox">
      <div className="message-inbox-header">
        <h2>Inbox</h2>
        <button className="compose-button" onClick={handleComposeClick}>Compose New Message</button>
      </div>
      {isComposing && (
        <ComposeMessage 
          onClose={handleCloseCompose} 
          onMessageSent={handleMessageSent} 
          replyTo={replyTo}
        />
      )}
      <div className="message-list">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.is_read ? 'read' : 'unread'} ${expandedMessageId === message.id ? 'expanded' : ''}`}
          >
            <div className="message-header" onClick={() => toggleMessage(message.id)}>
              <h3 className="message-subject">{message.subject}</h3>
              <p className="message-sender">From: {message.sender_username}</p>
              <small className="message-timestamp">{new Date(message.timestamp).toLocaleString()}</small>
            </div>
            {expandedMessageId === message.id && (
              <div className="message-content">
                <p>{message.content}</p>
                <button className="reply-button" onClick={() => handleReply(message)}>Reply</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MessageInbox;