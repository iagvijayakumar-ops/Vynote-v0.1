import React from 'react';
import { Link } from 'react-router-dom';
import GlassCard from './GlassCard';
import { PlayCircle, Globe, LayoutDashboard } from 'lucide-react';

const Hero = () => {
  return (
    <div className="relative pt-32 sm:pt-48 pb-20 px-6 overflow-hidden">

      {/* Dynamic Background Blobs */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-[600px] bg-gradient-to-b from-vynote-accent/10 to-transparent blur-[120px] pointer-events-none rounded-full dark:from-vynote-accent/20"></div>
      <div className="absolute -top-20 -right-20 w-[400px] h-[400px] bg-purple-500/5 blur-[100px] pointer-events-none rounded-full dark:bg-vynote-accent/10"></div>

      <div className="max-w-7xl mx-auto text-center relative z-10 animate-fade-in">

        {/* Badge Frame */}
        <div className="inline-flex items-center gap-2.5 px-5 py-2.5 glass-card bg-white/50 border-slate-200 dark:bg-slate-900/40 dark:border-white/10 rounded-full text-[11px] font-black uppercase tracking-widest text-slate-500 dark:text-slate-400 mb-10 hover:shadow-lg dark:hover:neo-glow transition-all active:scale-95 cursor-default">
          <Globe size={14} className="text-vynote-accent" />
          <span>New: Global Translation Support v2.0</span>
        </div>

        <h1 className="text-5xl md:text-8xl font-black mb-8 leading-tight tracking-tighter text-slate-900 dark:text-transparent dark:bg-clip-text dark:bg-gradient-to-r dark:from-white dark:via-slate-100 dark:to-slate-500">
          Turn lectures <br /> into <span className="text-vynote-accent italic underline decoration-violet-500/30">Clarity.</span>
        </h1>

        <p className="max-w-2xl mx-auto text-lg sm:text-xl text-slate-600 dark:text-slate-400 mb-14 font-medium leading-loose px-4 sm:px-0">
          Upload your audio recordings. Get professional notes, smart summaries,
          and actionable key points instantly. Powered by Phi-3 AI for faster local processing.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-24">
          <Link to="/workspace">
            <button className="flex items-center gap-3 bg-vynote-accent hover:bg-violet-600 px-10 py-5 rounded-3xl text-lg font-black text-white transition-all hover:scale-105 active:scale-95 shadow-2xl shadow-violet-500/40">
              <PlayCircle size={22} className="text-white fill-white/10" />
              Upload Lecture
            </button>
          </Link>

          <Link to="/chat">
            <GlassCard className="flex items-center gap-3 px-10 py-5 rounded-3xl text-lg font-black text-slate-700 dark:text-white transition-all active:scale-95 border-slate-200 shadow-xl dark:border-white/10 hover:bg-slate-50 dark:hover:bg-white/10">
              <LayoutDashboard size={22} className="text-slate-400" />
              Try Demo Chat
            </GlassCard>
          </Link>
        </div>

        {/* Hero Illustration Mockup */}
        <GlassCard className="max-w-5xl mx-auto p-1.5 md:p-3 relative group transition-all !rounded-[2.5rem] border-slate-200 shadow-[0_20px_50px_rgba(0,0,0,0.1)] dark:border-white/10 dark:shadow-[0_20px_50px_rgba(0,0,0,0.3)] bg-white/70 dark:bg-slate-950/80" hover={false}>
          <div className="h-6 w-full bg-slate-100 dark:bg-slate-900 flex items-center gap-2.5 px-6 border-b border-slate-200 dark:border-white/5 rounded-t-[2.3rem]">
            <div className="w-3 h-3 rounded-full bg-red-400/30 dark:bg-red-400/50"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-400/30 dark:bg-yellow-400/50"></div>
            <div className="w-3 h-3 rounded-full bg-green-400/30 dark:bg-green-400/50"></div>
          </div>
          <div className="bg-slate-50 dark:bg-slate-950/20 p-12 md:p-24 text-slate-400 italic font-medium transition-all group-hover:scale-[1.01]">
            <div className="flex flex-col gap-6 animate-pulse opacity-40">
              <div className="h-6 bg-slate-300 dark:bg-slate-800 rounded-full w-1/3"></div>
              <div className="h-6 bg-slate-300 dark:bg-slate-800 rounded-full w-2/3"></div>
              <div className="h-40 bg-slate-200 dark:bg-slate-800/30 rounded-3xl w-full border-2 border-dashed border-slate-300 dark:border-slate-800 mt-8 flex flex-col items-center justify-center gap-2 no-italic">
                <LayoutDashboard size={32} />
                <span className="text-sm font-black uppercase tracking-widest text-slate-400 opacity-60">Interactive Dashboard View</span>
              </div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default Hero;
