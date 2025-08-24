export default function Portfolio() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-700 via-blue-700 to-indigo-900 text-white font-sans">
      {/* Header with Waves */}
      <header className="relative text-center py-16">
        <svg className="absolute top-0 left-0 w-full opacity-30" viewBox="0 0 1440 320">
          <path fill="#9333ea" d="M0,64L60,80C120,96,240,128,360,133.3C480,139,600,117,720,106.7C840,96,960,96,1080,117.3C1200,139,1320,181,1380,202.7L1440,224V0H0Z"/>
        </svg>
        <h1 className="relative text-5xl font-bold z-10">Nishanth G</h1>
        <p className="relative mt-3 text-lg text-blue-100 z-10">"The future belongs to those who prepare for it today."</p>
      </header>

  {/* About Me */}
      <section className="max-w-4xl mx-auto text-center bg-white/10 rounded-xl p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-3">About Me</h2>
        <p>I’m Nishanth, a passionate developer who loves building scalable and practical solutions. My focus is on simplicity, clean code, and solving real-world problems.</p>
      </section>

  {/* Tech Stack */}
      <section className="max-w-4xl mx-auto bg-white/10 rounded-xl p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-3">Tech Stack</h2>
        <div className="flex flex-wrap justify-center gap-3">
          {["Python", "Java", "C", "R", "Android Studio", "VS Code", "GitHub"].map(skill => (
            <span key={skill} className="px-3 py-1 bg-gradient-to-r from-pink-500 to-yellow-500 rounded-full text-sm font-medium">{skill}</span>
          ))}
        </div>
      </section>

  {/* Featured Project */}
      <section className="max-w-4xl mx-auto bg-white/10 rounded-xl p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-3">Featured Project</h2>
        <p><b>AgriRenew</b> – A smart bio-waste intelligence platform that uses AI to forecast residue, grade quality via mobile, and create decentralized micro-biogas units.</p>
      </section>

  {/* GitHub Stats */}
      <section className="max-w-4xl mx-auto text-center bg-white/10 rounded-xl p-6">
        <h2 className="text-2xl font-semibold mb-3">GitHub Insights</h2>
        <img src="https://github-readme-stats.vercel.app/api?username=Nishanth6153&show_icons=true&theme=tokyonight" alt="GitHub Stats" className="mx-auto"/>
      </section>

  {/* Footer */}
      <footer className="text-center py-4 mt-8 text-sm text-blue-200">© {new Date().getFullYear()} Nishanth G</footer>
    </div>
  );
}
