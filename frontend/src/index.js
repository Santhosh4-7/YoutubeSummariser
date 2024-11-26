import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Global CSS styles (optional)
import App from './App'; // The main React component
import reportWebVitals from './reportWebVitals'; // Optional, for performance tracking

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // Hooks into the root div in index.html
);

// Performance tracking (optional)
reportWebVitals();
