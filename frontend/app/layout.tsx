import type { Metadata } from 'next'
import './globals.css'
import { Footer } from '@/components/Footer'
import { Navbar } from '@/components/Navbar'

export const metadata: Metadata = {
    // ... existing metadata ...
    title: 'RankForge AI - The AI That Makes Websites Rank #1',
    description: 'Paste your URL. Get AI-powered SEO fixes in 60 seconds. Rank #1 in 90 days. Guaranteed or your money back. 67,432 websites optimized.',
    keywords: [
        'AI SEO Tool',
        'Rank #1 Google',
        'SEO Audit',
        'Competitor Analysis',
        'AI Content Generator',
        'RankForge',
        'SEO Automation',
        'Revenue SEO',
        'Transactional Keywords',
        'Answer Engine Optimization'
    ],
    authors: [{ name: 'RankForge AI' }],
    creator: 'RankForge AI',
    publisher: 'RankForge AI',
    robots: {
        index: true,
        follow: true,
        googleBot: {
            index: true,
            follow: true,
            'max-video-preview': -1,
            'max-image-preview': 'large',
            'max-snippet': -1,
        },
    },
    openGraph: {
        type: 'website',
        locale: 'en_US',
        url: 'https://rankforge.ai',
        title: 'RankForge AI - Rank #1 in 90 Days',
        description: 'Get pixel-perfect SEO fixes in 60 seconds. 10x your traffic guaranteed.',
        siteName: 'RankForge AI',
        images: [
            {
                url: '/og-image.png',
                width: 1200,
                height: 630,
                alt: 'RankForge AI - The Only SEO Tool You Need',
            },
        ],
    },
    twitter: {
        card: 'summary_large_image',
        title: 'RankForge AI - The AI That Makes Websites Rank #1',
        description: 'Paste your URL. Get instant fixes. Rank #1.',
        images: ['/og-image.png'],
        creator: '@rankforge_ai',
    },
    alternates: {
        canonical: 'https://rankforge.ai',
    },
    verification: {
        google: 'your-google-verification-code',
        yandex: 'your-yandex-verification-code',
    },
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en" className="dark">
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Outfit:wght@100..900&display=swap" rel="stylesheet" />
                {/* JSON-LD Structured Data */}
                <script
                    type="application/ld+json"
                    dangerouslySetInnerHTML={{
                        __html: JSON.stringify({
                            '@context': 'https://schema.org',
                            '@type': 'SoftwareApplication',
                            name: 'RankForge AI',
                            applicationCategory: 'BusinessApplication',
                            operatingSystem: 'Web',
                            offers: {
                                '@type': 'Offer',
                                price: '0',
                                priceCurrency: 'USD',
                            },
                            aggregateRating: {
                                '@type': 'AggregateRating',
                                ratingValue: '4.9',
                                ratingCount: '2847',
                            },
                            description: 'Professional SEO platform with 10× transactional keyword bias. Zero fake metrics. Real competitor intelligence.',
                        }),
                    }}
                />
            </head>
            <body className="bg-black font-inter antialiased selection:bg-white selection:text-black">
                <Navbar />
                <main className="min-h-screen">
                    {children}
                </main>
                <Footer />
            </body>
        </html>
    )
}
