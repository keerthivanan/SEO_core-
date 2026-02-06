'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Loader2, ShieldCheck, Zap } from 'lucide-react'
import { toast } from 'sonner'

export default function LoginPage() {
    const [email, setEmail] = useState('')
    const [loading, setLoading] = useState(false)
    const [sent, setSent] = useState(false)

    const supabase = createClient()

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)

        try {
            const { error } = await supabase.auth.signInWithOtp({
                email,
                options: {
                    emailRedirectTo: `${location.origin}/auth/callback`,
                },
            })

            if (error) throw error

            setSent(true)
            toast.success('Magic link sent to your email!')
        } catch (error: any) {
            toast.error(error.message || 'Error logging in')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-black text-white flex items-center justify-center p-4 relative overflow-hidden">
            {/* Background Ambience */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-900/10 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-blue-900/10 rounded-full blur-[120px]" />
            </div>

            <div className="w-full max-w-md z-10 space-y-8">
                <div className="text-center space-y-2">
                    <Link href="/" className="inline-block group">
                        <h1 className="text-4xl font-black tracking-tighter cursor-pointer group-hover:opacity-80 transition-opacity font-outfit uppercase">
                            RANKFORGE<span className="text-white/20">.AI</span>
                        </h1>
                    </Link>
                    <p className="text-white/30 uppercase tracking-[0.2em] text-[10px] font-black">Titan Command / Auth Protocol</p>
                </div>

                <Card className="bg-black border-white/10 backdrop-blur-xl shadow-[0_0_100px_-20px_rgba(255,255,255,0.05)] rounded-2xl overflow-hidden">
                    <CardHeader className="space-y-1 pb-8 border-b border-white/5">
                        <CardTitle className="text-2xl font-black tracking-widest text-center text-white uppercase font-outfit">
                            {sent ? 'CHECK COMMAND' : 'INITIATE ENTRY'}
                        </CardTitle>
                        <CardDescription className="text-center text-white/30 text-xs font-medium">
                            {sent
                                ? `Protocol sent to ${email}`
                                : 'ENTER CREDENTIALS TO SYNC NEURAL ASSETS'}
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        {sent ? (
                            <div className="text-center space-y-6 py-4">
                                <div className="flex justify-center">
                                    <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center animate-pulse">
                                        <ShieldCheck className="w-8 h-8 text-green-500" />
                                    </div>
                                </div>
                                <p className="text-xs font-bold text-white/40 uppercase tracking-widest">
                                    Click the secure link in your terminal (email) to sync.
                                    <br />Neural link active.
                                </p>
                                <Button
                                    variant="outline"
                                    onClick={() => setSent(false)}
                                    className="w-full border-white/10 text-white/60 hover:bg-white hover:text-black font-black uppercase tracking-widest text-xs h-12 transition-all"
                                >
                                    Try Alternative Command
                                </Button>
                            </div>
                        ) : (
                            <form onSubmit={handleLogin} className="space-y-4">
                                <div className="space-y-2">
                                    <Input
                                        type="email"
                                        placeholder="SYNCID@RANKFORGE.AI"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                        className="bg-black border-white/10 text-white placeholder:text-white/10 focus:border-white focus:ring-0 h-14 font-black tracking-widest uppercase transition-all"
                                    />
                                </div>
                                <Button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full h-12 bg-white text-black hover:bg-gray-200 font-semibold transition-all"
                                >
                                    {loading ? (
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    ) : (
                                        <>
                                            <Zap className="mr-2 h-4 w-4" />
                                            Sign In with Magic Link
                                        </>
                                    )}
                                </Button>
                            </form>
                        )}
                    </CardContent>
                </Card>

                <div className="text-center text-[10px] text-white/10 font-black uppercase tracking-[0.3em] font-mono">
                    SECURE PROTOCOL ACTIVE / BY SYNCING YOU AGREE TO DATA TERMS
                </div>
            </div>
        </div>
    )
}
