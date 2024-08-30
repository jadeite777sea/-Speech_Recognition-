import axios from 'axios';

const backends = {
  backend1: 'http://127.0.0.1:5000',
  backend2: ''
};

const instance = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Flask 后端的地址
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default instance;
