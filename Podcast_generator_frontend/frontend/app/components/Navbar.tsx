"use client"
import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { useRouter } from 'next/navigation';

const Navbar = ({creditsPopup,setCreditsPopup}: {creditsPopup: boolean, setCreditsPopup: (value: boolean) => void}) => {
    const router = useRouter();
    const [loggedin,setLoggedin] = useState(false);
    const token = Cookies.get("token");

    const storedCredits = localStorage.getItem("credits")
    useEffect(() => {

        if (!token) {
            router.push("/login");
            return;
        }
        setLoggedin(true);
    }, [router,loggedin,token]);

  return (
    
    loggedin && (
    <header className="flex items-center justify-between sticky top-0 z-30 w-full glass-effect-strong shadow-2xl border-b border-white/20 animate-slide-down">
      <div className="flex items-center justify-between gap-6 px-6 py-4 bg-black rounded-lg shadow-md max-w-md mx-auto">
  {/* Credits Display */}
  <div className="flex flex-col">
    <span className="text-sm text-gray-400">Credits</span>
    <span className="text-2xl font-bold text-white">{storedCredits}</span>
  </div>

  {/* Add Credits Button */}
  <button
    onClick={() => setCreditsPopup(true)}
    className="inline-flex items-center gap-2 px-5 py-2.5 
               bg-white text-black font-medium rounded-md 
               hover:bg-gray-200 active:scale-95 transition-all"
  >
    💳 Add
  </button>
</div>


        
        <div className="flex items-center gap-4 py-4 px-6">
          <div className="w-12 h-12 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-2xl shadow-glow flex items-center justify-center">
            <span className="text-white font-bold text-xl">🎙️</span>
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-white">Podcast Generator</h1>
            <p className="text-gray-200 text-sm font-normal">Create amazing podcasts with AI</p>
          </div>
        </div>

        <button 
          className="mx-4 px-6 py-3 glass-effect text-white rounded-xl font-semibold hover:bg-white/20 transition-all duration-300 hover-lift" 
          onClick={() => {
            Cookies.remove("token");
            setLoggedin(false);
            router.push("/login");
          }}
        >
          🚪 Logout
        </button>
    </header>
    )
  );
};

export default Navbar;
