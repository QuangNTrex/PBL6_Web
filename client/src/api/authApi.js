import axios from 'axios';
import { API_URL } from '../utils/lib';

const AUTH_API = `${API_URL}auth`;

const authApi = {
  login: (data) => axios.post(`${AUTH_API}/login`, data),
  register: (data) => axios.post(`${AUTH_API}/register`, data),
  logout: (token) => axios.post(`${AUTH_API}/logout`, { token }),
};

export default authApi;