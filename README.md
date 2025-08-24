import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { Github, Mail, ExternalLink, Code2, LayoutGrid, BarChart3 } from "lucide-react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

// ======= QUICK CONFIG =======
const USERNAME = "Nishanth6153"; // <-- set your GitHub username
// =============================

export default function Portfolio() {
  const [repos, setRepos] = useState([]);
  const [langCounts, setLangCounts] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const r = await fetch(`https://api.github.com/users/${USERNAME}/repos?per_page=100`);
        const data = await r.json();
        if (Array.isArray(data)) {
          setRepos(data);
          const counts = {};
          for (const repo of data) {
            const lang = repo.language || "Other";
            counts[lang] = (counts[lang] || 0) + 1;
          }
          setLangCounts(counts);
        }
      } catch (e) {
        // graceful fallback
        setRepos([]);
        setLangCounts({ Python: 5, Java: 3, C: 2, R: 2, Other: 1 });
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const chartData = useMemo(() => {
    const labels = Object.keys(langCounts);
    const values = Object.values(langCounts);
    return {
      labels,
      datasets: [
        {
          label: "Repos",
          data: values,
          // don't set explicit colors in user-visible charts by default, but here it's a UI app so we add a palette
          backgroundColor: [
            "#60a5fa", // blue-400
            "#34d399", // emerald-400
            "#f472b6", // pink-400
            "#fbbf24", // amber-400
            "#c084fc", // violet-400
            "#4ade80", // green-400
            "#22d3ee", // cyan-400
          ],
          borderWidth: 0,
        },
      ],
    };
  }, [langCounts]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-sky-900 text-white">
      {/* HERO with multi-layer waves */}
      <section className="relative overflow-hidden">
        {/* Wave Layers */}
        <Waves />
        <div className="relative z-10 max-w-6xl mx-auto px-6 pt-28 pb-20 text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-5xl md:text-6xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-sky-200 to-indigo-200 drop-shadow"
          >
            Nishanth G
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15, duration: 0.6 }}
            className="mt-4 text-lg md:text-xl text-sky-100/90"
          >
            "The future belongs to those who prepare for it today."
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
            className="mt-8 flex items-center justify-center gap-4"
          >
            <a
              className="inline-flex items-center gap-2 rounded-2xl px-5 py-3 bg-gradient-to-r from-fuchsia-500 to-purple-500 hover:from-fuchsia-400 hover:to-purple-400 transition-all shadow-lg"
              href={`https://github.com/${USERNAME}`}
              target="_blank"
              rel="noreferrer"
            >
              <Github className="w-5 h-5" /> GitHub
            </a>
            <a
              className="inline-flex items-center gap-2 rounded-2xl px-5 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 transition-all shadow-lg"
              href="mailto:your-email@example.com"
            >
              <Mail className="w-5 h-5" /> Email
            </a>
          </motion.div>
        </div>
      </section>

      {/* ABOUT */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <SectionTitle icon={<LayoutGrid className="w-6 h-6" />} title="About Me" />
        <div className="grid md:grid-cols-3 gap-6 mt-6">
          <Card className="md:col-span-2 bg-gradient-to-br from-indigo-700/60 to-sky-700/40">
            <p className="leading-7 text-slate-100/90">
              I build practical, scalable software with a bias for simplicity and clarity. I enjoy turning ideas into production-grade systems and shipping fast without breaking quality. Strong focus on clean code, accessibility, and resilient UX.
            </p>
          </Card>
          <Card className="bg-gradient-to-br from-fuchsia-600/50 to-violet-700/40">
            <p className="leading-7 text-slate-100/90">
              Currently exploring colorful data visualizations, developer tooling, and sustainable tech that solves real problems for real people.
            </p>
          </Card>
        </div>
      </section>

      {/* TECH STACK */}
      <section className="max-w-6xl mx-auto px-6 pb-4">
        <SectionTitle icon={<Code2 className="w-6 h-6" />} title="Tech Stack" />
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
          <PillCard title="Languages" pills={["Python", "Java", "C", "R"]} gradient="from-cyan-500 to-blue-500" />
          <PillCard title="Tools" pills={["Android Studio", "VS Code", "Git/GitHub"]} gradient="from-fuchsia-500 to-pink-500" />
          <PillCard title="Focus Areas" pills={["Web Apps", "App Dev", "Data Viz"]} gradient="from-emerald-500 to-lime-500" />
        </div>
      </section>

      {/* PROJECTS */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <SectionTitle icon={<ExternalLink className="w-6 h-6" />} title="Featured Project" />
        <div className="grid lg:grid-cols-2 gap-6 mt-6">
          <ProjectCard
            title="AgriRenew: Smart Bio‑Waste Intelligence Platform"
            summary="AI-assisted forecasting (satellite + weather), mobile quality grading, and decentralized micro‑processing to turn residue into revenue. Offline-ready and local-language friendly."
            href="#"
            tags={["Prediction", "Computer Vision", "Sustainability"]}
            gradient="from-violet-600 to-indigo-600"
          />
          <Card className="bg-gradient-to-br from-emerald-600/60 to-teal-600/40">
            <h4 className="text-xl font-semibold">What makes it different</h4>
            <ul className="mt-3 space-y-2 list-disc list-inside text-slate-100/90">
              <li>No expensive IoT—leverages open data and phone cameras.</li>
              <li>Community incentives and marketplace hooks for circular economy.</li>
              <li>Portable micro-units enable hub-and-spoke operations.</li>
            </ul>
          </Card>
        </div>
      </section>

      {/* GITHUB INSIGHTS */}
      <section className="max-w-6xl mx-auto px-6 pb-24">
        <SectionTitle icon={<BarChart3 className="w-6 h-6" />} title="GitHub Insights" />
        <div className="grid md:grid-cols-2 gap-6 mt-6">
          <Card className="bg-gradient-to-br from-sky-700/50 to-indigo-700/50">
            <h4 className="text-lg font-semibold mb-4">Language Spread</h4>
            <div className="max-w-xs mx-auto">
              <Doughnut data={chartData} options={{ plugins: { legend: { labels: { color: "#e5e7eb" } } } }} />
            </div>
            <p className="mt-4 text-sm text-slate-200/80">Data derived from your public repositories.</p>
          </Card>
          <Card className="bg-gradient-to-br from-fuchsia-700/50 to-pink-700/50">
            <h4 className="text-lg font-semibold mb-4">Pinned Repositories</h4>
            {loading ? (
              <p className="text-slate-200/80">Loading…</p>
            ) : (
              <div className="space-y-3">
                {repos.slice(0, 5).map((r) => (
                  <a
                    key={r.id}
                    href={r.html_url}
                    target="_blank"
                    rel="noreferrer"
                    className="block rounded-xl bg-white/10 hover:bg-white/15 transition p-4"
                  >
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <h5 className="font-semibold">{r.name}</h5>
                        <p className="text-sm text-slate-200/80 line-clamp-2">{r.description || "No description"}</p>
                      </div>
                      <ExternalLink className="w-4 h-4 shrink-0" />
                    </div>
                  </a>
                ))}
              </div>
            )}
          </Card>
        </div>
      </section>

      {/* FOOTER RIBBON */}
      <footer className="relative">
        <Ribbon />
        <div className="text-center py-6 text-slate-300 text-sm">
          © {new Date().getFullYear()} Nishanth G — Crafted with React, Tailwind, Framer Motion & Chart.js
        </div>
      </footer>
    </div>
  );
}

