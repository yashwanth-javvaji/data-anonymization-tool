import React, { useState } from 'react';

type AnonymizationType = 'text' | 'csv';

interface AnonymizationSelectorProps {
    onSelect: (type: AnonymizationType) => void;
}

const AnonymizationSelector: React.FC<AnonymizationSelectorProps> = ({ onSelect }) => {
    const [selectedType, setSelectedType] = useState<AnonymizationType>('text');

    const handleSelect = (type: AnonymizationType) => {
        setSelectedType(type);
        onSelect(type);
    };

    return (
        <div className="flex justify-center space-x-4 my-4">
            <button
                className={`px-4 py-2 rounded-md ${selectedType === 'text' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
                onClick={() => handleSelect('text')}
            >
                Text Anonymization
            </button>
            <button
                className={`px-4 py-2 rounded-md ${selectedType === 'csv' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
                onClick={() => handleSelect('csv')}
            >
                CSV Anonymization
            </button>
        </div>
    );
};

export default AnonymizationSelector; 