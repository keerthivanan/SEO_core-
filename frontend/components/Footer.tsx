import Link from 'next/link'
import { Crown } from 'lucide-react'

export function Footer() {
    return (
        <footer className="bg-black border-t border-white/10 py-12 px-4 font-inter text-gray-400 text-sm">
            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
                <div className="space-y-4">
                    <div className="flex items-center gap-2 text-white font-bold text-lg">
                        <div className="w-6 h-6 bg-white text-black flex items-center justify-center rounded text-xs font-outfit">R</div>
                        <span className="font-outfit">RankForge AI</span>
                    </div>
                    <p className="leading-relaxed">
                        The world's most advanced AI SEO platform.
                        Fix your site in 60 seconds. Rank #1 in 90 days.
                    </p>
                </div>

                <div>
                    <h4 className="text-white font-outfit font-semibold mb-4 uppercase tracking-wider text-xs">Product</h4>
                    <ul className="space-y-2">
                        <li><Link href="/analyze" className="hover:text-white transition-colors">Analyzer</Link></li>
                        <li><Link href="/pricing" className="hover:text-white transition-colors">Pricing</Link></li>
                        <li><Link href="/login" className="hover:text-white transition-colors">Login</Link></li>
                        <li><Link href="/dashboard" className="hover:text-white transition-colors">Dashboard</Link></li>
                    </ul>
                </div>

                <div>
                    <h4 className="text-white font-outfit font-semibold mb-4 uppercase tracking-wider text-xs">Resources</h4>
                    <ul className="space-y-2">
                        <li><Link href="/docs" className="hover:text-white transition-colors">Documentation</Link></li>
                        <li><Link href="/blog" className="hover:text-white transition-colors">SEO Blog</Link></li>
                        <li><Link href="/tools" className="hover:text-white transition-colors">Free Tools</Link></li>
                    </ul>
                </div>

                <div>
                    <h4 className="text-white font-outfit font-semibold mb-4 uppercase tracking-wider text-xs">Legal</h4>
                    <ul className="space-y-2">
                        <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                        <li><Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
                    </ul>
                </div>
            </div>

            <div className="max-w-7xl mx-auto border-t border-white/5 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs font-black uppercase tracking-widest text-white/20">
                <p className="font-outfit">&copy; {new Date().getFullYear()} RankForge AI. Neural Intelligence Powered.</p>
                <div className="flex items-center gap-2 group">
                    <Crown className="w-3 h-3 text-white group-hover:scale-125 transition-transform" />
                    <span className="font-outfit">Strongest Version Active</span>
                </div>
            </div>
        </footer>
    )
}
