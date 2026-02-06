'use client'

import { motion } from 'framer-motion'
import { Wrench, FileCode, Search, Globe, Zap, Code, Shield, Download, Copy } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useState } from 'react'
import { toast } from 'sonner'
import Link from 'next/link'

export default function ToolsPage() {
    const [robotsUrl, setRobotsUrl] = useState('')
    const [robotsType, setRobotsType] = useState('allow')

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text)
        toast.success("Copied to clipboard")
    }

    const tools = [
        {
            title: "Robots.txt Generator",
            desc: "Command how bots access your domain.",
            icon: Shield
        },
        {
            title: "Sitemap Schema",
            desc: "Build logical maps for search spiders.",
            icon: Globe
        },
        {
            title: "Keyword Forensics",
            desc: "Check entity density on any page.",
            icon: Search
        }
    ]

    return (
        <div className="min-h-screen bg-black text-white font-inter">
            {/* Header */}
            <section className="pt-32 pb-20 px-6 border-b border-white/5 bg-white/[0.01]">
                <div className="max-w-7xl mx-auto flex flex-col items-center text-center space-y-8">
                    <div className="w-20 h-20 bg-white/5 rounded-3xl border border-white/10 flex items-center justify-center animate-pulse">
                        <Wrench className="w-10 h-10 text-white/40" />
                    </div>
                    <h1 className="text-6xl md:text-8xl font-black uppercase tracking-tighter font-outfit leading-none">
                        FREE <br /> <span className="text-white/20">TOOLS</span>
                    </h1>
                    <p className="text-white/40 uppercase tracking-[0.4em] text-[10px] font-black">INTERNAL AGENCY GEAR / PUBLIC ACCESS</p>
                </div>
            </section>

            {/* Tool Selection */}
            <section className="py-20 px-6 max-w-7xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {tools.map((t, i) => (
                        <div key={i} className="p-8 rounded-3xl border border-white/5 bg-white/[0.02] group hover:border-white/20 transition-all cursor-pointer">
                            <div className="w-12 h-12 rounded-xl bg-black border border-white/10 flex items-center justify-center mb-6">
                                <t.icon className="w-5 h-5 text-white/40 group-hover:text-white transition-colors" />
                            </div>
                            <h3 className="font-black uppercase tracking-tight text-xl font-outfit mb-2">{t.title}</h3>
                            <p className="text-sm text-white/30 font-medium leading-relaxed">{t.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Active Tool Module (Robots.txt) */}
            <section className="py-32 px-6 border-t border-white/5 relative overflow-hidden">
                <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-white/5 rounded-full blur-[120px] pointer-events-none" />
                <div className="max-w-4xl mx-auto space-y-12">
                    <div className="space-y-4">
                        <h2 className="text-3xl font-black uppercase font-outfit">ROBOTS.TXT <br /> <span className="text-white/20">COMMAND GENERATOR</span></h2>
                        <p className="text-white/40 text-sm font-medium">Generate a professional allow/disallow protocol for your root directory.</p>
                    </div>

                    <div className="bg-zinc-900/50 p-10 rounded-[2.5rem] border border-white/10 space-y-8">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div className="space-y-4">
                                <label className="text-[10px] font-black uppercase tracking-widest text-white/20 ml-2">Protocol Action</label>
                                <select
                                    className="w-full bg-black border border-white/10 h-14 rounded-xl px-4 font-black uppercase tracking-widest text-xs outline-none focus:border-white"
                                    value={robotsType}
                                    onChange={(e) => setRobotsType(e.target.value)}
                                >
                                    <option value="allow">ALLOW ALL</option>
                                    <option value="disallow">DISALLOW ALL</option>
                                </select>
                            </div>
                            <div className="space-y-4">
                                <label className="text-[10px] font-black uppercase tracking-widest text-white/20 ml-2">Specific Dir (Optional)</label>
                                <Input
                                    placeholder="/ADMIN"
                                    className="bg-black border-white/10 h-14 font-black uppercase tracking-widest text-xs rounded-xl"
                                />
                            </div>
                        </div>

                        <div className="space-y-4">
                            <label className="text-[10px] font-black uppercase tracking-widest text-white/20 ml-2">Generated Directive</label>
                            <div className="bg-black p-8 rounded-2xl border border-white/10 relative group">
                                <code className="text-white/60 font-mono text-sm">
                                    User-agent: * <br />
                                    {robotsType === 'allow' ? 'Allow: /' : 'Disallow: /'}
                                </code>
                                <Button
                                    size="icon"
                                    variant="ghost"
                                    className="absolute top-4 right-4 text-white/20 hover:text-white"
                                    onClick={() => copyToClipboard(`User-agent: *\n${robotsType === 'allow' ? 'Allow: /' : 'Disallow: /'}`)}
                                >
                                    <Copy className="w-4 h-4" />
                                </Button>
                            </div>
                        </div>

                        <Button className="w-full h-14 bg-white text-black font-black uppercase tracking-widest text-xs rounded-xl hover:bg-gray-200">
                            Download Protocol <Download className="ml-2 w-4 h-4" />
                        </Button>
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section className="py-40 text-center bg-white/[0.01]">
                <h2 className="text-5xl font-black uppercase font-outfit tracking-tighter mb-8">NEED <br /> <span className="text-white/20">DEEPER INTEL?</span></h2>
                <Link href="/analyze">
                    <Button className="bg-transparent border border-white/10 text-white font-black h-16 px-12 uppercase tracking-widest text-xs hover:bg-white hover:text-black transition-all rounded-xl">
                        Run Titan Analysis
                    </Button>
                </Link>
            </section>
        </div>
    )
}
