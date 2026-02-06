'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { motion } from 'framer-motion'
import { Zap, Menu, X } from 'lucide-react'
import { useState } from 'react'

export function Navbar() {
    const [isOpen, setIsOpen] = useState(false)

    return (
        <nav className="border-b border-white/5 bg-black/80 backdrop-blur-xl sticky top-0 z-50 font-inter">
            <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
                {/* Logo */}
                <Link href="/" className="group flex items-center gap-3">
                    <div className="w-10 h-10 bg-white text-black flex items-center justify-center rounded-lg font-black text-xl font-outfit transition-transform group-hover:scale-110">
                        R
                    </div>
                    <span className="text-2xl font-black tracking-tighter font-outfit uppercase">
                        RANKFORGE<span className="text-white/20">.AI</span>
                    </span>
                </Link>

                {/* Desktop Menu */}
                <div className="hidden md:flex items-center gap-8">
                    <NavLink href="/features">Features</NavLink>
                    <NavLink href="/tools">Tools</NavLink>
                    <NavLink href="/pricing">Pricing</NavLink>
                    <NavLink href="/docs">Docs</NavLink>
                    <div className="h-6 w-[1px] bg-white/10 mx-2" />
                    <Link href="/login">
                        <Button variant="ghost" className="text-white/40 hover:text-white hover:bg-white/5 font-bold uppercase tracking-widest text-[10px]">
                            Login
                        </Button>
                    </Link>
                    <Link href="/analyze">
                        <Button className="bg-white text-black hover:bg-gray-200 font-black px-6 rounded-full uppercase tracking-widest text-[10px] shadow-[0_10px_20px_-10px_rgba(255,255,255,0.3)]">
                            Analyze Now
                        </Button>
                    </Link>
                </div>

                {/* Mobile Toggle */}
                <button
                    className="md:hidden text-white"
                    onClick={() => setIsOpen(!isOpen)}
                >
                    {isOpen ? <X /> : <Menu />}
                </button>
            </div>

            {/* Mobile Menu */}
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="md:hidden bg-black border-b border-white/10 p-6 space-y-4"
                >
                    <MobileNavLink href="/features" onClick={() => setIsOpen(false)}>Features</MobileNavLink>
                    <MobileNavLink href="/tools" onClick={() => setIsOpen(false)}>Tools</MobileNavLink>
                    <MobileNavLink href="/pricing" onClick={() => setIsOpen(false)}>Pricing</MobileNavLink>
                    <MobileNavLink href="/blog" onClick={() => setIsOpen(false)}>Blog</MobileNavLink>
                    <div className="pt-4 flex flex-col gap-3">
                        <Link href="/login" onClick={() => setIsOpen(false)}>
                            <Button variant="outline" className="w-full border-white/10 text-white uppercase tracking-widest text-xs font-black">
                                Login
                            </Button>
                        </Link>
                        <Link href="/analyze" onClick={() => setIsOpen(false)}>
                            <Button className="w-full bg-white text-black uppercase tracking-widest text-xs font-black">
                                Analyze Now
                            </Button>
                        </Link>
                    </div>
                </motion.div>
            )}
        </nav>
    )
}

function NavLink({ href, children }: { href: string, children: React.ReactNode }) {
    return (
        <Link
            href={href}
            className="text-sm font-bold text-white/40 hover:text-white transition-all uppercase tracking-[0.2em] relative group"
        >
            {children}
            <span className="absolute -bottom-1 left-0 w-0 h-[2px] bg-white transition-all group-hover:w-full" />
        </Link>
    )
}

function MobileNavLink({ href, onClick, children }: { href: string, onClick: () => void, children: React.ReactNode }) {
    return (
        <Link
            href={href}
            onClick={onClick}
            className="block text-lg font-black text-white hover:text-white/60 transition-colors uppercase tracking-widest"
        >
            {children}
        </Link>
    )
}
