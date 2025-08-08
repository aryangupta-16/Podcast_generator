import React, { useRef, useState, useEffect } from "react";

type Props = {
  src?: string;
  isLoading?: boolean;
  onReset?: () => void;
};

export default function AudioPlayer({ src, isLoading, onReset }: Props) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    if (!src) {
      setPlaying(false);
      setProgress(0);
      setDuration(0);
    }
  }, [src]);

  const handlePlayPause = () => {
    if (!audioRef.current) return;
    if (playing) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setPlaying(!playing);
  };

  const handleTimeUpdate = () => {
    if (!audioRef.current) return;
    setProgress(audioRef.current.currentTime);
  };

  const handleLoadedMetadata = () => {
    if (!audioRef.current) return;
    setDuration(audioRef.current.duration);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!audioRef.current) return;
    const val = Number(e.target.value);
    audioRef.current.currentTime = val;
    setProgress(val);
  };

  if (!src && !isLoading) return null;

  return (
    <div className="w-full max-w-xl mx-auto mt-8 bg-white shadow-soft rounded-2xl p-4 flex flex-col gap-3 items-center">
      {isLoading ? (
        <div className="flex flex-col items-center gap-2 py-6">
          <svg className="animate-spin h-8 w-8 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
          <span className="text-gray-500">Generating podcast audio...</span>
        </div>
      ) : src ? (
        <>
          <audio
            ref={audioRef}
            src={src}
            preload="auto"
            onTimeUpdate={handleTimeUpdate}
            onLoadedMetadata={handleLoadedMetadata}
            className="hidden"
            onEnded={() => setPlaying(false)}
          />
          <div className="flex items-center gap-4 w-full">
            <button
              type="button"
              className="rounded-full bg-indigo-600 text-white w-12 h-12 flex items-center justify-center shadow-soft hover:bg-indigo-700 transition"
              onClick={handlePlayPause}
            >
              {playing ? (
                <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16" rx="2"/><rect x="14" y="4" width="4" height="16" rx="2"/></svg>
              ) : (
                <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21 5,3"/></svg>
              )}
            </button>
            <input
              type="range"
              min={0}
              max={duration || 1}
              value={progress}
              onChange={handleSeek}
              className="flex-1 accent-indigo-500 h-2 cursor-pointer"
            />
            <span className="text-xs text-gray-500 w-16 text-right">
              {formatTime(progress)} / {formatTime(duration)}
            </span>
            <a
              href={src}
              download
              className="ml-2 px-3 py-2 rounded-xl bg-gray-100 text-indigo-600 font-medium hover:bg-indigo-200 transition"
              title="Download Podcast"
            >
              <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 5v14m0 0l-5-5m5 5l5-5"/></svg>
            </a>
            {onReset && (
              <button type="button" className="ml-2 px-3 py-2 rounded-xl bg-gray-100 text-gray-600 font-medium hover:bg-gray-200 transition" onClick={onReset}>Reset</button>
            )}
          </div>
        </>
      ) : null}
    </div>
  );
}

function formatTime(sec: number) {
  if (!isFinite(sec)) return "0:00";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

