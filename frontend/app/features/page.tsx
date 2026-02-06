'use client'

import { motion } from 'framer-motion'
import { Cpu, Search, Zap, Shield, Globe, BarChart, Database, Zap as Bolt, Target, Brain, Share2, Layers } from 'lucide-react'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export default function FeaturesPage() {
    const features = [
        {
            title: "Neuro-Semantic Logic",
            desc: "Beyond keywords. We analyze the underlying intent and semantic connections that search engines actually value.",
            icon: Brain,
            color: "text-purple-500"
        },
        {
            title: "Titan ML 2.10 Engine",
            desc: "12-step deep learning pipeline including GNNs and RL Agents for predictive ranking forensics.",
            icon: Cpu,
            color: "text-blue-500"
        },
        {
            title: "Competitor Forensics",
            desc: "Reverse-engineer the top 10 SERP results. See their content gaps, entity density, and structure logic.",
            icon: Search,
            color: "text-orange-500"
        },
        {
            title: "Answer Engine Ops (AEO)",
            desc: "Optimize for the 'Zero-Click' future. Win featured snippets and AI overviews (SGE) with specific formatting.",
            icon: Bolt,
            color: "text-yellow-500"
        },
        {
            title: "Generative Engine Ops (GEO)",
            desc: "Ensure your brand is cited and trusted by LLMs like ChatGPT, Perplexity, and Gemini.",
            icon: Globe,
            color: "text-green-500"
        },
        {
            title: "90-Day Strategy RL",
            desc: "Our Reinforcement Learning agent builds a custom roadmap based on your current domain authority.",
            icon: Target,
            color: "text-red-500"
        }
    ]

    return (
        <div className="min-h-screen bg-black text-white font-inter">
            {/* Hero */}
            <section className="pt-32 pb-20 px-6 border-b border-white/5 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-white/5 rounded-full blur-[150px] -mr-100 -mt-20 pointer-events-none" />
                <div className="max-w-7xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="max-w-3xl"
                    >
                        <h1 className="text-6xl md:text-8xl font-black tracking-tighter uppercase font-outfit leading-none mb-8">
                            UNFAIR <br /> <span className="text-white/20">ADVANTAGES</span>
                        </h1>
                        <p className="text-xl text-white/40 font-medium leading-relaxed max-w-xl">
                            We don't just 'audit' your site. We deploy a multi-layered neural assault
                            to find every possible path to #1.
                        </p>
                    </motion.div>
                </div>
            </section>

            {/* Grid */}
            <section className="py-32 px-6">
                <div className="max-w-7xl mx-auto">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
                        {features.map((f, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.1 }}
                                className="group p-8 rounded-3xl border border-white/10 bg-white/5 hover:border-white/30 transition-all duration-500"
                            >
                                <div className={`w-14 h-14 rounded-2xl bg-black border border-white/10 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform`}>
                                    <f.icon className={`w-6 h-6 ${f.color}`} />
                                </div>
                                <h3 className="text-2xl font-black mb-4 uppercase tracking-tight font-outfit">{f.title}</h3>
                                <p className="text-white/40 font-medium leading-relaxed">
                                    {f.desc}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Tech Stack Visualizer */}
            <section className="py-32 border-t border-white/5 bg-white/[0.02]">
                <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
                    <div>
                        <h2 className="text-4xl md:text-5xl font-black uppercase tracking-tighter font-outfit mb-8">THE 12-STEP <br /> <span className="text-white/20">TITAN PIPELINE</span></h2>
                        <div className="space-y-6">
                            {[
                                { step: "01", label: "Stealth Crawl", desc: "Playwright-based bypass of bot detection." },
                                { step: "02", label: "Lighthouse V12", desc: "Core Web Vital forensic analysis." },
                                { step: "03", label: "Entity Extraction", desc: "NLP mapping of all domain concepts." },
                                { step: "04", label: "SERP Intelligence", desc: "Live competitor ranking patterns." }
                            ].map((s, i) => (
                                <div key={i} className="flex gap-6 items-start pb-6 border-b border-white/5 group">
                                    <span className="text-xs font-black text-white/20 group-hover:text-white transition-colors">{s.step}</span>
                                    <div>
                                        <h4 className="font-black uppercase tracking-widest text-sm mb-1">{s.label}</h4>
                                        <p className="text-xs text-white/40 font-medium uppercase tracking-wider">{s.desc}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="aspect-square bg-black border border-white/10 rounded-[3rem] p-12 relative overflow-hidden group">
                        <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent pointer-events-none" />
                        <div className="relative z-10 h-full flex flex-col justify-between">
                            <div className="flex justify-between items-start">
                                <div className="p-4 bg-white/5 rounded-2xl border border-white/10 animate-bounce">
                                    <Bolt className="w-8 h-8 text-yellow-500" />
                                </div>
                                <div className="text-[10px] font-black tracking-[0.5em] text-white/20 uppercase">
                                    SYSTEM ARCHITECTURE
                                </div>
                            </div>
                            <div className="space-y-4">
                                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        whileInView={{ width: "85%" }}
                                        className="h-full bg-white"
                                    />
                                </div>
                                <div className="flex justify-between text-[10px] font-black text-white/40 uppercase tracking-widest">
                                    <span>Neural Confidence</span>
                                    <span>85.42%</span>
                                </div>
                            </div>
                        </div>
                        {/* Abstract Lines */}
                        <div className="absolute bottom-0 right-0 w-2/3 h-2/3 opacity-20 group-hover:opacity-40 transition-opacity">
                            <svg viewBox="0 0 100 100" className="w-full h-full text-white">
                                <path d="M0,100 L100,0 M20,100 L100,20 M40,100 L100,40" stroke="currentColor" fill="none" strokeWidth="0.5" />
                            </svg>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section className="py-40 text-center px-6">
                <h2 className="text-5xl md:text-7xl font-black uppercase tracking-tighter font-outfit mb-12">READY TO <br /> <span className="text-white/20">WEAPONIZE YOUR SEO?</span></h2>
                <Link href="/analyze">
                    <Button className="bg-white text-black hover:bg-gray-200 font-black h-20 px-12 rounded-full uppercase tracking-widest text-lg shadow-[0_20px_40px_-5px_rgba(255,255,255,0.2)]">
                        Initialize First Scan
                    </Button>
                </Link>
            </section>
        </div>
    )
}
