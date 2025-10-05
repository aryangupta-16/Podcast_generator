import Link from "next/link";

export default function HomePage() {
  return (
    <section className="w-full max-w-4xl mx-auto flex flex-col items-center gap-12 py-16 animate-fade-in">
      {/* Hero Section */}
      <div className="w-full text-center flex flex-col gap-6 animate-slide-up">
        <div className="relative">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight mb-4">
            <span className="text-gradient">Podcast</span>
            <br />
            <span className="text-white">Generator</span>
          </h1>
          <div className="absolute -top-4 -right-4 w-8 h-8 bg-gradient-to-r from-primary-400 to-secondary-400 rounded-full animate-bounce-subtle"></div>
          <div className="absolute -bottom-2 -left-2 w-6 h-6 bg-gradient-to-r from-accent-400 to-primary-400 rounded-full animate-bounce-subtle animate-delay-200"></div>
        </div>
        
        <p className="text-gray-200 text-lg sm:text-xl font-normal max-w-2xl mx-auto leading-relaxed">
          Transform any idea into a professional podcast episode in minutes. 
          Choose your voice, tone, and duration. Powered by cutting-edge AI technology.
        </p>
        
        {/* Feature badges */}
        <div className="flex flex-wrap justify-center gap-3 mt-6">
          <span className="glass-effect px-4 py-2 rounded-full text-sm font-medium text-white">
            🎙️ AI-Powered Voice
          </span>
          <span className="glass-effect px-4 py-2 rounded-full text-sm font-medium text-white">
            ⚡ Instant Generation
          </span>
          <span className="glass-effect px-4 py-2 rounded-full text-sm font-medium text-white">
            🎨 Multiple Tones
          </span>
          <span className="glass-effect px-4 py-2 rounded-full text-sm font-medium text-white">
            📱 High Quality Audio
          </span>
        </div>
      </div>

      {/* CTA Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8 animate-slide-up animate-delay-200">
        <Link 
          href="/login" 
          className="group relative bg-button-gradient text-white px-8 py-4 rounded-2xl font-semibold text-lg shadow-glow hover:shadow-glow-purple transition-all duration-300 hover-lift min-w-[160px] text-center"
        >
          <span className="relative z-10">Get Started</span>
          <div className="absolute inset-0 bg-button-gradient-hover rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </Link>
        
        <Link 
          href="/signup" 
          className="group glass-effect-strong text-white px-8 py-4 rounded-2xl font-semibold text-lg hover:bg-white/20 transition-all duration-300 hover-lift min-w-[160px] text-center"
        >
          <span className="relative z-10">Create Account</span>
        </Link>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-2xl mt-16 animate-slide-up animate-delay-300">
        <div className="glass-effect p-6 rounded-2xl text-center hover-lift">
          <div className="text-3xl font-bold text-gradient mb-2">10K+</div>
          <div className="text-gray-200 text-sm">Podcasts Generated</div>
        </div>
        <div className="glass-effect p-6 rounded-2xl text-center hover-lift">
          <div className="text-3xl font-bold text-gradient-purple mb-2">6</div>
          <div className="text-gray-200 text-sm">Voice Options</div>
        </div>
        <div className="glass-effect p-6 rounded-2xl text-center hover-lift">
          <div className="text-3xl font-bold text-gradient mb-2">99%</div>
          <div className="text-gray-200 text-sm">User Satisfaction</div>
        </div>
      </div>
    </section>
  );
}
