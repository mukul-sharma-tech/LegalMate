// 'use client';

// import React, { useState } from 'react';
// import Link from 'next/link';

// // --- Type Definitions ---
// interface RightsResult {
//   explanation: string;
//   relevantLaws: { title: string; text: string; }[];
//   guidance: string;
//   disclaimer: string;
// }

// // --- SVG Icons ---
// const SearchIcon = ({ className }: {className?: string}) => (
//     <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
//         <circle cx="11" cy="11" r="8"></circle>
//         <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
//     </svg>
// );

// const MicIcon = ({ className }: {className?: string}) => (
//     <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
//         <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
//         <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
//         <line x1="12" y1="19" x2="12" y2="22"></line>
//     </svg>
// );

// const BookOpenIcon = ({ className }: {className?: string}) => (
//      <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
//         <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
//         <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
//     </svg>
// );

// const LightbulbIcon = ({ className }: {className?: string}) => (
//     <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
//         <path d="M15.09 16.05A6.47 6.47 0 0 1 12 20a6.47 6.47 0 0 1-3.09-3.95"></path><path d="M12 20v2"></path><path d="M12 14v-4"></path><path d="M8.5 8.5 7 7"></path><path d="M17 7l-1.5 1.5"></path><path d="M2 12h2"></path><path d="M20 12h2"></path><path d="m12 2 3.5 3.5"></path><path d="M8.5 5.5 12 2"></path><path d="M12 2a6.5 6.5 0 0 1 5.92 9.08"></path><path d="M3 11.08A6.5 6.5 0 0 1 8.92 2"></path>
//     </svg>
// );
// const AlertTriangleIcon = ({ className }: {className?: string}) => (
//     <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
//         <path d="m21.73 18-8-14a2 2 0 0 0-3.46 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><path d="M12 9v4"></path><path d="M12 17h.01"></path>
//     </svg>
// );

// // --- Sample Data ---
// const sampleRightsQuery = "What are my rights if my employer doesn’t pay my salary?";
// const sampleRightsResult: RightsResult = {
//     explanation: "You have a fundamental right to be paid your full salary on time for the work you have done. Your employer cannot legally delay, reduce, or deny your payment without a valid, lawful justification.",
//     relevantLaws: [
//         { title: "Article 21 - Right to Life & Livelihood", text: "The Supreme Court has interpreted this to include the right to a livelihood, which means timely payment of wages is essential for a dignified life." },
//         { title: "Payment of Wages Act, 1936", text: "This law regulates the payment of wages to employees and ensures that they are paid on time and without any unauthorized deductions." }
//     ],
//     guidance: "If you have not been paid, you can file a formal complaint with the labor commissioner's office in your area or seek assistance from a labor lawyer to recover your unpaid wages.",
//     disclaimer: "This is simplified legal information and not legal advice. For formal action, it is recommended to consult with a qualified legal professional."
// };

// export default function KnowYourRightsPage() {
//     const [query, setQuery] = useState<string>(sampleRightsQuery);
//     const [isLoading, setIsLoading] = useState<boolean>(false);
//     const [result, setResult] = useState<RightsResult | null>(null);

//     const handleSearch = () => {
//         setIsLoading(true);
//         setResult(null);
//         setTimeout(() => {
//             setResult(sampleRightsResult);
//             setIsLoading(false);
//         }, 1500);
//     };

//     return (
//         <main className="flex flex-col items-center min-h-screen p-4 bg-slate-900 text-white">
//             <div className="w-full max-w-4xl mx-auto px-4 py-12">
//                 <Link href="/" className="mb-8 text-sky-400 hover:text-sky-300 transition-colors inline-block">&larr; Back to Home</Link>
//                 <div className="text-center mb-12">
//                     <h1 className="text-4xl font-bold text-white">Know Your Rights</h1>
//                     <p className="text-lg text-slate-300 mt-2">Ask a general question to understand your legal rights in any situation.</p>
//                 </div>

