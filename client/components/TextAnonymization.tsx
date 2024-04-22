import React, { useState } from 'react';

interface TextAnonymizationProps {
    onError: (message: string) => void;
}

const TextAnonymization: React.FC<TextAnonymizationProps> = ({ onError }) => {
    const [text, setText] = useState('');
    const [anonymizedText, setAnonymizedText] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        onError('');
        setLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:5000/api/anonymize/text/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            const data = await response.json();
            if (data.error) {
                onError(data.error);
            } else {
                setAnonymizedText(data);
            }
        } catch (error) {
            console.error('Error:', error);
            onError('An error occurred while processing the request.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            <form onSubmit={handleSubmit} className="bg-white shadow-md rounded p-8 mb-4">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="text">
                        Text
                    </label>
                    <textarea
                        id="text"
                        placeholder="Enter text to anonymize"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        className="shadow appearance-none border rounded w-full p-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        rows={5}
                    />
                </div>

                <div className="flex items-center justify-center">
                    <button
                        type="submit"
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold p-2 rounded focus:outline-none focus:shadow-outline"
                    >
                        Anonymize
                    </button>
                </div>
            </form>

            <div className="bg-white text-gray-700 shadow-md rounded p-8">
                <div>
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="anonymizedText">
                        Anonymized Text
                    </label>
                    {!loading && !anonymizedText && <p className="text-sm text-gray-500">The anonymized text will appear here.</p>}
                    {loading && <p className="text-sm text-gray-500">Loading...</p>}
                    {anonymizedText && (
                        <textarea
                            id="anonymizedText"
                            value={anonymizedText}
                            readOnly
                            className="shadow appearance-none border rounded w-full p-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            rows={5}
                        />
                    )}
                </div>
            </div>
        </div>
    );
};

export default TextAnonymization; 