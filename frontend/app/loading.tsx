export default function Loading() {
    return (
        <div className="min-h-screen bg-black flex items-center justify-center">
            <div className="flex flex-col items-center gap-4">
                <div className="w-12 h-12 border-2 border-white/10 border-t-white rounded-full animate-spin" />
                <p className="text-gray-500 font-mono text-xs uppercase tracking-widest animate-pulse">Loading System...</p>
            </div>
        </div>
    )
}
