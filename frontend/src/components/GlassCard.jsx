import React from 'react';

const GlassCard = ({ children, className = "", hover = true }) => {
  return (
    <div className={`
      relative overflow-hidden
      backdrop-blur-md transition-all duration-300
      rounded-2xl border
      /* Light Mode */
      bg-white/70 border-slate-200 shadow-lg text-slate-800
      /* Dark Mode */
      dark:bg-slate-900/40 dark:border-white/10 dark:text-white dark:shadow-none
      ${hover ? 'hover:-translate-y-1 hover:shadow-xl dark:hover:shadow-purple-500/10 dark:hover:border-vynote-accent/30' : ''}
      ${className}
    `}>
      {children}
    </div>
  );
};

export default GlassCard;
