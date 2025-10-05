import React from "react";

type Voice = { value: string; label: string };

type Props = {
  voices: Voice[];
  value: string;
  onChange: (value: string) => void;
};

const VOICE_DESCRIPTIONS: Record<string, string> = {
  fable: "Warm, narrative, engaging storyteller.",
  nova: "Crisp, modern, energetic female.",
  echo: "Deep, smooth, radio-style male.",
  sage: "Calm, wise, educational tone.",
  onyx: "Bold, dramatic, cinematic presence.",
  luna: "Friendly, conversational, approachable.",
};

export default function VoiceSelector({ voices, value, onChange }: Props) {
  return (
    <div className="flex flex-col gap-4">
      <label htmlFor="voice" className="font-semibold text-white text-lg">🎤 Voice Selection</label>
      
      <select
        id="voice"
        value={value}
        onChange={e => onChange(e.target.value)}
        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white focus:ring-2 focus:ring-primary-400 focus:outline-none cursor-pointer transition-all duration-300"
      >
        {voices.map(v => (
          <option key={v.value} value={v.value} className="bg-gray-800 text-white">{v.label}</option>
        ))}
      </select>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {voices.map(v => (
          <div
            key={v.value}
            className={`relative group p-4 rounded-2xl border transition-all duration-300 cursor-pointer hover-lift ${
              value === v.value 
                ? 'border-primary-400 bg-gradient-to-br from-primary-500/20 to-secondary-500/20 shadow-glow' 
                : 'border-white/20 bg-white/5 hover:border-primary-300/50'
            }`}
            onClick={() => onChange(v.value)}
            tabIndex={0}
            aria-label={v.label}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="font-semibold text-white text-sm">{v.label}</span>
              {value === v.value && (
                <div className="w-5 h-5 bg-primary-400 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs">✓</span>
                </div>
              )}
            </div>
            
            <div className="text-xs text-gray-300 line-clamp-2">
              {VOICE_DESCRIPTIONS[v.value] || 'Professional voice quality'}
            </div>
            
            {/* Tooltip on hover */}
            <div className="absolute left-1/2 -translate-x-1/2 -bottom-2 group-hover:flex hidden flex-col items-center z-20">
              <div className="w-max bg-gray-900/95 backdrop-blur-sm text-white text-xs rounded-lg px-3 py-2 shadow-2xl mt-2 opacity-95">
                {VOICE_DESCRIPTIONS[v.value]}
              </div>
              <div className="w-2 h-2 bg-gray-900/95 rotate-45 -mt-1" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