function SectionTitle({ icon, title }) {
  return (
    <div className="flex items-center gap-3">
      <div className="p-2 rounded-xl bg-white/10 backdrop-blur ring-1 ring-white/10">{icon}</div>
      <h3 className="text-2xl font-bold tracking-tight">{title}</h3>
      <div className="h-px flex-1 bg-gradient-to-r from-fuchsia-400/60 via-cyan-300/60 to-emerald-300/60" />
    </div>
  );
}

function Card({ children, className = "" }) {
  return (
    <div className={`rounded-2xl p-6 shadow-xl ring-1 ring-white/10 backdrop-blur ${className}`}>
      {children}
    </div>
  );
}

function PillCard({ title, pills, gradient }) {
  return (
    <Card className={`bg-gradient-to-br ${gradient} bg-opacity-30`}> 
      <h4 className="text-xl font-semibold mb-4">{title}</h4>
      <div className="flex flex-wrap gap-3">
        {pills.map((p) => (
          <span key={p} className="px-3 py-1 rounded-full text-sm font-medium bg-black/20 ring-1 ring-white/20">
            {p}
          </span>
        ))}
      </div>
    </Card>
  );
}

function ProjectCard({ title, summary, tags, href, gradient }) {
  return (
    <Card className={`bg-gradient-to-br ${gradient} `}>
      <h4 className="text-2xl font-semibold">{title}</h4>
      <p className="mt-2 text-slate-100/90">{summary}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {tags.map((t) => (
          <span key={t} className="text-xs px-2 py-1 rounded-full bg-white/15 ring-1 ring-white/20">{t}</span>
        ))}
      </div>
      <div className="mt-6">
        <a href={href} className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-black/30 hover:bg-black/40 transition ring-1 ring-white/20" target="_blank" rel="noreferrer">
          <ExternalLink className="w-4 h-4" /> View project
        </a>
      </div>
    </Card>
  );
}

// Layered SVG waves for a unique hero
function Waves() {
  return (
    <div className="absolute inset-0">
      <svg className="absolute -top-20 left-0 w-[140%] md:w-full opacity-40" viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
        <path fill="#38bdf8" d="M0,160L60,181.3C120,203,240,245,360,234.7C480,224,600,160,720,138.7C840,117,960,139,1080,149.3C1200,160,1320,160,1380,160L1440,160L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z" />
      </svg>
      <svg className="absolute -top-10 left-0 w-[140%] md:w-full opacity-50" viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
        <path fill="#a78bfa" d="M0,256L60,229.3C120,203,240,149,360,128C480,107,600,117,720,128C840,139,960,149,1080,133.3C1200,117,1320,75,1380,53.3L1440,32L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z" />
      </svg>
      <svg className="absolute -top-6 left-0 w-[140%] md:w-full opacity-60" viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg">
        <path fill="#f472b6" d="M0,64L60,85.3C120,107,240,149,360,165.3C480,181,600,171,720,176C840,181,960,203,1080,218.7C1200,235,1320,245,1380,250.7L1440,256L1440,0L1380,0C1320,0,1200,0,1080,0C960,0,840,0,720,0C600,0,480,0,360,0C240,0,120,0,60,0L0,0Z" />
      </svg>
    </div>
  );
}

// Color ribbon footer
function Ribbon() {
  return (
    <div className="h-2 bg-gradient-to-r from-fuchsia-400 via-cyan-300 to-emerald-300" />
  );
}
