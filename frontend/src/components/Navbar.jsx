import React from 'react';
import { Link } from 'react-router-dom';
import GlassCard from './GlassCard';
import { Sparkles, MessageCircle, Moon, Sun, MonitorPlay } from 'lucide-react';

const Navbar = ({ theme, toggleTheme }) => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-[100] px-6 py-6 sm:py-8">
      <div className="max-w-7xl mx-auto flex items-center justify-between transition-all">
        
        {/* Logo with Glass Frame */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="bg-vynote-accent p-2.5 rounded-2xl group-hover:rotate-[15deg] transition-all shadow-xl shadow-vynote-accent/30 dark:shadow-violet-500/20 active:scale-90">
            <MonitorPlay size={22} className="text-white" />
          </div>
          <span className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-500 dark:from-white dark:to-violet-400 tracking-tight">
            Vynote
          </span>
        </Link>

        {/* Links + Controls in GlassCard */}
        <GlassCard className="flex items-center gap-1 sm:gap-6 px-1.5 sm:px-4 py-1.5 !rounded-full sm:!rounded-3xl border-slate-200 shadow-xl dark:border-white/10 dark:shadow-none bg-white/70 dark:bg-slate-900/60" hover={false}>
          <div className="hidden sm:flex items-center gap-4 px-2">
            <Link to="/workspace" className="flex items-center gap-2 text-sm font-bold text-slate-500 hover:text-vynote-accent dark:text-slate-400 dark:hover:text-white transition-all whitespace-nowrap px-4 py-2 hover:bg-slate-100 dark:hover:bg-white/5 rounded-2xl">
              <Sparkles size={16} /> Workspace
            </Link>
            <Link to="/chat" className="flex items-center gap-2 text-sm font-bold text-slate-500 hover:text-vynote-accent dark:text-slate-400 dark:hover:text-white transition-all whitespace-nowrap px-4 py-2 hover:bg-slate-100 dark:hover:bg-white/5 rounded-2xl">
              <MessageCircle size={16} /> AI Chat
            </Link>
          </div>
          
          <div className="h-6 w-[1px] bg-slate-200 dark:bg-white/10 mx-1 hidden sm:block"></div>

          {/* Theme Toggle in Glass Orb */}
          <button 
            onClick={toggleTheme}
            className="p-3.5 sm:p-2.5 rounded-full hover:bg-slate-200 dark:hover:bg-white/10 transition-all text-slate-500 dark:text-slate-400 hover:text-violet-500 dark:hover:text-white active:scale-90"
          >
            {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
          </button>

          <Link to="/workspace">
            <button className="hidden md:block bg-vynote-accent hover:bg-violet-600 px-6 py-2.5 rounded-2xl text-sm font-black text-white transition-all hover:scale-105 active:scale-95 shadow-xl shadow-violet-500/30 dark:shadow-violet-900/40">
              Launch App
            </button>
          </Link>
        </GlassCard>
      </div>
    </nav>
  );
};

export default Navbar;
