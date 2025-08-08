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
    <div className="flex flex-col gap-1">
      <label htmlFor="voice" className="font-medium text-gray-700">Voice</label>
      <select
        id="voice"
        value={value}
        onChange={e => onChange(e.target.value)}
        className="w-full px-4 py-2 rounded-xl border border-gray-200 bg-gray-50 focus:ring-2 focus:ring-indigo-400 focus:outline-none cursor-pointer"
      >
        {voices.map(v => (
          <option key={v.value} value={v.value}>{v.label}</option>
        ))}
      </select>
      <div className="mt-2 flex flex-wrap gap-2">
        {voices.map(v => (
          <div
            key={v.value}
            className={`relative group flex-1 min-w-[110px] p-3 rounded-xl border ${value === v.value ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 bg-white'} shadow-soft cursor-pointer transition hover:border-indigo-400`}
            onClick={() => onChange(v.value)}
            tabIndex={0}
            aria-label={v.label}
          >
            <span className="font-semibold text-indigo-700">{v.label}</span>
            <span className="ml-1 text-xs text-gray-400">{value === v.value ? '✓' : ''}</span>
            <div className="absolute left-1/2 -translate-x-1/2 -bottom-2 group-hover:flex hidden flex-col items-center z-20">
              <div className="w-max bg-gray-900 text-white text-xs rounded px-3 py-2 shadow-lg mt-2 opacity-90">
                {VOICE_DESCRIPTIONS[v.value]}
              </div>
              <div className="w-3 h-3 bg-gray-900 rotate-45 -mt-1" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

