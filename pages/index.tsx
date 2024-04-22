import React, { useState } from 'react';
import AnonymizationSelector from '../components/AnonymizationSelector';
import CSVAnonymization from '../components/CSVAnonymization';
import TextAnonymization from '../components/TextAnonymization';

const HomePage: React.FC = () => {
    const [anonymizationType, setAnonymizationType] = useState<'text' | 'csv'>('text');
    const [error, setError] = useState<string>('');

    const handleAnonymizationTypeSelect = (type: 'text' | 'csv') => {
        setAnonymizationType(type);
    };

    const handleError = (message: string) => {
        setError(message);
    }

    return (
        <div className="max-w-2xl mx-auto py-8">
            <div className="text-center mb-8">
                <h1 className="text-4xl font-bold mb-2">Data Anonymization Tool</h1>
                <p className="text-gray-500">Protect sensitive data with our powerful anonymization tool.</p>
            </div>

            <AnonymizationSelector onSelect={handleAnonymizationTypeSelect} />

            {error && (
                <div className="flex items-center justify-between bg-red-100 border border-red-400 text-red-700 rounded relative p-3 mb-4" role="alert">
                    <span>{error}</span>
                    <button type="button" onClick={() => setError('')} className="absolute top-0 bottom-0 right-0 px-4 py-3">
                        <svg className="fill-current h-6 w-6 text-red-500" role="button" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                            <title>Close</title>
                            <path fillRule="evenodd" clipRule="evenodd" d="M14.95 5.05a.75.75 0 0 1 1.06 1.06L11.06 10l4.95 4.95a.75.75 0 1 1-1.06 1.06L10 11.06l-4.95 4.95a.75.75 0 0 1-1.06-1.06L8.94 10 4.05 5.05a.75.75 0 0 1 1.06-1.06L10 8.94l4.95-4.95z" />
                        </svg>
                    </button>
                </div>
            )}

            {anonymizationType === 'text' ? <TextAnonymization onError={handleError} /> : <CSVAnonymization onError={handleError} />}
        </div>
    );
};

export default HomePage; 