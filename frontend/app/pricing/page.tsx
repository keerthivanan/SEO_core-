'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Check, Zap, Shield } from 'lucide-react'
import { motion } from 'framer-motion'

export default function PricingPage() {
    return (
        <div className="min-h-screen bg-black text-white font-inter selection:bg-white selection:text-black">
            {/* Navbar */}
            <nav className="border-b border-white/5 bg-black/80 backdrop-blur-xl sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
                    <Link href="/" className="group">
                        <span className="text-2xl font-black tracking-tighter font-outfit uppercase group-hover:opacity-80 transition-opacity">
                            RANKFORGE<span className="text-white/30">.AI</span>
                        </span>
                    </Link>
                    <div className="flex items-center gap-8">
                        <Link href="/docs" className="text-sm font-bold text-white/40 hover:text-white transition-colors uppercase tracking-widest">Docs</Link>
                        <Button variant="ghost" asChild className="text-white/40 hover:text-white hover:bg-white/5 font-bold uppercase tracking-widest text-xs">
                            <Link href="/login">Sign In</Link>
                        </Button>
                    </div>
                </div>
            </nav>

            <div className="py-32 px-6 lg:px-8 relative overflow-hidden">
                {/* Background Glow */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-gradient-to-b from-white/5 to-transparent pointer-events-none" />

                {/* Header Section */}
                <div className="relative z-10 text-center max-w-4xl mx-auto space-y-6 mb-32">
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-6xl md:text-8xl font-black tracking-tighter text-white font-outfit uppercase leading-[0.9]"
                    >
                        PROPER <br /> <span className="text-white/20">SUBSCRIPTIONS</span>
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        className="text-white/40 max-w-xl mx-auto text-lg font-medium leading-relaxed"
                    >
                        Professional-grade SEO intelligence for serious domains.
                        Zero bloat. Total dominance.
                    </motion.p>
                </div>

                {/* Pricing Grid */}
                <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-10 relative z-10">

                    {/* Starter Tier */}
                    <motion.div
                        whileHover={{ y: -5 }}
                        className="border border-white/10 bg-black/40 backdrop-blur-sm rounded-[2rem] p-12 flex flex-col group transition-all duration-500 hover:border-white/30"
                    >
                        <h3 className="text-xs font-black mb-8 uppercase font-outfit tracking-[0.3em] text-white/30">Tier I / Starter</h3>
                        <div className="text-6xl font-black mb-8 font-outfit leading-none">$0</div>
                        <p className="text-white/50 mb-10 text-sm font-medium leading-relaxed">Fundamental verification gear. Test the Titan Engine on a single domain.</p>
                        <ul className="space-y-5 flex-1 mb-12">
                            <li className="flex items-center gap-4 text-sm font-bold tracking-tight"><Check className="w-5 h-5 text-white/20" /> 1 DOMAIN AUDIT / MO</li>
                            <li className="flex items-center gap-4 text-sm font-bold tracking-tight"><Check className="w-5 h-5 text-white/20" /> BASIC NEURAL ID</li>
                            <li className="flex items-center gap-4 text-sm font-bold tracking-tight"><Check className="w-5 h-5 text-white/20" /> PDF EXPORT (WATERMARKED)</li>
                        </ul>
                        <Button variant="outline" className="w-full border-white/10 hover:bg-white text-white hover:text-black font-black h-16 uppercase tracking-widest text-xs transition-all duration-300" asChild>
                            <Link href="/">Try Free</Link>
                        </Button>
                    </motion.div>

                    {/* Pro Tier */}
                    <motion.div
                        initial={{ scale: 1 }}
                        whileHover={{ scale: 1.02 }}
                        className="border-2 border-white bg-black rounded-[2.2rem] p-12 flex flex-col relative shadow-[0_0_100px_-20px_rgba(255,255,255,0.1)] z-10"
                    >
                        <div className="absolute top-10 right-10 bg-white text-black text-[10px] font-black px-4 py-1.5 rounded-full flex items-center gap-2 font-outfit tracking-widest">
                            <Zap className="w-3 h-3 fill-black" /> COMMAND CHOICE
                        </div>
                        <h3 className="text-xs font-black mb-8 uppercase font-outfit tracking-[0.3em] text-white/50">Tier II / Pro</h3>
                        <div className="text-6xl font-black mb-8 font-outfit leading-none">$29<span className="text-xl text-white/20 ml-2 font-black">/mo</span></div>
                        <p className="text-white/80 mb-10 text-sm font-medium leading-relaxed">The strongest option. Full access to Titan ML and Competitor Logic.</p>
                        <ul className="space-y-5 flex-1 mb-12">
                            <li className="flex items-center gap-4 text-sm font-black"><Check className="w-5 h-5 text-white" /> UNLIMITED NEURAL AUDITS</li>
                            <li className="flex items-center gap-4 text-sm font-black"><Check className="w-5 h-5 text-white" /> FULL COMPETITOR FORENSICS</li>
                            <li className="flex items-center gap-4 text-sm font-black"><Check className="w-5 h-5 text-white" /> 90-DAY STRATEGY PIPELINE</li>
                            <li className="flex items-center gap-4 text-sm font-black"><Check className="w-5 h-5 text-white" /> WEEKLY RANK SURVEILLANCE</li>
                        </ul>
                        <Button className="w-full bg-white text-black hover:bg-gray-200 font-black h-16 uppercase tracking-widest text-sm transition-all shadow-[0_20px_40px_-10px_rgba(255,255,255,0.2)]" asChild>
                            <Link href="/login?plan=pro">Go Professional</Link>
                        </Button>
                        <p className="text-[10px] text-center text-white/20 mt-4 uppercase font-black tracking-widest">30-day logical refund guarantee</p>
                    </motion.div>

                    {/* Agency Tier */}
                    <motion.div
                        whileHover={{ y: -5 }}
                        className="border border-white/10 bg-black/40 backdrop-blur-sm rounded-[2rem] p-12 flex flex-col group transition-all duration-500 hover:border-white/30"
                    >
                        <h3 className="text-xs font-black mb-8 uppercase font-outfit tracking-[0.3em] text-white/30">Tier III / Agency</h3>
                        <div className="text-6xl font-black mb-8 font-outfit leading-none">$99<span className="text-xl text-white/20 ml-2 font-black">/mo</span></div>
                        <p className="text-white/50 mb-10 text-sm font-medium leading-relaxed">Scale your command across 100+ domains with white-label assets.</p>
                        <ul className="space-y-5 flex-1 mb-12">
                            <li className="flex items-center gap-4 text-sm font-bold tracking-tight"><Check className="w-5 h-5 text-white" /> EVERYTHING IN PRO</li>
                            <li className="flex items-center gap-4 text-sm font-bold tracking-tight"><Check className="w-5 h-5 text-white" /> WHITE-LABEL PDF ENGINE</li>
                            <li className="flex items-center gap-4 text-sm font-bold tracking-tight"><Check className="w-5 h-5 text-white" /> API COMMAND ACCESS</li>
                            <li className="flex items-center gap-4 text-sm font-bold tracking-tight"><Check className="w-5 h-5 text-white" /> TEAM PERMISSIONS CONTROL</li>
                        </ul>
                        <Button variant="outline" className="w-full border-white/10 hover:bg-white text-white hover:text-black font-black h-16 uppercase tracking-widest text-xs transition-all duration-300" asChild>
                            <Link href="/login?plan=agency">Contact Command</Link>
                        </Button>
                    </motion.div>

                </div>

                {/* Footer Security */}
                <div className="mt-40 text-center pb-20">
                    <div className="inline-flex items-center gap-4 text-white/10 uppercase font-black tracking-[0.5em] text-[10px] border border-white/10 px-6 py-3 rounded-full">
                        <Shield className="w-4 h-4" /> MILITARY-GRADE STRIPE ENCRYPTION
                    </div>
                </div>
            </div>
        </div>
    )
}
