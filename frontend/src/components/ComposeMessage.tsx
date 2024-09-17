import React, { useState } from 'react';
import { messageService } from '../services/messageService';
import './ComposeMessage.css';
import axios from 'axios'; // Assuming axios is imported for axios.isAxiosError

interface ComposeMessageProps {
  onClose: () => void;
  onMessageSent: () => void;
}

const ComposeMessage: React.FC<ComposeMessageProps> = ({ onClose, onMessageSent }) => {
  const [recipient, setRecipient] = useState('');
  const [subject, setSubject] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState('');
  const [isSending, setIsSending] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSending(true);

    try {
      const response = await messageService.createMessage({ recipient, subject, content });
      console.log('Message sent successfully:', response);
      onMessageSent();
      onClose();
    } catch (error) {
      console.error('Error sending message:', error);
      if (axios.isAxiosError(error)) {
        setError(`Failed to send message: ${error.response?.status} ${error.response?.statusText}`);
        console.error('Error response:', error.response?.data);
      } else {
        setError('Failed to send message. Please try again.');
      }
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="compose-message">
      <h3>Compose New Message</h3>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="recipient">To:</label>
          <input
            type="text"
            id="recipient"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="subject">Subject:</label>
          <input
            type="text"
            id="subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="content">Message:</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
        </div>
        <div className="form-actions">
          <button type="submit" className="send-button" disabled={isSending}>
            {isSending ? 'Sending...' : 'Send'}
          </button>
          <button type="button" onClick={onClose} className="cancel-button" disabled={isSending}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default ComposeMessage;