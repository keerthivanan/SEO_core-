export default function TermsPage() {
    return (
        <div className="min-h-screen bg-black text-white p-8 font-inter">
            <div className="max-w-3xl mx-auto space-y-8 py-12">
                <h1 className="text-4xl font-bold">Terms of Service</h1>
                <p className="text-gray-400">Last updated: February 2026</p>

                <section className="space-y-4">
                    <h2 className="text-2xl font-semibold">1. Acceptance</h2>
                    <p className="text-gray-400 leading-relaxed">
                        By using RankForge AI, you agree to these terms. If you analyze a website, you confirm you have permission to do so.
                    </p>
                </section>

                <section className="space-y-4">
                    <h2 className="text-2xl font-semibold">2. Refunds</h2>
                    <p className="text-gray-400 leading-relaxed">
                        We offer a 90-day money-back guarantee if your rankings do not improve after implementing our fixes.
                    </p>
                </section>
            </div>
        </div>
    )
}
