export default function PrivacyPage() {
    return (
        <div className="min-h-screen bg-black text-white p-8 font-inter">
            <div className="max-w-3xl mx-auto space-y-8 py-12">
                <h1 className="text-4xl font-bold">Privacy Policy</h1>
                <p className="text-gray-400">Last updated: February 2026</p>

                <section className="space-y-4">
                    <h2 className="text-2xl font-semibold">1. Data We Collect</h2>
                    <p className="text-gray-400 leading-relaxed">
                        We collect URLs you analyze, email addresses for account creation, and usage data to improve our AI models.
                        We do NOT sell your data to third parties.
                    </p>
                </section>

                <section className="space-y-4">
                    <h2 className="text-2xl font-semibold">2. How We Use It</h2>
                    <p className="text-gray-400 leading-relaxed">
                        - To generate SEO reports
                        - To verify your subscription status (via Stripe)
                        - To send you ranking alerts (if opted in)
                    </p>
                </section>
            </div>
        </div>
    )
}
