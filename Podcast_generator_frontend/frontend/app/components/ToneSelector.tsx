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
    <div className="flex flex-col gap-1">
      <label htmlFor="tone" className="font-medium text-gray-700">Tone</label>
      <select
        id="tone"
        value={value}
        onChange={e => onChange(e.target.value)}
        className="w-full px-4 py-2 rounded-xl border border-gray-200 bg-gray-50 focus:ring-2 focus:ring-indigo-400 focus:outline-none cursor-pointer"
      >
        {tones.map(t => (
          <option key={t.value} value={t.value}>{t.label}</option>
        ))}
      </select>
      <div className="mt-2 flex flex-wrap gap-2">
        {tones.map(t => (
          <div
            key={t.value}
            className={`relative group flex-1 min-w-[110px] p-3 rounded-xl border ${value === t.value ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200 bg-white'} shadow-soft cursor-pointer transition hover:border-indigo-400`}
            onClick={() => onChange(t.value)}
            tabIndex={0}
            aria-label={t.label}
          >
            <span className="font-semibold text-indigo-700">{t.label}</span>
            <span className="ml-1 text-xs text-gray-400">{value === t.value ? '✓' : ''}</span>
            <div className="absolute left-1/2 -translate-x-1/2 -bottom-2 group-hover:flex hidden flex-col items-center z-20">
              <div className="w-max bg-gray-900 text-white text-xs rounded px-3 py-2 shadow-lg mt-2 opacity-90">
                {TONE_DESCRIPTIONS[t.value]}
              </div>
              <div className="w-3 h-3 bg-gray-900 rotate-45 -mt-1" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

