import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Send, User, Bot, Loader2, Sparkles, MessageSquare } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:5000/api';

const Chat = ({ theme, toggleTheme }) => {
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hello! I am Vynote AI, your personalized academic assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await axios.post(`${API_BASE}/nlp/chat`, { query: input });
      setMessages(prev => [...prev, { role: 'bot', text: res.data.answer }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'bot', text: 'Connection error. Ensure the Phi-3 backend is running on port 5000.' }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className={`min-h-screen bg-slate-950 text-white flex flex-col transition-all overflow-hidden ${theme === 'dark' ? 'dark' : 'bg-white text-slate-900'}`}>
      
      <Navbar theme={theme} toggleTheme={toggleTheme} />

      <div className="flex-1 flex flex-col relative pt-24 max-w-4xl mx-auto w-full px-4 md:px-0 mb-6">
        
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-vynote-accent/5 blur-[120px] pointer-events-none rounded-full"></div>

        <div 
           ref={scrollRef}
           className="flex-1 overflow-y-auto px-2 py-8 space-y-6 scrollbar-hide no-scrollbar"
        >
          <AnimatePresence>
            {messages.map((msg, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className={`flex items-start gap-4 ${msg.role === 'user' ? 'flex-row-reverse text-right' : ''}`}
              >
                <div className={`p-2.5 rounded-xl shadow-lg flex-shrink-0 ${msg.role === 'bot' ? 'bg-vynote-accent shadow-violet-500/20' : 'bg-slate-800 border border-white/10'}`}>
                   {msg.role === 'bot' ? <Bot size={18} className="text-white" /> : <User size={18} className="text-slate-300" />}
                </div>

                <div className={`max-w-[80%] p-5 rounded-3xl glass-card text-sm leading-relaxed ${msg.role === 'user' ? 'dark:bg-violet-600/10 border-violet-500/20 rounded-tr-none' : 'dark:bg-slate-900/60 rounded-tl-none'}`}>
                  {msg.text}
                </div>
              </motion.div>
            ))}
            
            {isTyping && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-start gap-4">
                 <div className="p-2.5 rounded-xl bg-vynote-accent animate-pulse">
                    <Bot size={18} className="text-white" />
                 </div>
                 <div className="p-5 glass-card dark:bg-slate-900/60 rounded-3xl rounded-tl-none flex items-center gap-2">
                    <Loader2 size={16} className="animate-spin text-vynote-accent" />
                    <span className="text-sm font-medium animate-pulse text-slate-400">Vynote AI is thinking...</span>
                 </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <div className="p-4 relative z-10 w-full max-w-4xl mx-auto">
          <form 
            onSubmit={handleSubmit}
            className="glass-card dark:bg-slate-900/80 p-2 md:p-3 flex items-center gap-3 border-white/10 hover:neo-glow transition-all rounded-[2rem]"
          >
            <div className="pl-4 text-slate-500">
               <Sparkles size={20} />
            </div>
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything..."
              className="flex-1 bg-transparent border-none outline-none text-white placeholder-slate-600 text-sm md:text-base font-medium py-2 px-1"
            />
            <button 
              type="submit" 
              className="bg-vynote-accent hover:bg-violet-600 p-3 rounded-2xl text-white transition-all shadow-lg shadow-violet-500/20"
              disabled={!input.trim() || isTyping}
            >
              <Send size={20} />
            </button>
          </form>
          <p className="text-[9px] text-center mt-3 text-slate-600 font-black uppercase tracking-[0.2em]">
            Vynote Premium Engine • Local Inference Active
          </p>
        </div>
      </div>
    </div>
  );
};

export default Chat;
