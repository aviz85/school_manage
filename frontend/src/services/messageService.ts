import axiosInstance from './axiosConfig';

const API_URL = 'http://localhost:8000/api';  // Adjust this to your backend URL

export const messageService = {
  getAllMessages: () => axiosInstance.get(`${API_URL}/messages/`),
  getInboxMessages: () => axiosInstance.get(`${API_URL}/messages/inbox/`),
  getSentMessages: () => axiosInstance.get(`${API_URL}/messages/sent/`),
  getUnreadCount: () => axiosInstance.get(`${API_URL}/messages/unread-count/`),
  markAsRead: (id: number) => axiosInstance.post(`${API_URL}/messages/${id}/mark-as-read/`),
  createMessage: (message: { recipient: string; subject: string; content: string }) => 
    axiosInstance.post(`${API_URL}/messages/`, message),
  verifyMessage: (content: string) => 
    axiosInstance.post(`${API_URL}/messages/verify/`, { content }),
};