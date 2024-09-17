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
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState<{ status: string; explanation: string } | null>(null);

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

  const handleVerify = async () => {
    setIsVerifying(true);
    setVerificationResult(null);
    setError('');

    try {
      const response = await messageService.verifyMessage(content);
      setVerificationResult(response.data);
    } catch (error) {
      console.error('Error verifying message:', error);
      if (axios.isAxiosError(error) && error.response) {
        setError(`Failed to verify message: ${error.response.data.explanation || error.message}`);
      } else {
        setError('Failed to verify message. Please try again.');
      }
    } finally {
      setIsVerifying(false);
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