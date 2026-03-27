import React from 'react';
import GlassCard from './GlassCard';
import { Brain, Zap, ShieldCheck, Search, Download, Mic } from 'lucide-react';

const Features = () => {
  const features = [
    { title: "Intelligent Notes", desc: "Automated extraction of key concepts and structured summaries using Phi-3.", icon: <Brain size={24} />, color: "text-violet-400 bg-violet-400/10" },
    { title: "Instant Flashcards", desc: "Q&A generation for active recall study sessions, optimized for memory retention.", icon: <Zap size={24} />, color: "text-amber-400 bg-amber-400/10" },
    { title: "Privacy First", desc: "All processing happens locally via Ollama. Your audio data stays on your device.", icon: <ShieldCheck size={24} />, color: "text-emerald-400 bg-emerald-400/10" },
    { title: "Smart Ingestion", desc: "Support for direct audio uploads or YouTube video URLs for immediate analysis.", icon: <Mic size={24} />, color: "text-blue-400 bg-blue-400/10" },
    { title: "RAG Capabilities", desc: "Chat with your lectures using vector-search context for precise accuracy.", icon: <Search size={24} />, color: "text-rose-400 bg-rose-400/10" },
    { title: "PDF Export", desc: "Export your AI-generated insights into clean academic PDF documents.", icon: <Download size={24} />, color: "text-sky-400 bg-sky-400/10" }
  ];

  return (
    <section className="py-24 px-6 relative">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-20 animate-fade-in">
           <h2 className="text-4xl md:text-6xl font-black mb-6 text-slate-900 dark:text-white tracking-tight">Vynote <span className="text-vynote-accent">Toolkit</span></h2>
           <p className="text-slate-500 dark:text-slate-400 font-bold uppercase text-xs tracking-[0.3em]">Production-ready AI utilities</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((f, i) => (
             <GlassCard key={i} className="p-8 group bg-white/60 dark:bg-slate-900/40 border-slate-200 dark:border-white/10">
                <div className={`p-4 rounded-2xl w-fit mb-6 transition-all group-hover:scale-110 shadow-lg ${f.color} dark:bg-transparent dark:border dark:border-white/20`}>
                   {f.icon}
                </div>
                <h3 className="text-xl font-bold mb-4 text-slate-900 dark:text-white group-hover:text-vynote-accent transition-colors">
                   {f.title}
                </h3>
                <p className="text-slate-500 dark:text-slate-400 text-sm font-medium leading-[1.8]">
                   {f.desc}
                </p>
             </GlassCard>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
