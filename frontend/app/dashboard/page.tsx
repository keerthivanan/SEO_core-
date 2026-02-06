'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Loader2, Plus, TrendingUp, Search, Crown } from 'lucide-react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function DashboardPage() {
    const [analyses, setAnalyses] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const supabase = createClient()

    useEffect(() => {
        async function fetchHistory() {
            // In a real scenario with keys, we fetch from Supabase
            const { data: { user } } = await supabase.auth.getUser()

            if (user) {
                const { data } = await supabase
                    .from('analyses')
                    .select('*')
                    .eq('user_id', user.id)
                    .order('created_at', { ascending: false })
                setAnalyses(data || [])
            } else {
                setAnalyses([])
            }
            setLoading(false)
        }

        fetchHistory()
    }, [])

    return (
        <div className="min-h-screen bg-black text-white font-inter">
            {/* Navbar */}
            <nav className="border-b border-zinc-800 bg-black/50 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
                    <Link href="/">
                        <span className="text-xl font-bold tracking-tighter">RANKFORGE<span className="text-gray-500">.AI</span></span>
                    </Link>
                    <div className="flex items-center gap-4">
                        <span className="text-sm text-gray-400">Free Plan</span>
                        <Button variant="outline" className="border-zinc-700 text-white hover:bg-zinc-800" asChild>
                            <Link href="/pricing"><Crown className="w-4 h-4 mr-2 text-yellow-500" /> Upgrade</Link>
                        </Button>
                    </div>
                </div>
            </nav>

            <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">

                {/* Header */}
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                        <p className="text-gray-400">Manage your SEO reports and track rankings.</p>
                    </div>
                    <Button className="bg-white text-black hover:bg-gray-200" asChild>
                        <Link href="/"><Plus className="w-4 h-4 mr-2" /> New Analysis</Link>
                    </Button>
                </div>

                {/* Stats Row */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card className="bg-black border-white/10">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-gray-400">Total Analyses</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">1</div>
                        </CardContent>
                    </Card>
                    <Card className="bg-black border-white/10">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-gray-400">Avg. SEO Score</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">67/100</div>
                        </CardContent>
                    </Card>
                    <Card className="bg-black border-white/10">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm font-medium text-gray-400">Tracked Keywords</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">1</div>
                        </CardContent>
                    </Card>
                </div>

                {/* Rank Tracking Chart */}
                <Card className="bg-black border-white/10">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2"><TrendingUp className="w-4 h-4 text-green-500" /> 30-Day Visibility</CardTitle>
                    </CardHeader>
                    <CardContent className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={[
                                { name: 'Week 1', score: 45 },
                                { name: 'Week 2', score: 52 },
                                { name: 'Week 3', score: 58 },
                                { name: 'Week 4', score: 67 },
                            ]}>
                                <defs>
                                    <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                <XAxis dataKey="name" stroke="#666" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis stroke="#666" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#000', borderColor: '#333', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                                <Area type="monotone" dataKey="score" stroke="#22c55e" strokeWidth={2} fillOpacity={1} fill="url(#colorScore)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>

                {/* History Table */}
                <Card className="bg-black border-white/10">
                    <CardHeader>
                        <CardTitle>Recent Analysis</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {loading ? (
                            <div className="flex justify-center py-8"><Loader2 className="w-8 h-8 animate-spin text-gray-500" /></div>
                        ) : analyses.length === 0 ? (
                            <div className="text-center py-12 space-y-4">
                                <Search className="w-12 h-12 text-gray-600 mx-auto" />
                                <p className="text-gray-400">No analyses found. Start your first scan!</p>
                                <Button variant="outline" asChild>
                                    <Link href="/">Start Analysis</Link>
                                </Button>
                            </div>
                        ) : (
                            <Table>
                                <TableHeader>
                                    <TableRow className="border-zinc-800 hover:bg-zinc-900/50">
                                        <TableHead className="text-gray-400">URL</TableHead>
                                        <TableHead className="text-gray-400">Keyword</TableHead>
                                        <TableHead className="text-gray-400">Overall Score</TableHead>
                                        <TableHead className="text-gray-400">Date</TableHead>
                                        <TableHead className="text-right text-gray-400">Action</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {analyses.map((item) => (
                                        <TableRow key={item.analysis_id} className="border-zinc-800 hover:bg-zinc-800/50">
                                            <TableCell className="font-medium text-white">{item.url}</TableCell>
                                            <TableCell className="text-gray-300">{item.keyword}</TableCell>
                                            <TableCell>
                                                <span className={`px-2 py-1 rounded text-xs font-bold ${item.overall_score >= 80 ? 'bg-green-500/10 text-green-500' :
                                                    item.overall_score >= 50 ? 'bg-yellow-500/10 text-yellow-500' :
                                                        'bg-red-500/10 text-red-500'
                                                    }`}>
                                                    {item.overall_score || item.seo_score}
                                                </span>
                                            </TableCell>
                                            <TableCell className="text-gray-400 text-sm">
                                                {new Date(item.created_at).toLocaleDateString()}
                                            </TableCell>
                                            <TableCell className="text-right">
                                                <Button variant="ghost" size="sm" className="text-blue-400 hover:text-blue-300" asChild>
                                                    <Link href={`/analyze?id=${item.analysis_id}`}>View Report</Link>
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
