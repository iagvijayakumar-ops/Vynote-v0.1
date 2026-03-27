import React, { useState, useRef } from 'react';
import axios from 'axios';
import { PlayCircle, Youtube, CloudUpload } from 'lucide-react';

const API_BASE = 'http://localhost:5000/api';

const AudioIngestion = ({ setTranscriptData, setAudioUrl, setLoading }) => {
  const [file, setFile] = useState(null);
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const fileInputRef = useRef(null);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const url = URL.createObjectURL(file);
    setAudioUrl(url);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_BASE}/audio/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setTranscriptData(res.data);
    } catch (err) {
      console.error(err);
      alert("Error transcribing file. Is backend on port 5000?");
    } finally {
      setLoading(false);
    }
  };

  const handleYoutubeIngest = async (e) => {
    e.preventDefault();
    if (!youtubeUrl) return;

    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/audio/youtube`, { url: youtubeUrl });
      setTranscriptData(res.data);
    } catch (err) {
      console.error(err);
      alert("Error processing YouTube URL. Make sure yt-dlp is installed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col md:flex-row items-center gap-4 flex-1">
      {/* File Upload */}
      <form onSubmit={handleFileUpload} className="relative flex-1 flex items-center bg-white/5 border border-white/10 p-1.5 rounded-2xl group focus-within:ring-2 focus-within:ring-violet-500/50 transition-all">
        <div className="pl-4 text-slate-500 group-hover:text-violet-400 transition-colors">
           <CloudUpload size={18} />
        </div>
        <input 
          type="file" 
          accept="audio/*" 
          onChange={(e) => setFile(e.target.files[0])}
          ref={fileInputRef}
          className="flex-1 bg-transparent border-none outline-none text-sm text-slate-300 px-3 cursor-pointer file:hidden"
        />
        <button type="submit" disabled={!file} className="bg-vynote-accent hover:bg-violet-600 disabled:opacity-50 px-4 py-2 rounded-xl text-xs font-bold text-white transition-all hover:scale-105 active:scale-95 shadow-lg shadow-violet-500/30 flex items-center gap-2">
           <PlayCircle size={14}/> {file ? "Process" : "Upload"}
        </button>
      </form>

      {/* YouTube URL */}
      <form onSubmit={handleYoutubeIngest} className="relative flex-1 flex items-center bg-white/5 border border-white/10 p-1.5 rounded-2xl group focus-within:ring-2 focus-within:ring-red-500/50 transition-all">
        <div className="pl-4 text-slate-500 group-hover:text-red-400 transition-colors">
           <Youtube size={18} />
        </div>
        <input 
          type="url" 
          placeholder="Paste YouTube Link..." 
          value={youtubeUrl}
          onChange={(e) => setYoutubeUrl(e.target.value)}
          className="flex-1 bg-transparent border-none outline-none text-sm text-slate-300 px-3 placeholder:text-slate-600 font-medium"
        />
        <button type="submit" disabled={!youtubeUrl} className="bg-red-500 hover:bg-red-600 disabled:opacity-50 px-4 py-2 rounded-xl text-xs font-bold text-white transition-all hover:scale-105 active:scale-95 shadow-lg shadow-red-500/30 flex items-center gap-2">
          Sync Video
        </button>
      </form>
    </div>
  );
};

export default AudioIngestion;
