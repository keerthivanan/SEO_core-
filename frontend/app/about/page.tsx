'use client'

import { motion } from 'framer-motion'
import { Shield, Target, Zap, Crown, Globe, Cpu } from 'lucide-react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function AboutPage() {
    return (
        <div className="min-h-screen bg-black text-white font-inter">
            {/* Header */}
            <section className="pt-32 pb-20 px-6 border-b border-white/5 text-center">
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 text-[10px] font-black uppercase tracking-[0.3em] text-white/40 mb-12"
                >
                    <Crown className="w-3 h-3" /> The Global Oracle Manifesto
                </motion.div>
                <h1 className="text-6xl md:text-9xl font-black uppercase tracking-tighter font-outfit leading-none mb-12">
                    WE ARE <br /> <span className="text-white/20">RANKFORGE</span>
                </h1>
                <p className="text-xl md:text-2xl text-white/40 max-w-2xl mx-auto leading-relaxed font-medium">
                    The only SEO platform engineered with a "Hybrid Brain".
                    Global search intelligence combined with native culturally-sensitive execution.
                </p>
            </section>

            {/* The Vision */}
            <section className="py-32 px-6">
                <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-20 items-center">
                    <div className="space-y-12">
                        <div className="space-y-4">
                            <h2 className="text-4xl font-black uppercase font-outfit tracking-tight">GLOBAL BRAIN, <br /> <span className="text-white/20">LOCAL TONGUE</span></h2>
                            <p className="text-white/40 leading-relaxed max-w-md">
                                Most SEO tools are built for the US market and translated as an afterthought.
                                RankForge AI was built from the ground up to understand the nuances of
                                diverse markets, starting with advanced Arabic-English cross-dominance.
                            </p>
                        </div>
                        <div className="grid grid-cols-2 gap-8">
                            <Stat label="SUCCESS RATE" value="94.2%" />
                            <Stat label="DOMAINS SCANNED" value="67K+" />
                        </div>
                    </div>
                    <div className="grid grid-cols-1 gap-4">
                        <ManifestoCard
                            icon={Globe}
                            title="Zero Jurisdictions"
                            text="We scan globally. No data silos. No location bias. Just pure SERP reality."
                        />
                        <ManifestoCard
                            icon={Shield}
                            title="Absolute Integrity"
                            text="We don't sell 'maybe'. If our neural engine says you can't rank, we tell you exactly why."
                        />
                        <ManifestoCard
                            icon={Zap}
                            title="Instant Command"
                            text="Analysis in 60 seconds. Fixes in 2 minutes. Ranking in 90 days. That is the protocol."
                        />
                    </div>
                </div>
            </section>

            {/* The Tech Philosophy */}
            <section className="py-32 border-y border-white/5 bg-white/[0.01]">
                <div className="max-w-4xl mx-auto px-6 text-center space-y-16">
                    <h2 className="text-4xl font-black uppercase font-outfit tracking-tighter">OUR NEURAL PHILOSOPHY</h2>
                    <div className="space-y-8 text-left border-l-2 border-white/10 pl-12">
                        <div className="space-y-2">
                            <h4 className="font-black text-xs uppercase tracking-[0.3em] text-white/20">PRINCIPLE ONE</h4>
                            <p className="text-xl font-bold uppercase tracking-tight">SEO IS A LOGIC GAME, NOT A GUESSING GAME.</p>
                        </div>
                        <div className="space-y-2">
                            <h4 className="font-black text-xs uppercase tracking-[0.3em] text-white/20">PRINCIPLE TWO</h4>
                            <p className="text-xl font-bold uppercase tracking-tight">IF THE AI CAN'T GENERATE A BETTER FIX THAN A HUMAN, THE AI IS BROKEN.</p>
                        </div>
                        <div className="space-y-2">
                            <h4 className="font-black text-xs uppercase tracking-[0.3em] text-white/20">PRINCIPLE THREE</h4>
                            <p className="text-xl font-bold uppercase tracking-tight">SPEED IS THE ONLY MEASURE OF COMMAND.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Meet the Machine */}
            <section className="py-32 px-6">
                <div className="max-w-7xl mx-auto text-center space-y-20">
                    <div className="space-y-6">
                        <h2 className="text-6xl font-black uppercase font-outfit tracking-tighter">THE TEAM</h2>
                        <p className="text-white/40 uppercase tracking-[0.4em] text-[10px] font-black">HUMAN INGENUITY / NEURAL EXECUTION</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-3xl mx-auto">
                        <TeamCard name="THE ARCHITECT" role="Neural Logic Design" />
                        <TeamCard name="THE CRAWLER" role="Global Data Extraction" />
                    </div>
                </div>
            </section>

            {/* Footer CTA */}
            <section className="py-40 border-t border-white/10 text-center">
                <p className="text-[10px] font-black uppercase tracking-[0.5em] text-white/20 mb-12">ESTABLISHED 2026 / RIYADH / GLOBAL</p>
                <Link href="/analyze">
                    <Button variant="outline" className="border-white/10 text-white hover:bg-white hover:text-black font-black h-16 px-12 uppercase tracking-widest text-xs transition-all duration-500">
                        Join the RankForge Protocol
                    </Button>
                </Link>
            </section>
        </div>
    )
}

function Stat({ label, value }: { label: string, value: string }) {
    return (
        <div className="space-y-1">
            <div className="text-4xl font-black font-outfit">{value}</div>
            <div className="text-[10px] font-black uppercase tracking-widest text-white/20">{label}</div>
        </div>
    )
}

function ManifestoCard({ icon: Icon, title, text }: { icon: any, title: string, text: string }) {
    return (
        <div className="p-8 rounded-3xl border border-white/5 bg-white/[0.02] flex items-start gap-8 group hover:border-white/20 transition-all">
            <div className="w-12 h-12 rounded-xl bg-black border border-white/10 flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
                <Icon className="w-5 h-5 text-white/40" />
            </div>
            <div className="space-y-2">
                <h4 className="font-black uppercase tracking-widest text-sm">{title}</h4>
                <p className="text-sm text-white/30 leading-relaxed font-medium">{text}</p>
            </div>
        </div>
    )
}

function TeamCard({ name, role }: { name: string, role: string }) {
    return (
        <div className="space-y-4">
            <div className="aspect-square bg-white/5 rounded-[2rem] border border-white/10" />
            <div className="space-y-1">
                <div className="font-black uppercase tracking-tighter text-2xl font-outfit">{name}</div>
                <div className="text-[10px] font-black uppercase tracking-widest text-white/20">{role}</div>
            </div>
        </div>
    )
}
