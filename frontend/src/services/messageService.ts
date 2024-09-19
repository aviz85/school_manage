import axiosInstance from './axiosConfig';

interface Message {
  recipient: number;
  subject: string;
  content: string;
}

export const messageService = {
  getAllMessages: () => axiosInstance.get('/messages/'),
  getInboxMessages: () => axiosInstance.get('/messages/inbox/'),
  getSentMessages: () => axiosInstance.get('/messages/sent/'),
  getUnreadCount: () => axiosInstance.get('/messages/unread_count/'),
  markAsRead: (id: number) => axiosInstance.post(`/messages/${id}/mark-as-read/`),
  createMessage: (message: Message) => {
    console.log('Sending message:', message);
    return axiosInstance.post('/messages/', message);
  },
  getUsers: () => axiosInstance.get('/users/'),
  verifyMessage: (content: string) => axiosInstance.post('/messages/verify/', { content }),
};