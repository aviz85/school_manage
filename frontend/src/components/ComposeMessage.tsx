import React, { useState, useEffect } from 'react';
import { messageService } from '../services/messageService';
import './ComposeMessage.css';
import axios from 'axios';

interface ComposeMessageProps {
  onClose: () => void;
  onMessageSent: () => void;
  replyTo: Message | null;
}

interface User {
  id: number;
  username: string;
}

interface Message {
  id: number;
  subject: string;
  content: string;
  sender: number;
  sender_username: string;
  timestamp: string;
  is_read: boolean;
}

const ComposeMessage: React.FC<ComposeMessageProps> = ({ onClose, onMessageSent, replyTo }) => {
  const [recipient, setRecipient] = useState<number | ''>('');
  const [subject, setSubject] = useState(replyTo ? `Re: ${replyTo.subject}` : '');
  const [content, setContent] = useState(replyTo ? `\n\nOn ${new Date(replyTo.timestamp).toLocaleString()}, ${replyTo.sender_username} wrote:\n${replyTo.content}` : '');
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const [isSending, setIsSending] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState<{ status: string; explanation: string } | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [messageSent, setMessageSent] = useState(false);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await messageService.getUsers();
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };
    fetchUsers();
  }, []);

  useEffect(() => {
    if (replyTo) {
      const replyRecipient = users.find(user => user.username === replyTo.sender_username);
      if (replyRecipient) {
        setRecipient(replyRecipient.id);
      }
    }
  }, [replyTo, users]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setIsSending(true);

    if (!recipient) {
      setErrors({ recipient: 'Please select a valid recipient' });
      setIsSending(false);
      return;
    }

    try {
      const response = await messageService.createMessage({ recipient, subject, content });
      console.log('Message sent successfully:', response);
      setMessageSent(true);
      setTimeout(() => {
        onMessageSent();
        onClose();
      }, 2000);
    } catch (error) {
      console.error('Error sending message:', error);
      if (axios.isAxiosError(error) && error.response) {
        if (error.response.data.errors) {
          setErrors(error.response.data.errors);
        } else {
          setErrors({ general: `Failed to send message: ${error.response.status} ${error.response.statusText}` });
        }
        console.error('Error response data:', error.response.data);
      } else {
        setErrors({ general: 'Failed to send message. Please try again.' });
      }
    } finally {
      setIsSending(false);
    }
  };

  const handleVerify = async () => {
    setIsVerifying(true);
    setVerificationResult(null);
    setErrors({});

    try {
      const response = await messageService.verifyMessage(content);
      setVerificationResult(response.data);
    } catch (error) {
      console.error('Error verifying message:', error);
      if (axios.isAxiosError(error) && error.response) {
        setErrors({ verification: `Failed to verify message: ${error.response.data.explanation || error.message}` });
      } else {
        setErrors({ verification: 'Failed to verify message. Please try again.' });
      }
    } finally {
      setIsVerifying(false);
    }
  };

  if (messageSent) {
    return (
      <div className="compose-message">
        <h3>Message Sent</h3>
        <p className="success-message">Your message has been sent successfully!</p>
      </div>
    );
  }

  return (
    <div className="compose-message">
      <h3>{replyTo ? 'Reply to Message' : 'Compose New Message'}</h3>
      {errors.general && <p className="error-message">{errors.general}</p>}
      {errors.verification && <p className="error-message">{errors.verification}</p>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="recipient">To:</label>
          <select
            id="recipient"
            value={recipient}
            onChange={(e) => setRecipient(Number(e.target.value))}
            required
          >
            <option value="">Select a recipient</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>{user.username}</option>
            ))}
          </select>
          {errors.recipient && <p className="error-message">{errors.recipient}</p>}
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
          {errors.subject && <p className="error-message">{errors.subject}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="content">Message:</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
          {errors.content && <p className="error-message">{errors.content}</p>}
        </div>
        {verificationResult && (
          <div className={`verification-result ${verificationResult.status.toLowerCase()}`}>
            <p>Status: {verificationResult.status}</p>
            {verificationResult.explanation && <p>Explanation: {verificationResult.explanation}</p>}
          </div>
        )}
        <div className="form-actions">
          <button type="button" onClick={handleVerify} className="verify-button" disabled={isVerifying || !content}>
            {isVerifying ? 'Verifying...' : 'Verify Message'}
          </button>
          <button type="submit" className="send-button" disabled={isSending || !verificationResult || verificationResult.status !== 'APPROVED'}>
            {isSending ? 'Sending...' : 'Send'}
          </button>
          <button type="button" onClick={onClose} className="cancel-button" disabled={isSending || isVerifying}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default ComposeMessage;