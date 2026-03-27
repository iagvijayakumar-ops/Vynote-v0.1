import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { jsPDF } from 'jspdf';
import { LexicalComposer } from '@lexical/react/LexicalComposer';
import { RichTextPlugin } from '@lexical/react/LexicalRichTextPlugin';
import { ContentEditable } from '@lexical/react/LexicalContentEditable';
import { HistoryPlugin } from '@lexical/react/LexicalHistoryPlugin';
import { Loader2, Zap, Brain, MessageSquare } from 'lucide-react';

const API_BASE = 'http://localhost:5000/api';

const SidebarExtra = ({ transcriptData, onNotesGenerated }) => {
  const [activeTab, setActiveTab] = useState('notes');
  const [loading, setLoading] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState('Thinking...');

  const [notes, setNotes] = useState('');
  const [glossary, setGlossary] = useState('');
  const [eli5, setEli5] = useState('');
  const [assessments, setAssessments] = useState(null);
  
  const [sessionId, setSessionId] = useState(null);
  const [chatLog, setChatLog] = useState([]);
  const [query, setQuery] = useState('');

  const rawText = transcriptData?.text;

  useEffect(() => {
    let interval;
    if (loading) {
      const messages = ["Summarizing text...", "Building glossary...", "Tuning Phi-3...", "Almost there..."];
      let i = 0;
      interval = setInterval(() => {
        setLoadingMsg(messages[i % messages.length]);
        i++;
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const initialConfig = {
    namespace: 'LectureEditor',
    theme: { paragraph: 'editor-p' },
    onError(error) { console.error(error); },
  };

  const handleGenerateNotes = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/nlp/notes`, { text: rawText });
      setNotes(res.data.notes);
      if (onNotesGenerated) onNotesGenerated(res.data.notes);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleGenerateGlossary = async (isEli5) => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/nlp/extra`, { text: rawText, eli5: isEli5 });
      if (isEli5) setEli5(res.data.extra_glossary);
      else setGlossary(res.data.extra_glossary);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleGenerateAssessments = async () => {
    if (!notes) return alert("Generate Notes first!");
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/nlp/assess`, { notes });
      setAssessments(res.data.assessments);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleSetupRAG = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/rag/index`, { text: rawText });
      setSessionId(res.data.session_id);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const handleSendChat = async (e) => {
    e.preventDefault();
    if (!query || !sessionId) return;
    
    setChatLog(prev => [...prev, {role: 'user', text: query}]);
    setQuery('');
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/rag/chat`, { session_id: sessionId, query });
      setChatLog(prev => [...prev, {role: 'bot', text: res.data.answer}]);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const exportPDF = () => {
      const doc = new jsPDF();
      doc.text(notes || "No content.", 10, 10);
      doc.save("LectureNotes.pdf");
  };

  if (!transcriptData) {
    return <div className="p-8 text-center text-slate-500 font-bold uppercase text-[10px] tracking-widest leading-loose">Upload audio for AI tools.</div>;
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-950/20 backdrop-blur-md">
      <div className="flex border-b border-white/5 bg-slate-900/40">
        {['notes', 'extra', 'assess', 'chat'].map(tab => (
          <button 
            key={tab} 
            className={`flex-1 py-3 text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === tab ? 'text-vynote-accent border-b-2 border-vynote-accent bg-vynote-accent/5' : 'text-slate-500 hover:text-slate-300'}`} 
            onClick={() => setActiveTab(tab)}
          >
             {tab}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto p-6 scrollbar-hide no-scrollbar relative">
        {loading && (
           <div className="absolute top-4 left-6 right-6 z-20 flex items-center gap-3 p-3 bg-vynote-accent/10 border border-vynote-accent/20 rounded-xl animate-in slide-in-from-top-2">
              <Loader2 className="animate-spin text-vynote-accent" size={16} />
              <span className="text-[10px] font-bold text-vynote-accent uppercase tracking-widest">{loadingMsg}</span>
           </div>
        )}

        {activeTab === 'notes' && (
           <div className="space-y-4">
              {!notes ? (
                 <button onClick={handleGenerateNotes} className="w-full bg-vynote-accent hover:bg-violet-600 p-4 rounded-xl flex items-center justify-center gap-2 font-bold transition-all shadow-lg shadow-violet-500/20 active:scale-95">
                   <Brain size={18}/> Generate Full Notes
                 </button>
              ) : (
                 <div className="space-y-4 animate-in fade-in zoom-in-95 duration-500">
                    <button onClick={exportPDF} className="w-full border border-green-500/30 bg-green-500/10 text-green-400 hover:bg-green-500/20 p-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-2">
                       Download PDF Archive
                    </button>
                    <div className="bg-slate-900/50 border border-white/5 rounded-2xl p-6 min-h-[300px] text-sm leading-relaxed text-slate-300 whitespace-pre-wrap font-medium">
                        {notes}
                    </div>
                 </div>
              )}
           </div>
        )}

        {activeTab === 'extra' && (
           <div className="space-y-6">
              <button className="w-full glass-card hover:bg-white/5 p-4 rounded-xl flex items-center justify-center gap-2 font-bold transition-all" onClick={() => handleGenerateGlossary(false)}>
                 <Zap size={18} /> Deep Glossary
              </button>
              {glossary && <div className="bg-slate-900/50 border border-white/5 p-4 rounded-xl text-xs leading-relaxed text-slate-400">{glossary}</div>}
              
              <button className="w-full bg-purple-600/20 border border-purple-500/30 text-purple-400 p-4 rounded-xl flex items-center justify-center gap-2 font-bold hover:bg-purple-600/30 transition-all" onClick={() => handleGenerateGlossary(true)}>
                 Explain (Simplified)
              </button>
              {eli5 && <div className="bg-purple-950/20 border border-purple-500/10 p-4 rounded-xl text-xs leading-relaxed text-slate-400 italic">“ {eli5} ”</div>}
           </div>
        )}

        {activeTab === 'assess' && (
            <div className="space-y-4">
                 <button className="w-full bg-blue-600 hover:bg-blue-700 p-4 rounded-xl font-bold transition-all shadow-lg active:scale-95" onClick={handleGenerateAssessments}>Build Knowledge Quiz</button>
                 {assessments && (
                    <div className="space-y-4 pt-4">
                       <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-widest pl-1">Cards & Quizzes</h4>
                       {assessments.flashcards?.map((f, i) => (
                           <div key={i} className="glass-card p-4 text-xs">
                              <div className="text-blue-400 font-bold mb-1">PROMPT</div>
                              <div className="text-slate-200 mb-3">{f.front}</div>
                              <div className="text-slate-500 border-t border-white/5 pt-2 uppercase font-black text-[9px]">Answer</div>
                              <div className="text-slate-400">{f.back}</div>
                           </div>
                       ))}
                    </div>
                 )}
            </div>
        )}

        {activeTab === 'chat' && (
            <div className="flex flex-col h-full space-y-4">
                 {!sessionId ? (
                     <button className="w-full bg-vynote-accent hover:bg-violet-600 p-4 rounded-xl font-bold transition-all shadow-lg active:scale-95" onClick={handleSetupRAG}>Index for Search</button>
                 ) : (
                     <div className="flex flex-col gap-4">
                        <div className="space-y-4 mb-4">
                            {chatLog.map((chat, idx) => (
                               <div key={idx} className={`p-4 rounded-2xl text-xs leading-relaxed ${chat.role === 'user' ? 'bg-violet-600/10 border border-violet-500/20 ml-8 text-white' : 'bg-slate-900/60 border border-white/5 mr-8 text-slate-400'}`}>
                                   <div className="font-black uppercase text-[9px] mb-1 tracking-widest opacity-50">{chat.role}</div>
                                   {chat.text}
                               </div>
                            ))}
                        </div>
                        <form onSubmit={handleSendChat} className="flex gap-2">
                            <input type="text" value={query} onChange={(e)=>setQuery(e.target.value)} className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-xs outline-none focus:ring-1 focus:ring-vynote-accent transition-all" placeholder="Quick query..." />
                            <button type="submit" disabled={!query} className="bg-vynote-accent p-3 rounded-xl hover:scale-105 transition-all"><MessageSquare size={16}/></button>
                        </form>
                     </div>
                 )}
            </div>
        )}
      </div>
    </div>
  );
};

export default SidebarExtra;
