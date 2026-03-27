import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Workspace from './pages/Workspace';
import Chat from './pages/Chat';

function App() {
  // 1. Initialize theme from localStorage or system preference
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem('vynote-theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  });

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  // 2. Persist and sync theme with HTML class
  useEffect(() => {
    localStorage.setItem('vynote-theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light'); // For safety
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light'); 
    }
  }, [theme]);

  return (
    <Router>
      {/* 3. Global Layout Wrapper (theme-aware colors) */}
      <div className={`
          min-h-screen transition-colors duration-500 selection:bg-violet-500 selection:text-white
          ${theme === 'dark' ? 'bg-slate-950 text-slate-100' : 'bg-gradient-to-br from-gray-50 to-white text-gray-900'}
      `}>
        <Routes>
          <Route path="/" element={<Home theme={theme} toggleTheme={toggleTheme} />} />
          <Route path="/workspace" element={<Workspace theme={theme} toggleTheme={toggleTheme} />} />
          <Route path="/chat" element={<Chat theme={theme} toggleTheme={toggleTheme} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
