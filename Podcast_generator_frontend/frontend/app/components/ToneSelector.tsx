import React from "react";

type Tone = { value: string; label: string };

type Props = {
  tones: Tone[];
  value: string;
  onChange: (value: string) => void;
};

const TONE_DESCRIPTIONS: Record<string, string> = {
  storytelling: "Engaging, narrative-driven style.",
  inspirational: "Uplifting and motivational.",
  educational: "Clear, informative, and structured.",
  conversational: "Relaxed, friendly, and informal.",
  news: "Neutral, factual, and concise.",
  humorous: "Light-hearted, witty, and fun.",
};

export default function ToneSelector({ tones, value, onChange }: Props) {
  return (
    <div className="flex flex-col gap-4">
      <label htmlFor="tone" className="font-semibold text-white text-lg">🎭 Tone Selection</label>
      
      <select
        id="tone"
        value={value}
        onChange={e => onChange(e.target.value)}
        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white focus:ring-2 focus:ring-secondary-400 focus:outline-none cursor-pointer transition-all duration-300"
      >
        {tones.map(t => (
          <option key={t.value} value={t.value} className="bg-gray-800 text-white">{t.label}</option>
        ))}
      </select>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {tones.map(t => (
          <div
            key={t.value}
            className={`relative group p-4 rounded-2xl border transition-all duration-300 cursor-pointer hover-lift ${
              value === t.value 
                ? 'border-secondary-400 bg-gradient-to-br from-secondary-500/20 to-accent-500/20 shadow-glowPurple' 
                : 'border-white/20 bg-white/5 hover:border-secondary-300/50'
            }`}
            onClick={() => onChange(t.value)}
            tabIndex={0}
            aria-label={t.label}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-white text-sm">{t.label}</span>
              {value === t.value && (
                <div className="w-5 h-5 bg-secondary-400 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs">✓</span>
                </div>
              )}
            </div>
            
            <div className="text-xs text-gray-300 line-clamp-2">
              {TONE_DESCRIPTIONS[t.value] || 'Professional tone quality'}
            </div>
            
            {/* Tooltip on hover */}
            <div className="absolute left-1/2 -translate-x-1/2 -bottom-2 group-hover:flex hidden flex-col items-center z-20">
              <div className="w-max bg-gray-900/95 backdrop-blur-sm text-white text-xs rounded-lg px-3 py-2 shadow-2xl mt-2 opacity-95">
                {TONE_DESCRIPTIONS[t.value]}
              </div>
              <div className="w-2 h-2 bg-gray-900/95 rotate-45 -mt-1" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

