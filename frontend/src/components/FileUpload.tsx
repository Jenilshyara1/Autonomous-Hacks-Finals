import React, { useState } from 'react';
import axios from 'axios';
import { Upload, Loader2, AlertCircle } from 'lucide-react';

interface FileUploadProps {
    onUploadComplete: (result: any) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUploadComplete }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleUpload(files[0]);
        }
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            handleUpload(e.target.files[0]);
        }
    };

    const handleUpload = async (file: File) => {
        if (!file) return;

        // Validate type
        const validTypes = ['.eml', '.txt'];
        const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
        if (!validTypes.includes(extension)) {
            setError("Invalid file type. Please upload .eml or .txt");
            return;
        }

        setIsUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Assuming Vite proxy redirects /api to backend
            const response = await axios.post('/api/v1/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onUploadComplete(response.data);
        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || "Upload failed. Please try again.");
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="w-full max-w-2xl mx-auto">
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`relative border-2 border-dashed rounded-xl p-8 transition-all duration-200 ease-in-out text-center cursor-pointer ${isDragging
                    ? 'border-indigo-500 bg-indigo-50 scale-[1.01]'
                    : 'border-slate-300 hover:border-slate-400 bg-white/50'
                    } ${isUploading ? 'opacity-75 pointer-events-none' : ''}`}
            >
                <input
                    type="file"
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    onChange={handleFileSelect}
                    accept=".eml,.txt"
                    disabled={isUploading}
                />

                <div className="flex flex-col items-center gap-4">
                    <div className={`p-4 rounded-full ${isDragging ? 'bg-indigo-100' : 'bg-slate-100'}`}>
                        {isUploading ? (
                            <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
                        ) : (
                            <Upload className={`w-8 h-8 ${isDragging ? 'text-indigo-600' : 'text-slate-400'}`} />
                        )}
                    </div>

                    <div className="space-y-1">
                        <h3 className="text-lg font-semibold text-slate-900">
                            {isUploading ? 'Processing Email...' : 'Upload Email File'}
                        </h3>
                        <p className="text-sm text-slate-500">
                            Drag and drop or click to upload (.eml or .txt)
                        </p>
                    </div>
                </div>
            </div>

            {error && (
                <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg flex items-center gap-2">
                    <AlertCircle className="w-5 h-5 flex-shrink-0" />
                    <p className="text-sm">{error}</p>
                </div>
            )}
        </div>
    );
};