//                 <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
//                     <div className="flex flex-col md:flex-row gap-4">
//                         <div className="relative flex-grow">
//                              <input
//                                 type="text"
//                                 value={query}
//                                 onChange={(e) => setQuery(e.target.value)}
//                                 placeholder="Ask a question like: 'What are my rights as a tenant?'"
//                                 className="w-full bg-slate-900 border border-slate-700 rounded-lg p-4 pl-12 text-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-none transition-shadow"
//                             />
//                             <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-500" />
//                         </div>
//                         <button className="p-4 bg-slate-700 rounded-lg hover:bg-slate-600 transition-colors">
//                             <MicIcon className="w-6 h-6 text-sky-300"/>
//                         </button>
//                         <button onClick={handleSearch} disabled={isLoading || !query} className="bg-sky-600 text-white font-semibold py-4 px-8 rounded-lg hover:bg-sky-500 disabled:bg-slate-600 disabled:cursor-not-allowed transition-colors">
//                             {isLoading ? 'Searching...' : 'Ask'}
//                         </button>
//                     </div>
//                 </div>
                
//                 {isLoading && (
//                     <div className="text-center p-12">
//                         <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-400 mx-auto"></div>
//                     </div>
//                 )}

//                 {result && !isLoading && (
//                     <div className="mt-8 space-y-6">
//                         <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
//                             <p className="text-lg text-slate-300">{result.explanation}</p>
//                         </div>
//                          <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
//                             <div className="flex items-center gap-3 mb-4">
//                                 <BookOpenIcon className="w-7 h-7 text-sky-400" />
//                                 <h3 className="text-2xl font-semibold text-white">Relevant Rights & Laws</h3>
//                             </div>
//                             <div className="space-y-3">
//                                 {result.relevantLaws.map((law, index) => (
//                                     <div key={index} className="bg-slate-800/60 p-4 rounded-lg border border-slate-700/70">
//                                         <h4 className="font-bold text-sky-300">{law.title}</h4>
//                                         <p className="text-slate-300">{law.text}</p>
//                                     </div>
//                                 ))}
//                             </div>
//                         </div>
//                          <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
//                             <div className="flex items-center gap-3 mb-4">
//                                 <LightbulbIcon className="w-7 h-7 text-amber-400" />
//                                 <h3 className="text-2xl font-semibold text-white">Guidance</h3>
//                             </div>
//                             <p className="text-slate-300">{result.guidance}</p>
//                         </div>
//                          <div className="bg-slate-800/50 p-6 rounded-xl border border-amber-500/30">
//                             <div className="flex items-center gap-3">
//                                 <AlertTriangleIcon className="w-6 h-6 text-amber-400 flex-shrink-0" />
//                                 <p className="text-slate-400 text-sm">{result.disclaimer}</p>
//                             </div>
//                         </div>
//                     </div>
//                 )}
//             </div>
//         </main>
//     );
// }


'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowLeftIcon } from '@heroicons/react/24/solid';

// --- Type Definitions ---
interface RightsResult {
  explanation: string;
  relevantLaws: { title: string; text: string; }[];
  guidance: string;
  disclaimer: string;
}

interface ApiResponse {
  explanation?: string;
  relevantLaws?: { title: string; text: string; }[];
  guidance?: string;
  disclaimer?: string;
  error?: string;
}

// --- SVG Icons ---
const SearchIcon = ({ className }: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
);

const MicIcon = ({ className }: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        <line x1="12" y1="19" x2="12" y2="22"></line>
    </svg>
);

const BookOpenIcon = ({ className }: {className?: string}) => (
     <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
    </svg>
);

const LightbulbIcon = ({ className }: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M15.09 16.05A6.47 6.47 0 0 1 12 20a6.47 6.47 0 0 1-3.09-3.95"></path>
        <path d="M12 20v2"></path>
        <path d="M12 14v-4"></path>
        <path d="M8.5 8.5 7 7"></path>
        <path d="M17 7l-1.5 1.5"></path>
        <path d="M2 12h2"></path>
        <path d="M20 12h2"></path>
        <path d="m12 2 3.5 3.5"></path>
        <path d="M8.5 5.5 12 2"></path>
        <path d="M12 2a6.5 6.5 0 0 1 5.92 9.08"></path>
        <path d="M3 11.08A6.5 6.5 0 0 1 8.92 2"></path>
    </svg>
);

const AlertTriangleIcon = ({ className }: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="m21.73 18-8-14a2 2 0 0 0-3.46 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path>
        <path d="M12 9v4"></path>
        <path d="M12 17h.01"></path>
    </svg>
);

const AlertCircleIcon = ({ className }: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
    </svg>
);

const CheckCircleIcon = ({ className }: {className?: string}) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
    </svg>
);

// --- Sample Questions for better UX ---
const sampleQuestions = [
    "What are my rights if my employer doesn't pay my salary?",
    "Can my landlord evict me without notice?",
    "What are my rights as a consumer?",
    "What can I do if I'm discriminated against at work?",
    "What are my rights during police questioning?"
];

