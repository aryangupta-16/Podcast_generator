import PodcastForm from "./components/PodcastForm";

export default function HomePage() {
  return (
    <section className="w-full max-w-2xl mx-auto flex flex-col items-center gap-10 py-12">
      <div className="w-full text-center flex flex-col gap-3">
        <h2 className="text-3xl sm:text-4xl font-bold tracking-tight mb-2">Create your own AI-powered podcast</h2>
        <p className="text-gray-500 text-base sm:text-lg font-normal max-w-xl mx-auto">
          Instantly generate a high-quality podcast episode on any topic, in your favorite voice and tone. Powered by state-of-the-art AI.
        </p>
      </div>
      <PodcastForm />
    </section>
  );
}
