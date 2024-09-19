import axios, { AxiosInstance, AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';

// הגדרת טיפוס מותאם אישית שמרחיב את InternalAxiosRequestConfig
interface CustomInternalAxiosRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('accessToken');
        if (token && config.headers) {
          config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as CustomInternalAxiosRequestConfig;
        if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
          originalRequest._retry = true;
          try {
            const refreshToken = localStorage.getItem('refreshToken');
            const response = await axios.post(`${this.api.defaults.baseURL}/api/token/refresh/`, {
              refresh: refreshToken,
            });
            const { access } = response.data;
            localStorage.setItem('accessToken', access);
            if (this.api.defaults.headers.common) {
              this.api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
            }
            return this.api(originalRequest);
          } catch (refreshError) {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        return Promise.reject(error);
      }
    );
  }

  async login(username: string, password: string): Promise<AxiosResponse> {
    return this.api.post('/api/token/', { username, password });
  }

  async getStudents(): Promise<AxiosResponse> {
    return this.api.get('/api/students/');
  }

  async getTeachers(): Promise<AxiosResponse> {
    return this.api.get('/api/teachers/');
  }

  async getCourses(): Promise<AxiosResponse> {
    return this.api.get('/api/courses/');
  }
}

export default new ApiService();