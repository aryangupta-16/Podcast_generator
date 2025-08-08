"use client"

import React, { useState } from "react";
import VoiceSelector from "./VoiceSelector";
import ToneSelector from "./ToneSelector";
import AudioPlayer from "./AudioPlayer";
import axios from "axios";
import toast, { Toaster } from "react-hot-toast";

const DUMMY_VOICES = [
  { value: "fable", label: "Fable" },
  { value: "nova", label: "Nova" },
  { value: "echo", label: "Echo" },
  { value: "shimmer", label: "Shimmer" },
  { value: "onyx", label: "Onyx" },
  { value: "alloy", label: "Alloy" },
];
const DUMMY_TONES = [
  { value: "storytelling", label: "Storytelling" },
  { value: "entertaining", label: "Entertaining" },
  { value: "educational", label: "Educational" },
  { value: "conversational", label: "Conversational" },
  { value: "casual", label: "Casual" },
  { value: "professional", label: "Professional" },
];

const BACKEND_URL = "http://localhost:8000";

export default function PodcastForm() {
  const [topic, setTopic] = useState("");
  const [voice, setVoice] = useState(DUMMY_VOICES[0].value);
  const [tone, setTone] = useState(DUMMY_TONES[0].value);
  const [duration, setDuration] = useState(5);
  const [loading, setLoading] = useState(false);
  const [audioPath, setAudioPath] = useState<string | undefined>();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAudioPath(undefined);
    try {
      const res = await axios.post(
        `${BACKEND_URL}/api/v1/generate-podcast`,
        {
          topic,
          tone,
          voice,
          duration_minutes: duration,
        },
        { timeout: 180000 }
      );
      if (res.data && res.data.success && res.data.audio_file_path) {
        console.log(res.data.audio_file_path);
        console.log(res.data);
        setAudioPath(`${BACKEND_URL}/api/v1/download/${res.data.audio_file_path}`);
        toast.success("Podcast generated!");
      } else {
        toast.error("Failed to generate podcast. Try again.");
      }
    } catch (err: any) {
      toast.error("Error generating podcast. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAudioPath(undefined);
    setTopic("");
    setVoice(DUMMY_VOICES[0].value);
    setTone(DUMMY_TONES[0].value);
    setDuration(5);
  };

  return (
    <>
      <Toaster position="top-right" />
      <form
        className="w-full bg-white shadow-soft rounded-2xl p-6 flex flex-col gap-6"
        onSubmit={handleSubmit}
      >
        <div className="flex flex-col gap-2">
          <label htmlFor="topic" className="font-medium text-gray-700">Podcast Topic</label>
          <input
            id="topic"
            type="text"
            required
            value={topic}
            onChange={e => setTopic(e.target.value)}
            placeholder="E.g. How AI will change travel"
            className="px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-400 focus:outline-none bg-gray-50"
          />
        </div>
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <VoiceSelector voices={DUMMY_VOICES} value={voice} onChange={setVoice} />
          </div>
          <div className="flex-1">
            <ToneSelector tones={DUMMY_TONES} value={tone} onChange={setTone} />
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="duration" className="font-medium text-gray-700">Duration: <span className="text-indigo-600 font-semibold">{duration} min</span></label>
          <input
            id="duration"
            type="range"
            min={1}
            max={10}
            value={duration}
            onChange={e => setDuration(Number(e.target.value))}
            className="w-full accent-indigo-500"
          />
        </div>
        <button
          type="submit"
          className="w-full py-3 rounded-xl bg-indigo-600 text-white font-semibold shadow-soft transition hover:bg-indigo-700 active:scale-95 disabled:opacity-60 disabled:cursor-not-allowed"
          disabled={loading}
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
              Generating Podcast...
            </span>
          ) : (
            <>Generate Podcast</>
          )}
        </button>
      </form>
      <AudioPlayer src={audioPath} isLoading={loading} onReset={audioPath ? handleReset : undefined} />
    </>
  );
}

