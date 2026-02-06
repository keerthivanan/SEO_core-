'use client'

import { motion } from 'framer-motion'
import { Hammer, Book, Code, Cpu, Shield, Zap, Search, Globe, ChevronRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export default function DocsPage() {
    const sections = [
        { title: "Introduction", icon: Book },
        { title: "Titan ML Pipeline", icon: Cpu },
        { title: "API Command Set", icon: Code },
        { title: "Authentication", icon: Shield },
        { title: "Optimization Logic", icon: Zap }
    ]

    return (
        <div className="min-h-screen bg-black text-white font-inter flex flex-col md:flex-row">
            {/* Sidebar */}
            <aside className="w-full md:w-80 border-r border-white/5 p-8 space-y-12 shrink-0">
                <div className="space-y-4">
                    <h2 className="text-xs font-black uppercase tracking-[0.3em] text-white/20">DOCUMENTATION</h2>
                    <nav className="space-y-2">
                        {sections.map((s, i) => (
                            <Link
                                key={i}
                                href="#"
                                className={`flex items-center gap-4 p-4 rounded-xl transition-all ${i === 1 ? 'bg-white text-black font-black' : 'text-white/40 hover:bg-white/5 hover:text-white'}`}
                            >
                                <s.icon className="w-4 h-4" />
                                <span className="text-xs uppercase tracking-widest">{s.title}</span>
                                {i === 1 && <ChevronRight className="ml-auto w-4 h-4" />}
                            </Link>
                        ))}
                    </nav>
                </div>
            </aside>

            {/* Content */}
            <main className="flex-1 p-12 md:p-24 max-w-5xl">
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-16"
                >
                    <div className="space-y-6">
                        <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded text-[10px] font-black uppercase tracking-widest text-white/40">
                            SPECIFICATION V2.10
                        </div>
                        <h1 className="text-5xl md:text-7xl font-black uppercase tracking-tighter font-outfit leading-none">
                            TITAN ML <br /> <span className="text-white/20">PIPELINE</span>
                        </h1>
                        <p className="text-xl text-white/40 leading-relaxed font-medium">
                            An exhaustive breakdown of the 12-stage neural optimization sequence.
                        </p>
                    </div>

                    <div className="space-y-12">
                        <DocSection
                            title="01 / STEALTH CRAWL"
                            content="Our crawler utilizes a headful Playwright cluster to bypass Cloudflare and Akamai bot detection. It extracts raw HTML, computed CSS, and all JSON-LD schemas."
                        />
                        <DocSection
                            title="02 / ENTITY FORENSICS"
                            content="Using the Neuro-Semantic engine, we map the entity density of the page versus the top 10 SERP competitors to identify conceptual gaps."
                        />
                        <DocSection
                            title="03 / RL STRATEGY"
                            content="The Reinforcement Learning agent selects from 20 predefined SEO actions (Interlinking, Entity Injection, H-Tag Refactoring) to build the 90-day roadmap."
                        />
                    </div>

                    <div className="p-12 rounded-[2.5rem] bg-zinc-900/50 border border-white/10 space-y-6">
                        <h4 className="font-black uppercase tracking-widest text-sm">PROPER IMPLEMENTATION</h4>
                        <p className="text-sm text-white/40 leading-relaxed font-medium">
                            To achieve a 90% confidence score, you must implement at least 85% of the
                            Neuro-Semantic recommendations within the first 14 days of analysis.
                        </p>
                        <Link href="/analyze">
                            <Button className="bg-white text-black font-black uppercase tracking-widest text-[10px] h-12 px-8 rounded-xl">
                                INITIATE SCAN
                            </Button>
                        </Link>
                    </div>
                </motion.div>
            </main>
        </div>
    )
}

function DocSection({ title, content }: { title: string, content: string }) {
    return (
        <div className="space-y-4 border-l border-white/10 pl-8">
            <h3 className="text-lg font-black uppercase tracking-tight font-outfit">{title}</h3>
            <p className="text-white/40 text-sm leading-relaxed font-medium">{content}</p>
        </div>
    )
}
