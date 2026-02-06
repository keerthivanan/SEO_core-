'use client'

import { motion } from 'framer-motion'
import { PenTool, Calendar, User, ArrowRight, Zap, Target, Brain, Globe } from 'lucide-react'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export default function BlogPage() {
    const posts = [
        {
            title: "Neuro-Semantic SEO: The 2026 Ranking Factor",
            excerpt: "Why traditional keyword density is dead and entity logic is the new king of the SERP.",
            category: "INTEL",
            date: "FEB 2026",
            icon: Brain
        },
        {
            title: "Winning the SGE Overviews",
            excerpt: "How to structure your content so Google's Generative AI cites your domain as the primary source.",
            category: "AEO",
            date: "JAN 2026",
            icon: Zap
        },
        {
            title: "Global Search Nuance: Case Study Riyadh",
            excerpt: "A deep dive into cross-language dominance and why localized logic beats raw translation.",
            category: "GLOBAL",
            date: "JAN 2026",
            icon: Globe
        }
    ]

    return (
        <div className="min-h-screen bg-black text-white font-inter">
            {/* Header */}
            <section className="pt-32 pb-20 px-6 border-b border-white/5 bg-white/[0.01]">
                <div className="max-w-7xl mx-auto text-center space-y-8">
                    <div className="flex justify-center">
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-white/10 bg-white/5 text-[10px] font-black uppercase tracking-[0.3em] text-white/40">
                            <PenTool className="w-3 h-3" /> SEO Intelligence Feed
                        </div>
                    </div>
                    <h1 className="text-6xl md:text-9xl font-black uppercase tracking-tighter font-outfit leading-none">
                        RANKFORGE <br /> <span className="text-white/20">BLOG</span>
                    </h1>
                </div>
            </section>

            {/* Featured Post */}
            <section className="py-20 px-6 max-w-7xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="group relative h-[500px] rounded-[3rem] border border-white/10 overflow-hidden cursor-pointer"
                >
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent z-10" />
                    <div className="absolute inset-0 bg-white/5 group-hover:bg-white/10 transition-colors" />

                    <div className="absolute bottom-16 left-16 z-20 space-y-6 max-w-2xl">
                        <div className="inline-block px-3 py-1 bg-white text-black text-[10px] font-black tracking-widest uppercase rounded">FEATURED COMMAND</div>
                        <h2 className="text-4xl md:text-6xl font-black uppercase font-outfit leading-none tracking-tight">THE 12-STEP <br /> TITAN PROTOCOL</h2>
                        <p className="text-white/60 text-lg font-medium leading-relaxed">
                            How we engineered the world's most aggressive SEO pipeline and why it's guaranteed to work.
                        </p>
                        <Button className="bg-white text-black font-black uppercase tracking-widest text-xs h-14 px-8 rounded-xl group">
                            Full Intel Report <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </Button>
                    </div>
                </motion.div>
            </section>

            {/* Grid */}
            <section className="py-20 px-6 max-w-7xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
                    {posts.map((p, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: i * 0.1 }}
                            className="group space-y-8 p-8 rounded-[2.5rem] border border-white/5 bg-white/[0.02] hover:border-white/20 transition-all"
                        >
                            <div className="w-14 h-14 rounded-2xl bg-black border border-white/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                                <p.icon className="w-6 h-6 text-white/40" />
                            </div>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center text-[10px] font-black tracking-widest text-white/20 uppercase">
                                    <span>{p.category}</span>
                                    <span>{p.date}</span>
                                </div>
                                <h3 className="text-2xl font-black uppercase font-outfit tracking-tight group-hover:text-white/80 transition-colors">{p.title}</h3>
                                <p className="text-sm text-white/40 font-medium leading-relaxed">{p.excerpt}</p>
                            </div>
                            <Link href="#" className="inline-flex items-center gap-2 text-xs font-black uppercase tracking-widest text-white hover:opacity-60 transition-opacity">
                                Read Protocol <ArrowRight className="w-3 h-3" />
                            </Link>
                        </motion.div>
                    ))}
                </div>
            </section>

            {/* Footer */}
            <section className="py-40 text-center border-t border-white/10">
                <h2 className="text-4xl font-black uppercase font-outfit tracking-tighter mb-8">SUBSCRIBE TO <br /> <span className="text-white/20">NEURAL ALERTS</span></h2>
                <div className="max-w-md mx-auto flex gap-2 p-2 rounded-2xl border border-white/10 bg-white/5">
                    <input
                        placeholder="PROTOCOL@EMAIL.COM"
                        className="flex-1 bg-transparent px-4 font-black uppercase tracking-widest text-xs outline-none"
                    />
                    <Button className="bg-white text-black font-black uppercase tracking-widest text-[10px] h-12 rounded-xl">Join</Button>
                </div>
            </section>
        </div>
    )
}
