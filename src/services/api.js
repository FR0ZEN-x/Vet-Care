export const apiService = {
  async login(credentials) {
    return await axios.post('/api/login', credentials)
  },
  // ... other active methods ...
} 