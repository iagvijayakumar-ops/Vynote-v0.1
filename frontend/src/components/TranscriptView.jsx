import React, { useRef } from 'react';
import { Play, User, Users } from 'lucide-react';

const TranscriptView = ({ transcriptData, audioUrl }) => {
  const audioRef = useRef(null);

  if (!transcriptData || !transcriptData.detailed) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-12 text-center opacity-50 space-y-4">
        <Users size={48} className="text-slate-300" />
        <p className="max-w-[180px] text-xs font-bold uppercase tracking-widest leading-loose">Upload audio to begin transcription.</p>
      </div>
    );
  }

  const handleWordClick = (startTime) => {
    if (audioRef.current && startTime !== undefined) {
      audioRef.current.currentTime = startTime;
      audioRef.current.play().catch(e => console.error(e));
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-950/20 backdrop-blur-md">
      {/* Audio Player */}
      {audioUrl && (
        <div className="p-4 border-b border-white/5 bg-slate-900/40">
           <audio ref={audioRef} src={audioUrl} controls className="w-full h-8 brightness-110 contrast-125 invert dark:invert-0 opacity-80 hover:opacity-100 transition-opacity" />
        </div>
      )}

      {/* Transcript Text */}
      <div className="flex-1 overflow-y-auto px-6 py-8 space-y-6 scroll-smooth no-scrollbar">
        {transcriptData.detailed.map((item, index) => {
          const isLowConfidence = item.confidence < 0.8;
          const showSpeaker = index === 0 || item.speaker !== transcriptData.detailed[index - 1].speaker;

          return (
            <React.Fragment key={index}>
              {showSpeaker && (
                <div className="flex items-center gap-2 mt-8 mb-2 group">
                  <div className="p-1.5 rounded-lg bg-white/5 border border-white/10 group-hover:neo-glow transition-all">
                    <User size={12} className="text-vynote-accent" />
                  </div>
                   <span className="text-[10px] font-bold uppercase tracking-widest text-slate-500 group-hover:text-vynote-accent transition-colors">
                      {item.speaker}
                   </span>
                </div>
              )}

              <span 
                className={`inline-block px-1 py-0.5 rounded-md cursor-pointer transition-all duration-200 text-sm md:text-base leading-relaxed tracking-wide font-medium ${isLowConfidence ? 'bg-yellow-400/20 text-yellow-200 decoration-yellow-500/50 underline decoration-dotted' : 'text-slate-300 hover:text-white hover:bg-white/5'}`}
                onClick={() => handleWordClick(item.start_time)}
                title={`Confidence: ${Math.round(item.confidence * 100)}%`}
              >
                {item.word}{" "}
              </span>
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export default TranscriptView;
