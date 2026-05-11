// static/js/api.js

const BASE_URL = '';   // empty = same domain

const API = {

  // Get auth token from localStorage
  getToken() {
    return localStorage.getItem('token');
  },

  // Build headers — add token if available
  headers(isFormData = false) {
    const h = {};
    const token = this.getToken();
    if (token) h['Authorization'] = 'Token ' + token;
    if (!isFormData) h['Content-Type'] = 'application/json';
    return h;
  },

  // GET request
  async get(url) {
    const res = await fetch(BASE_URL + url, {
      headers: this.headers()
    });
    return this._handle(res);
  },

  // POST request
  async post(url, data) {
    const res = await fetch(BASE_URL + url, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify(data)
    });
    return this._handle(res);
  },

  // PATCH request
  async patch(url, data) {
    const res = await fetch(BASE_URL + url, {
      method: 'PATCH',
      headers: this.headers(),
      body: JSON.stringify(data)
    });
    return this._handle(res);
  },

  // DELETE request
  async delete(url) {
    const res = await fetch(BASE_URL + url, {
      method: 'DELETE',
      headers: this.headers()
    });
    return this._handle(res);
  },

  // Upload files (multipart/form-data)
  async upload(url, formData) {
    const res = await fetch(BASE_URL + url, {
      method: 'POST',
      headers: this.headers(true),   // no Content-Type — browser sets boundary
      body: formData
    });
    return this._handle(res);
  },

  // Handle responses — parse JSON and catch errors
  async _handle(res) {
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      // Collect all error messages from DRF
      const messages = [];
      for (const key in data) {
        const val = data[key];
        if (Array.isArray(val)) messages.push(...val);
        else messages.push(val);
      }
      throw new Error(messages.join(' ') || 'Something went wrong.');
    }
    return data;
  },

  // Helpers — save/clear login session
  saveSession(token, user) {
    localStorage.setItem('token',    token);
    localStorage.setItem('role',     user.role);
    localStorage.setItem('username', user.username);
    localStorage.setItem('userId',   user.id);
  },

  clearSession() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('username');
    localStorage.removeItem('userId');
  },

  isLoggedIn() {
    return !!localStorage.getItem('token');
  },

  getRole() {
    return localStorage.getItem('role');
  }
};