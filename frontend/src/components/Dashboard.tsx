import { useState } from 'react';
import axios from 'axios';
import { FileUpload } from './FileUpload';
import { Download, Shield, ShieldAlert, CheckCircle2, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface LogEntry {
    metadata: any;
    is_privileged: boolean;
    privilege_type: string | null;
    log_description: string | null;
    reasoning: string | null;
}

export const Dashboard = () => {
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const { logout, user } = useAuth();

    const handleUploadComplete = (result: LogEntry) => {
        setLogs((prev) => [result, ...prev]);
    };

    return (
        <div className="min-h-screen bg-slate-50 p-6 md:p-12 font-sans">
            <header className="max-w-5xl mx-auto mb-12 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Privilege Log Portal</h1>
                    <p className="text-slate-500 mt-2">Welcome, {user?.username || 'User'}</p>
                </div>
                <div className="flex gap-4">
                    <button
                        onClick={async () => {
                            try {
                                const response = await axios.get('/api/v1/export', {
                                    responseType: 'blob',
                                    headers: {
                                        // The token is automatically handled by the interceptor if setup, 
                                        // or we grab it from localStorage if that's how this app works.
                                        // Based on useAuth usage, it likely sets the default header.
                                        // If not, we might need: 'Authorization': `Bearer ${localStorage.getItem('token')}`
                                    }
                                });
                                const url = window.URL.createObjectURL(new Blob([response.data]));
                                const link = document.createElement('a');
                                link.href = url;
                                link.setAttribute('download', 'privilege_log.csv');
                                document.body.appendChild(link);
                                link.click();
                                link.remove();
                                window.URL.revokeObjectURL(url);
                            } catch (error) {
                                console.error("Export failed", error);
                                alert("Failed to download CSV. Please try again.");
                            }
                        }}
                        className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors font-medium text-sm"
                    >
                        <Download className="w-4 h-4" />
                        Download CSV
                    </button>
                    <button
                        onClick={logout}
                        className="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors font-medium text-sm"
                    >
                        <LogOut className="w-4 h-4" />
                        Sign Out
                    </button>
                </div>
            </header>

            <main className="max-w-5xl mx-auto space-y-12">
                <section>
                    <FileUpload onUploadComplete={handleUploadComplete} />
                </section>

                {logs.length > 0 && (
                    <section className="space-y-6">
                        <h2 className="text-xl font-semibold text-slate-900 flex items-center gap-2">
                            <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                            Processed Items
                        </h2>

                        <div className="grid gap-4">
                            {logs.map((log, idx) => (
                                <div key={idx} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 transition-all hover:shadow-md">
                                    <div className="flex items-start justify-between gap-4">
                                        <div className="space-y-2">
                                            <div className="flex items-center gap-3">
                                                <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${log.is_privileged
                                                    ? 'bg-amber-50 text-amber-700 border border-amber-200'
                                                    : 'bg-slate-100 text-slate-600 border border-slate-200'
                                                    }`}>
                                                    {log.is_privileged ? (
                                                        <>
                                                            <ShieldAlert className="w-3.5 h-3.5" />
                                                            Privileged
                                                        </>
                                                    ) : (
                                                        <>
                                                            <Shield className="w-3.5 h-3.5" />
                                                            Not Privileged
                                                        </>
                                                    )}
                                                </span>
                                                <span className="text-slate-500 text-sm font-medium">{log.metadata?.Subject || "No Subject"}</span>
                                            </div>

                                            {log.is_privileged && (
                                                <div className="bg-slate-50 rounded-lg p-3 text-sm mt-3 border border-slate-100">
                                                    <div className="grid grid-cols-[100px_1fr] gap-2 mb-2">
                                                        <span className="text-slate-500 font-medium">Type:</span>
                                                        <span className="text-slate-900">{log.privilege_type || "N/A"}</span>
                                                    </div>
                                                    <div className="grid grid-cols-[100px_1fr] gap-2">
                                                        <span className="text-slate-500 font-medium">Description:</span>
                                                        <span className="text-slate-900">{log.log_description}</span>
                                                    </div>
                                                </div>
                                            )}

                                            {!log.is_privileged && (
                                                <p className="text-sm text-slate-600 mt-2">
                                                    This document was analyzed and deemed not privileged.
                                                </p>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>
                )}
            </main>
        </div>
    );
}
