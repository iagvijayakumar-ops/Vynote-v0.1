import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import AudioIngestion from '../components/AudioIngestion';
import TranscriptView from '../components/TranscriptView';
import SidebarExtra from '../components/SidebarExtra';
import KnowledgeGraph from '../components/KnowledgeGraph';
import GlassCard from '../components/GlassCard';
import { LayoutDashboard, FileText, Sparkles, Brain } from 'lucide-react';

const Workspace = ({ theme, toggleTheme }) => {
  const [transcriptData, setTranscriptData] = useState(null);
  const [audioUrl, setAudioUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [notesState, setNotesState] = useState(''); 

  return (
    <div className={`min-h-screen flex flex-col transition-all overflow-hidden ${theme === 'dark' ? 'bg-slate-950 text-white' : 'bg-gray-50 text-slate-800'}`}>
       
       <Navbar theme={theme} toggleTheme={toggleTheme} />

       <div className="pt-32 px-6 flex-1 flex flex-col overflow-hidden max-w-[1600px] mx-auto w-full gap-8 pb-8">
          
          {/* Action Header Glass Frame */}
          <GlassCard className="flex flex-col md:flex-row items-center justify-between gap-6 p-8 border-slate-200 shadow-xl dark:border-white/10 dark:bg-slate-900/60 relative z-20" hover={false}>
             <div className="flex items-center gap-5">
                <div className="bg-vynote-accent/10 dark:bg-vynote-accent/10 p-4 rounded-2xl text-vynote-accent transition-all hover:scale-105 active:scale-90 cursor-pointer shadow-lg">
                    <LayoutDashboard size={28} />
                </div>
                <div>
                   <h2 className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-500 dark:from-white dark:to-slate-400 tracking-tight">Lecture Analysis Lab</h2>
                   <p className="text-[10px] text-slate-400 dark:text-slate-500 uppercase tracking-[0.4em] font-black mt-1">Workspace Alpha Suite v2.1</p>
                </div>
             </div>
             
             <AudioIngestion 
                setTranscriptData={setTranscriptData} 
                setAudioUrl={setAudioUrl}
                setLoading={setLoading}
             />
          </GlassCard>

          <div className="flex-1 flex flex-col lg:flex-row gap-8 overflow-hidden relative z-10 transition-all">
             
             {/* LEFT PANE: TRANSCRIPT UI */}
             <div className="w-full lg:w-[48%] flex flex-col gap-6 overflow-hidden">
                <GlassCard className="flex-1 flex flex-col overflow-hidden dark:bg-slate-900/40 border-slate-200 dark:border-white/10" hover={false}>
                   <div className="p-5 border-b border-slate-200 dark:border-white/5 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/20">
                      <div className="flex items-center gap-3 text-slate-500 dark:text-slate-400 font-black text-[10px] uppercase tracking-[0.2em] px-2 py-1 bg-slate-100 dark:bg-white/5 rounded-lg">
                         <FileText size={14} /> Interactive Transcript
                      </div>
                      {loading && (
                         <div className="flex items-center gap-3 animate-pulse text-vynote-accent pr-2">
                            <Sparkles size={16} className="animate-spin" />
                            <span className="text-[10px] font-black uppercase tracking-widest">Processing Core...</span>
                         </div>
                      )}
                   </div>
                   <div className="flex-1 overflow-hidden">
                      <TranscriptView 
                        transcriptData={transcriptData}
                        audioUrl={audioUrl}
                      />
                   </div>
                </GlassCard>
             </div>

             {/* RIGHT PANE: AI TOOLS & VISUALS */}
             <div className="w-full lg:w-[52%] flex flex-col gap-8 overflow-hidden">
                {/* TOOLBAR SIDEBAR (TABS) */}
                <GlassCard className="flex-1 dark:bg-slate-900/40 border-slate-200 dark:border-violet-500/10 overflow-hidden flex flex-col" hover={false}>
                   <div className="p-5 border-b border-slate-200 dark:border-white/5 flex items-center gap-3 text-slate-500 dark:text-slate-400 font-black text-[10px] uppercase tracking-[0.2em] bg-slate-50/50 dark:bg-slate-900/20">
                      <Brain size={16} className="text-vynote-accent" /> AI Insights Generation Toolset
                   </div>
                   <div className="flex-1 overflow-hidden">
                      <SidebarExtra 
                        transcriptData={transcriptData} 
                        onNotesGenerated={setNotesState} 
                      />
                   </div>
                </GlassCard>

                {/* VISUAL KNOWLEDGE GRAPH */}
                <GlassCard className="h-[320px] dark:bg-slate-950/40 border-slate-200 dark:border-white/5 shadow-2xl overflow-hidden" hover={false}>
                   <KnowledgeGraph notesText={notesState} />
                </GlassCard>
             </div>

          </div>
       </div>

    </div>
  );
};

export default Workspace;
