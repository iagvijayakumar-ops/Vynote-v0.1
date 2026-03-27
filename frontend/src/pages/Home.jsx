import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import Features from '../components/Features';
import GlassCard from '../components/GlassCard';
import { MonitorPlay, LayoutDashboard, Brain, MessageSquare, Files, Download } from 'lucide-react';

const Home = ({ theme, toggleTheme }) => {
  return (
    <div className={`
      min-h-screen transition-all select-none
      ${theme === 'dark' ? 'bg-slate-950 text-white' : 'bg-gradient-to-br from-gray-50 to-white text-slate-900'}
    `}>
       
       <Navbar theme={theme} toggleTheme={toggleTheme} />

       <Hero />

       {/* How It Works Layered Section */}
       <section className="py-32 px-6 relative bg-white/10 dark:bg-transparent">
          <div className="max-w-7xl mx-auto text-center mb-24 animate-fade-in">
             <h2 className="text-4xl md:text-6xl font-black mb-6 tracking-tight text-slate-900 dark:text-white">Capture the <span className="text-vynote-accent italic">Unseen.</span></h2>
             <p className="text-slate-500 dark:text-slate-400 font-bold uppercase text-[10px] tracking-[0.5em]">Three steps to academic mastery</p>
          </div>

          <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 relative z-10">
             {/* Step 1 */}
             <GlassCard className="p-10 relative group bg-white/80 dark:bg-slate-950/40 border-slate-200 dark:border-white/10">
                <div className="bg-slate-900 dark:bg-slate-800 absolute -top-5 -right-5 w-14 h-14 flex items-center justify-center rounded-3xl border border-white/5 font-black text-vynote-accent shadow-2xl transition-all group-hover:rotate-12 group-hover:scale-110">1</div>
                <div className="bg-slate-100 dark:bg-slate-900/50 p-6 rounded-3xl w-fit mb-8 border border-slate-200 dark:border-white/10 transition-all group-hover:neo-glow">
                   <MonitorPlay size={36} className="text-vynote-accent" />
                </div>
                <h3 className="text-2xl font-black mb-4 dark:text-white">Upload Audio</h3>
                <p className="text-slate-500 dark:text-slate-400 text-sm font-medium leading-loose">Direct file upload or YouTube extraction with Whisper technology.</p>
             </GlassCard>

             {/* Step 2 */}
             <GlassCard className="p-10 relative group bg-white/80 dark:bg-slate-950/40 border-slate-200 dark:border-white/10">
                <div className="bg-slate-900 dark:bg-slate-800 absolute -top-5 -right-5 w-14 h-14 flex items-center justify-center rounded-3xl border border-white/5 font-black text-vynote-accent shadow-2xl transition-all group-hover:rotate-12 group-hover:scale-110">2</div>
                <div className="bg-slate-100 dark:bg-slate-900/50 p-6 rounded-3xl w-fit mb-8 border border-slate-200 dark:border-white/10 transition-all group-hover:neo-glow">
                   <Brain size={36} className="text-violet-500" />
                </div>
                <h3 className="text-2xl font-black mb-4 dark:text-white">AI Processing</h3>
                <p className="text-slate-500 dark:text-slate-400 text-sm font-medium leading-loose">Phi-3 synthesizes context, extracts key terms, and generates summaries.</p>
             </GlassCard>

             {/* Step 3 */}
             <GlassCard className="p-10 relative group bg-white/80 dark:bg-slate-950/40 border-slate-200 dark:border-white/10">
                <div className="bg-slate-900 dark:bg-slate-800 absolute -top-5 -right-5 w-14 h-14 flex items-center justify-center rounded-3xl border border-white/5 font-black text-vynote-accent shadow-2xl transition-all group-hover:rotate-12 group-hover:scale-110">3</div>
                <div className="bg-slate-100 dark:bg-slate-900/50 p-6 rounded-3xl w-fit mb-8 border border-slate-200 dark:border-white/10 transition-all group-hover:neo-glow">
                   <Files size={36} className="text-blue-500" />
                </div>
                <h3 className="text-2xl font-black mb-4 dark:text-white">Master Content</h3>
                <p className="text-slate-500 dark:text-slate-400 text-sm font-medium leading-loose">Interact with transcripts, download PDFs, and learn with chat.</p>
             </GlassCard>
          </div>
       </section>

       <Features />

       {/* DEMO PREVIEW SECTION (NEW) */}
       <section className="py-32 px-6 relative bg-slate-100/50 dark:bg-slate-950/40 border-y border-slate-200 dark:border-white/5">
          <div className="max-w-7xl mx-auto flex flex-col items-center">
             <div className="text-center mb-20">
                <h2 className="text-4xl md:text-6xl font-black mb-6 tracking-tight text-slate-900 dark:text-white">See Vynote in <span className="text-vynote-accent">Action</span></h2>
                <p className="text-slate-400 font-bold uppercase text-[10px] tracking-[0.5em]">Experience the interface</p>
             </div>

             <GlassCard className="max-w-6xl w-full p-2 md:p-4 bg-white/90 dark:bg-slate-900/60 border-slate-300 dark:border-white/10 shadow-[0_40px_100px_rgba(0,0,0,0.1)] dark:shadow-[0_40px_100px_rgba(139,92,246,0.1)]" hover={false}>
                <div className="h-6 md:h-8 w-full bg-slate-100 dark:bg-slate-950 flex items-center gap-2.5 px-6 border-b border-slate-200 dark:border-white/5 rounded-t-[1.8rem]">
                   <div className="w-3 h-3 rounded-full bg-red-400/50"></div>
                   <div className="w-3 h-3 rounded-full bg-yellow-400/50"></div>
                   <div className="w-3 h-3 rounded-full bg-green-400/50"></div>
                   <span className="ml-4 text-[10px] font-black uppercase text-slate-400 tracking-widest opacity-40">vynote-workspace.app</span>
                </div>
                <div className="relative overflow-hidden group">
                   <img 
                      src="/preview.png" 
                      alt="Vynote Workspace Preview" 
                      className="w-full rounded-b-3xl transition-transform duration-700 group-hover:scale-[1.02]"
                      onError={(e) => {
                          e.target.src = 'https://images.unsplash.com/photo-1516321497487-e288fb19a13f?auto=format&fit=crop&q=80&w=2070';
                          e.target.style.opacity = '0.5';
                      }}
                   />
                   <div className="absolute inset-0 bg-gradient-to-t from-slate-950/20 to-transparent pointer-events-none"></div>
                </div>
             </GlassCard>
          </div>
       </section>

       {/* CTA Section */}
       <section className="py-40 px-6 overflow-hidden relative">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-[600px] bg-vynote-accent/10 blur-[200px] pointer-events-none rounded-full dark:bg-violet-900/20"></div>
          <GlassCard className="max-w-5xl mx-auto p-12 md:p-24 text-center relative z-10 border-slate-200 dark:border-violet-500/20 shadow-2xl dark:shadow-violet-500/10 bg-white/70 dark:bg-slate-900/40">
             <h2 className="text-4xl md:text-7xl font-black mb-10 leading-tight text-slate-900 dark:text-white">Ready to <span className="text-vynote-accent">upgrade</span> your flow?</h2>
             <p className="text-slate-500 dark:text-slate-400 max-w-xl mx-auto mb-14 text-lg sm:text-xl font-medium leading-loose">Join 15,000+ students and researchers turning academic noise into knowledge with Vynote AI.</p>
             <Link to="/workspace">
               <button className="bg-slate-900 dark:bg-white text-white dark:text-slate-950 px-12 py-6 rounded-3xl text-xl font-black hover:bg-vynote-accent hover:text-white transition-all hover:scale-110 hover:-rotate-1 active:scale-95 shadow-2xl shadow-slate-900/20 dark:shadow-none">
                 Get Started Free
               </button>
             </Link>
          </GlassCard>
       </section>

       {/* Footer */}
       <footer className="py-24 px-6 border-t border-slate-200 dark:border-white/5 bg-white dark:bg-slate-950 relative overflow-hidden">
          <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-start justify-between gap-20 text-left">
             <div className="max-w-sm">
                <Link to="/" className="flex items-center gap-2.5 mb-8 group">
                   <div className="bg-vynote-accent p-2 rounded-xl">
                      <MonitorPlay size={20} className="text-white" />
                   </div>
                   <span className="text-2xl font-black tracking-tighter text-slate-900 dark:text-white">Vynote</span>
                </Link>
                <p className="text-slate-500 dark:text-slate-400 text-sm font-medium leading-loose">Capture the Unseen. Intelligent lecture understanding for the modern academic journey. Secure, local, and incredibly fast.</p>
             </div>

             <div className="grid grid-cols-2 sm:grid-cols-3 gap-20 md:gap-32">
                <div className="flex flex-col gap-6">
                   <h4 className="font-black text-slate-900 dark:text-white uppercase tracking-[0.2em] text-[10px]">Product</h4>
                   <Link to="/workspace" className="text-slate-500 hover:text-vynote-accent transition-colors text-sm font-bold">Workspace</Link>
                   <Link to="/chat" className="text-slate-500 hover:text-vynote-accent transition-colors text-sm font-bold">Chat AI</Link>
                   <Link to="/" className="text-slate-500 hover:text-vynote-accent transition-colors text-sm font-bold">Pricing</Link>
                </div>
                <div className="flex flex-col gap-6">
                   <h4 className="font-black text-slate-900 dark:text-white uppercase tracking-[0.2em] text-[10px]">Community</h4>
                   <a href="#" className="text-slate-500 hover:text-vynote-accent transition-colors text-sm font-bold underline decoration-slate-200 underline-offset-4">GitHub</a>
                   <a href="#" className="text-slate-500 hover:text-vynote-accent transition-colors text-sm font-bold underline decoration-slate-200 underline-offset-4">Discord</a>
                </div>
                <div className="flex flex-col gap-6">
                   <h4 className="font-black text-slate-900 dark:text-white uppercase tracking-[0.2em] text-[10px]">Legal</h4>
                   <Link to="/" className="text-slate-500 hover:text-vynote-accent transition-colors text-sm font-bold">Privacy</Link>
                   <Link to="/" className="text-slate-500 hover:text-vynote-accent transition-colors text-sm font-bold">Terms</Link>
                </div>
             </div>
          </div>
          <div className="max-w-7xl mx-auto pt-24 text-center border-t border-slate-200 dark:border-white/5 mt-20">
             <p className="text-slate-400 text-[10px] font-black uppercase tracking-[0.3em]">© 2026 Vynote AI Lab • San Francisco, CA</p>
          </div>
       </footer>

    </div>
  );
};

export default Home;
