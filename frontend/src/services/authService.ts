import axiosInstance from './axiosConfig';

export const authService = {
  login: async (username: string, password: string) => {
    const response = await axiosInstance.post('/token/', { username, password });
    localStorage.setItem('accessToken', response.data.access);
    localStorage.setItem('refreshToken', response.data.refresh);
    localStorage.setItem('username', username);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('username');
  },

  isAuthenticated: () => !!localStorage.getItem('accessToken'),

  getUsername: () => localStorage.getItem('username'),
};