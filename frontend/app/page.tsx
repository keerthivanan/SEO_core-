'use client'

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Check, Zap, Search, Shield, Cpu, Globe } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
    return (
        <div className="min-h-screen bg-black text-white font-inter">
            <main className="flex-1 flex flex-col">
                {/* Hero Section */}
                <section className="relative max-w-7xl mx-auto w-full pt-40 pb-32 px-6 text-center overflow-hidden">
                    {/* Background Gradients */}
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-gradient-to-b from-white/5 to-transparent pointer-events-none" />

                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, ease: "easeOut" }}
                    >
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 text-[10px] font-black uppercase tracking-[0.3em] text-white/40 mb-12">
                            <Zap className="w-3 h-3 fill-white/40" /> Neural Intelligence v2.10 Active
                        </div>

                        <h1 className="text-6xl md:text-9xl font-black tracking-tighter leading-[0.85] text-white mb-10 font-outfit uppercase">
                            COMMAND THE <br />
                            <span className="text-white/20">FIRST PAGE</span>
                        </h1>

                        <p className="text-xl md:text-2xl text-white/40 max-w-3xl mx-auto leading-relaxed mb-16 font-medium">
                            Professional-grade AI SEO for serious domains.
                            Detect semantic gaps, outpace competitors, and dominate SERPs with Titan ML logic.
                        </p>

                        <div className="max-w-2xl mx-auto bg-white/5 p-2 rounded-2xl border border-white/10 flex flex-col sm:flex-row gap-2 mb-8">
                            <input
                                type="text"
                                placeholder="Paste Your Website URL Here..."
                                className="flex-1 bg-transparent border-none text-white placeholder:text-gray-500 px-6 py-4 focus:ring-0 text-lg outline-none"
                            />
                            <Link href="/analyze" className="w-full sm:w-auto">
                                <Button size="lg" className="w-full h-14 px-8 text-lg bg-white text-black hover:bg-gray-100 font-bold rounded-xl transition-all hover:scale-105">
                                    Analyze Now <ArrowRight className="ml-2 w-5 h-5" />
                                </Button>
                            </Link>
                        </div>

                        {/* Trust Bar */}
                        <div className="flex flex-wrap justify-center gap-12 text-[10px] font-black text-white/20 uppercase tracking-[0.4em] pt-12 border-t border-white/5">
                            <span className="flex items-center gap-2"><Globe className="w-3 h-3" /> 67,432 SCANS</span>
                            <span className="flex items-center gap-2"><Cpu className="w-3 h-3" /> NEURAL v2.10</span>
                            <span className="flex items-center gap-2"><Shield className="w-3 h-3" /> 90-DAY PROMISE</span>
                        </div>
                    </motion.div>
                </section>

                {/* Main Action Section */}
                <section className="py-24 border-y border-white/5 bg-black">
                    <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
                        <div className="space-y-8 text-left">
                            <h2 className="text-4xl md:text-6xl font-black uppercase font-outfit tracking-tighter leading-none text-white">
                                THE 2026 <br /> <span className="text-white/20">SEO PROTOCOL</span>
                            </h2>
                            <p className="text-white/40 text-lg leading-relaxed max-w-md">
                                Most tools show you problems. RankForge AI gives you the **logic**.
                                Use our deep learning pipeline to detect exactly why competitors are outranking you.
                            </p>
                            <div className="flex flex-col gap-4">
                                <FeatureItem text="TITAN ML NEURAL ANALYSIS" />
                                <FeatureItem text="SEMANTIC ENTITY INJECTION" />
                                <FeatureItem text="REINFORCEMENT LEARNING ROADMAP" />
                            </div>
                        </div>
                        <div className="aspect-video bg-black border border-white/10 rounded-[3rem] p-1 shadow-[0_0_100px_-20px_rgba(255,255,255,0.1)] overflow-hidden">
                            <div className="h-full w-full bg-black rounded-[2.8rem] flex items-center justify-center border border-white/5">
                                <Search className="w-20 h-20 text-white/10 animate-pulse" />
                            </div>
                        </div>
                    </div>
                </section>

                {/* Final CTA */}
                <section className="py-40 text-center px-6">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        className="space-y-12"
                    >
                        <h2 className="text-5xl md:text-9xl font-black uppercase tracking-tighter font-outfit leading-[0.85]">
                            RANK #1 <br /> <span className="text-white/20">OR IT'S FREE</span>
                        </h2>
                        <Link href="/analyze">
                            <Button className="bg-white text-black hover:bg-gray-200 font-black h-24 px-16 rounded-full uppercase tracking-widest text-xl shadow-[0_30px_60px_-15px_rgba(255,255,255,0.3)]">
                                Initialize Global Scan
                            </Button>
                        </Link>
                        <p className="text-[10px] font-black uppercase tracking-[0.5em] text-white/10">30-DAY LOGICAL REFUND POLICY ACTIVE</p>
                    </motion.div>
                </section>
            </main>
        </div>
    );
}

function FeatureItem({ text }: { text: string }) {
    return (
        <div className="flex items-center gap-4 group">
            <div className="w-6 h-6 rounded-full border border-white/20 flex items-center justify-center group-hover:bg-white group-hover:border-white transition-all">
                <Check className="w-3 h-3 text-white group-hover:text-black" />
            </div>
            <span className="text-xs font-black uppercase tracking-widest text-white/60 group-hover:text-white transition-colors">
                {text}
            </span>
        </div>
    )
}