export default function KnowYourRightsPage() {
    const [query, setQuery] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [result, setResult] = useState<RightsResult | null>(null);
    const [error, setError] = useState<string>('');
    const [isListening, setIsListening] = useState<boolean>(false);

    const handleSearch = async () => {
        if (!query.trim()) {
            setError('Please enter a question to get started.');
            return;
        }

        setIsLoading(true);
        setResult(null);
        setError('');

        try {
            const response = await fetch('http://localhost:5000/api/know-your-rights', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query.trim() })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data: ApiResponse = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            if (data.explanation && data.relevantLaws && data.guidance && data.disclaimer) {
                setResult({
                    explanation: data.explanation,
                    relevantLaws: data.relevantLaws,
                    guidance: data.guidance,
                    disclaimer: data.disclaimer
                });
            } else {
                throw new Error('Invalid response format from server');
            }

        } catch (err) {
            console.error('Error calling know-your-rights API:', err);
            setError(err instanceof Error ? err.message : 'Failed to get rights information. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !isLoading) {
            handleSearch();
        }
    };

    const handleSampleQuestion = (question: string) => {
        setQuery(question);
        setError('');
        setResult(null);
    };

    const handleVoiceSearch = () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
            const recognition = new SpeechRecognition();
            
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                setIsListening(true);
                setError('');
            };

            recognition.onresult = (event: any) => {
                const transcript = event.results[0][0].transcript;
                setQuery(transcript);
                setIsListening(false);
            };

            recognition.onerror = (event: any) => {
                setError('Speech recognition failed. Please try typing your question.');
                setIsListening(false);
            };

            recognition.onend = () => {
                setIsListening(false);
            };

            recognition.start();
        } else {
            setError('Speech recognition is not supported in your browser.');
        }
    };

    const clearError = () => setError('');

    return (
        <main className="flex flex-col items-center min-h-screen p-4 bg-slate-900 text-white">
            <div className="w-full max-w-4xl mx-auto px-4 py-12">
                <Link href="/" className="inline-flex items-center mb-8 text-sky-400 hover:underline">
                    <ArrowLeftIcon className="w-5 h-5 mr-2" />
                    Back to Home
                </Link>

                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-white">Know Your Rights</h1>
                    <p className="text-lg text-slate-300 mt-2">Ask a general question to understand your legal rights in any situation.</p>
                </div>

                {/* Error Alert */}
                {error && (
                    <div className="mb-6 bg-red-900/50 border border-red-700 rounded-lg p-4 flex items-start gap-3">
                        <AlertCircleIcon className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5" />
                        <div className="flex-grow">
                            <h3 className="font-semibold text-red-300">Error</h3>
                            <p className="text-red-200">{error}</p>
                        </div>
                        <button 
                            onClick={clearError}
                            className="text-red-400 hover:text-red-300 transition-colors"
                        >
                            ×
                        </button>
                    </div>
                )}

                {/* Search Input */}
                <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50 mb-6">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="relative flex-grow">
                             <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Ask a question like: 'What are my rights as a tenant?'"
                                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-4 pl-12 text-slate-300 focus:ring-2 focus:ring-sky-500 focus:outline-none transition-shadow"
                            />
                            <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-6 h-6 text-slate-500" />
                        </div>
                        <button 
                            onClick={handleVoiceSearch}
                            disabled={isListening}
                            className={`p-4 rounded-lg transition-colors ${
                                isListening 
                                    ? 'bg-red-600 hover:bg-red-500' 
                                    : 'bg-slate-700 hover:bg-slate-600'
                            }`}
                            title="Voice search"
                        >
                            <MicIcon className={`w-6 h-6 ${isListening ? 'text-white animate-pulse' : 'text-sky-300'}`}/>
                        </button>
                        <button 
                            onClick={handleSearch} 
                            disabled={isLoading || !query.trim()} 
                            className="bg-sky-600 text-white font-semibold py-4 px-8 rounded-lg hover:bg-sky-500 disabled:bg-slate-600 disabled:cursor-not-allowed transition-colors"
                        >
                            {isLoading ? (
                                <div className="flex items-center justify-center gap-2">
                                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                    Searching...
                                </div>
                            ) : (
                                'Ask'
                            )}
                        </button>
                    </div>
                </div>

                {/* Sample Questions */}
                {!result && !isLoading && (
                    <div className="mb-8">
                        <h3 className="text-lg font-semibold text-white mb-4">Popular Questions</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {sampleQuestions.map((question, index) => (
                                <button
                                    key={index}
                                    onClick={() => handleSampleQuestion(question)}
                                    className="text-left p-4 bg-slate-800/30 hover:bg-slate-800/50 border border-slate-700/50 rounded-lg transition-colors text-slate-300 hover:text-sky-300"
                                >
                                    <span className="text-sky-400 mr-2">Q:</span>
                                    {question}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {/* Loading State */}
                {isLoading && (
                    <div className="text-center p-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-400 mx-auto mb-4"></div>
                        <p className="text-slate-400">Researching your rights and analyzing relevant laws...</p>
                    </div>
                )}

                {/* Results */}
                {result && !isLoading && (
                    <div className="space-y-6">
                        {/* Success Header */}
                        <div className="bg-green-900/30 border border-green-700/50 rounded-lg p-4 flex items-center gap-3">
                            <CheckCircleIcon className="w-6 h-6 text-green-400" />
                            <p className="text-green-300">
                                ✓ Found relevant rights information and legal guidance for your question
                            </p>
                        </div>

                        {/* Main Explanation */}
                        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
                            <div className="flex items-center gap-3 mb-4">
                                <div className="w-8 h-8 bg-sky-600 rounded-full flex items-center justify-center">
                                    <span className="text-white font-bold">?</span>
                                </div>
                                <h3 className="text-2xl font-semibold text-white">Your Rights Explained</h3>
                            </div>
                            <p className="text-lg text-slate-300 leading-relaxed">{result.explanation}</p>
                        </div>

                        {/* Relevant Laws */}
                        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
                            <div className="flex items-center gap-3 mb-4">
                                <BookOpenIcon className="w-7 h-7 text-sky-400" />
                                <h3 className="text-2xl font-semibold text-white">Relevant Rights & Laws</h3>
                            </div>
                            <div className="space-y-4">
                                {result.relevantLaws.map((law, index) => (
                                    <div key={index} className="bg-slate-800/60 p-5 rounded-lg border border-slate-700/70 hover:bg-slate-800/80 transition-colors">
                                        <div className="flex items-start gap-4">
                                            <div className="flex-shrink-0 w-8 h-8 bg-sky-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                                                {index + 1}
                                            </div>
                                            <div>
                                                <h4 className="font-bold text-sky-300 mb-2">{law.title}</h4>
                                                <p className="text-slate-300 leading-relaxed">{law.text}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Guidance */}
                        <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700/50">
                            <div className="flex items-center gap-3 mb-4">
                                <LightbulbIcon className="w-7 h-7 text-amber-400" />
                                <h3 className="text-2xl font-semibold text-white">What You Can Do</h3>
                            </div>
                            <div className="bg-amber-900/20 border border-amber-700/30 rounded-lg p-4">
                                <p className="text-slate-300 leading-relaxed">{result.guidance}</p>
                            </div>
                        </div>

                        {/* Disclaimer */}
                        <div className="bg-slate-800/50 p-6 rounded-xl border border-amber-500/30">
                            <div className="flex items-start gap-3">
                                <AlertTriangleIcon className="w-6 h-6 text-amber-400 flex-shrink-0 mt-1" />
                                <div>
                                    <h4 className="font-semibold text-amber-300 mb-2">Important Disclaimer</h4>
                                    <p className="text-slate-400 text-sm leading-relaxed">{result.disclaimer}</p>
                                </div>
                            </div>
                        </div>

                        {/* Ask Another Question */}
                        <div className="text-center pt-6">
                            <button
                                onClick={() => {
                                    setQuery('');
                                    setResult(null);
                                    setError('');
                                }}
                                className="bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
                            >
                                Ask Another Question
                            </button>
                        </div>
                    </div>
                )}

                {/* No Results Empty State */}
                {!result && !isLoading && !error && query && (
                    <div className="text-center p-12">
                        <div className="w-16 h-16 border-2 border-slate-600 rounded-full flex items-center justify-center mx-auto mb-4">
                            <SearchIcon className="w-8 h-8 text-slate-600" />
                        </div>
                        <p className="text-slate-500">Enter your question above and click &quot;Ask&quot; to get started.</p>
                    </div>
                )}

                {/* Voice Search Status */}
                {isListening && (
                    <div className="fixed bottom-6 right-6 bg-red-600 text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2">
                        <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                        Listening...
                    </div>
                )}
            </div>
        </main>
    );
}