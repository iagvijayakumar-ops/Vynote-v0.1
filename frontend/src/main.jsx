import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

console.log("Vynote Main: Mounting...");

const rootEl = document.getElementById('root');
if (!rootEl) {
  console.error("Vynote Main: Root element not found!");
} else {
  ReactDOM.createRoot(rootEl).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
  console.log("Vynote Main: Rendered successfully.");
}
