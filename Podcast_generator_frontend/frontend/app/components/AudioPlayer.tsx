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
    <div className="w-full max-w-2xl mx-auto mt-8 glass-effect-strong shadow-2xl rounded-3xl p-6 animate-slide-up">
      {isLoading ? (
        <div className="flex flex-col items-center gap-4 py-8">
          <div className="relative">
            <div className="w-16 h-16 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full flex items-center justify-center animate-pulse-glow">
              <svg className="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
              </svg>
            </div>
            <div className="absolute -top-2 -right-2 w-6 h-6 bg-accent-400 rounded-full animate-bounce-subtle"></div>
          </div>
          <div className="text-center">
            <h3 className="text-lg font-semibold text-white mb-1">Generating Your Podcast</h3>
            <p className="text-gray-300 text-sm">Creating high-quality audio content...</p>
          </div>
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
          
          {/* Header */}
          <div className="text-center mb-6">
            <h3 className="text-xl font-bold text-white mb-2">🎧 Your Podcast is Ready!</h3>
            <p className="text-gray-300 text-sm">Listen to your generated podcast episode</p>
          </div>

          {/* Audio Controls */}
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <button
                type="button"
                className="w-14 h-14 bg-button-gradient rounded-2xl flex items-center justify-center shadow-glow hover:shadow-glow-purple transition-all duration-300 hover-lift"
                onClick={handlePlayPause}
              >
                {playing ? (
                  <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <rect x="6" y="4" width="4" height="16" rx="2"/>
                    <rect x="14" y="4" width="4" height="16" rx="2"/>
                  </svg>
                ) : (
                  <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <polygon points="5,3 19,12 5,21 5,3"/>
                  </svg>
                )}
              </button>
              
              <div className="flex-1 space-y-2">
                <input
                  type="range"
                  min={0}
                  max={duration || 1}
                  value={progress}
                  onChange={handleSeek}
                  className="w-full h-2 bg-white/20 rounded-full appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, #0ea5e9 0%, #6366f1 ${(progress / (duration || 1)) * 100}%, rgba(255,255,255,0.2) ${(progress / (duration || 1)) * 100}%, rgba(255,255,255,0.2) 100%)`
                  }}
                />
                <div className="flex justify-between text-xs text-gray-400">
                  <span>{formatTime(progress)}</span>
                  <span>{formatTime(duration)}</span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 justify-center">
              <a
                href={src}
                download
                className="px-6 py-3 bg-gradient-to-r from-accent-400 to-accent-500 text-white rounded-xl font-semibold hover:from-accent-500 hover:to-accent-600 transition-all duration-300 hover-lift shadow-glow"
                title="Download Podcast"
              >
                <span className="flex items-center gap-2">
                  <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path d="M12 5v14m0 0l-5-5m5 5l5-5"/>
                  </svg>
                  Download
                </span>
              </a>
              
              {onReset && (
                <button 
                  type="button" 
                  className="px-6 py-3 glass-effect text-white rounded-xl font-semibold hover:bg-white/20 transition-all duration-300 hover-lift"
                  onClick={onReset}
                >
                  <span className="flex items-center gap-2">
                    <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                      <path d="M1 4v6h6M23 20v-6h-6"/>
                      <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/>
                    </svg>
                    Reset
                  </span>
                </button>
              )}
            </div>
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

