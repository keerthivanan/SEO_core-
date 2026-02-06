'use client'

import { motion } from 'framer-motion'
import { Send, MapPin, Mail, Phone, Globe, Shield } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

export default function ContactPage() {
    return (
        <div className="min-h-screen bg-black text-white font-inter">
            {/* Header */}
            <section className="pt-32 pb-20 px-6 border-b border-white/5 relative">
                <div className="absolute top-0 left-0 w-full h-[300px] bg-gradient-to-b from-white/5 to-transparent pointer-events-none" />
                <div className="max-w-7xl mx-auto text-center space-y-8">
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-6xl md:text-9xl font-black uppercase tracking-tighter font-outfit leading-none"
                    >
                        COMMAND <br /> <span className="text-white/20">CENTER</span>
                    </motion.h1>
                    <p className="text-white/40 uppercase tracking-[0.5em] text-xs font-black">24/7 NEURAL SUPPORT PROTOCOL</p>
                </div>
            </section>

            <section className="py-32 px-6">
                <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-32">
                    {/* Info */}
                    <div className="space-y-20">
                        <div className="space-y-8">
                            <h2 className="text-4xl font-black uppercase font-outfit tracking-tight">GLOBAL <br /> <span className="text-white/20">INTERCEPT</span></h2>
                            <p className="text-white/40 max-w-sm leading-relaxed">
                                Need technical support or agency-level command?
                                Send your signal. We respond within 4 neural cycles (hours).
                            </p>
                        </div>

                        <div className="space-y-12">
                            <ContactInfo icon={Mail} label="SECURE EMAIL" value="COMMAND@RANKFORGE.AI" />
                            <ContactInfo icon={MapPin} label="HEADQUARTERS" value="RIYADH PROTOCOL / GLOBAL REMOTE" />
                            <ContactInfo icon={Globe} label="SOCIAL LINK" value="@RANKFORGE_AI" />
                        </div>

                        <div className="p-8 rounded-3xl border border-white/5 bg-white/[0.02]">
                            <div className="flex items-center gap-4 text-xs font-black text-white/20 uppercase tracking-[0.3em]">
                                <Shield className="w-4 h-4" /> Data Encryption Active
                            </div>
                        </div>
                    </div>

                    {/* Form */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="bg-zinc-900/50 backdrop-blur-xl p-12 rounded-[3rem] border border-white/10"
                    >
                        <form className="space-y-8">
                            <div className="space-y-2">
                                <label className="text-[10px] font-black uppercase tracking-widest text-white/30 ml-4">Full Identity</label>
                                <Input
                                    placeholder="SYNCID NAME"
                                    className="bg-black border-white/10 h-16 px-6 font-black uppercase tracking-widest focus:border-white transition-all rounded-2xl"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-black uppercase tracking-widest text-white/30 ml-4">Secure Channel (Email)</label>
                                <Input
                                    placeholder="EMAIL@PROTOCOL.COM"
                                    className="bg-black border-white/10 h-16 px-6 font-black uppercase tracking-widest focus:border-white transition-all rounded-2xl"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-[10px] font-black uppercase tracking-widest text-white/30 ml-4">Command Intent</label>
                                <Textarea
                                    placeholder="DESCRIBE YOUR OBJECTIVE..."
                                    className="bg-black border-white/10 min-h-[160px] p-6 font-black uppercase tracking-widest focus:border-white transition-all rounded-2xl resize-none"
                                />
                            </div>
                            <Button className="w-full h-16 bg-white text-black hover:bg-gray-200 font-black uppercase tracking-widest text-xs rounded-2xl transition-all shadow-[0_10px_30px_-10px_rgba(255,255,255,0.2)]">
                                SECURE TRANSMIT <Send className="ml-3 w-4 h-4" />
                            </Button>
                        </form>
                    </motion.div>
                </div>
            </section>
        </div>
    )
}

function ContactInfo({ icon: Icon, label, value }: { icon: any, label: string, value: string }) {
    return (
        <div className="flex gap-6 items-center group">
            <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Icon className="w-5 h-5 text-white/40 group-hover:text-white transition-colors" />
            </div>
            <div className="space-y-1">
                <h4 className="text-[10px] font-black uppercase tracking-[0.2em] text-white/20">{label}</h4>
                <p className="font-black text-sm uppercase tracking-widest">{value}</p>
            </div>
        </div>
    )
}
