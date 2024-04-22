import React, { useState } from 'react';
import { DataGrid, GridColDef, GridToolbar } from '@mui/x-data-grid';

interface CSVAnonymizationProps {
    onError: (message: string) => void;
}

interface ColumnMetadata {
    name: string;
    dataType: 'date' | 'number' | 'string';
    sensitivityType: 'identifier' | 'insensitive' | 'quasi-identifier' | 'sensitive';
}

const CSVAnonymization: React.FC<CSVAnonymizationProps> = ({ onError }) => {
    const [file, setFile] = useState<File | null>(null);
    const [columnMetadata, setColumnMetadata] = useState<ColumnMetadata[]>([]);
    const [anonymizedData, setAnonymizedData] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFile(e.target.files?.[0] || null);

        if (e.target.files?.length) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const csv = e.target?.result as string;
                const lines = csv.split('\n');
                const headers = lines[0].split(',');
                const filteredHeaders = headers.filter((header) => header.trim() !== '');
                const metadata = filteredHeaders.map((header) => ({
                    name: header,
                    dataType: '',
                    sensitivityType: ''
                }));
                setColumnMetadata(metadata as ColumnMetadata[]);
            };
            reader.readAsText(e.target.files[0]);
        }
    };

    const handleMetadataChange = (updatedRow: ColumnMetadata) => {
        const updatedMetadata = columnMetadata.map((metadata) =>
            metadata.name === updatedRow.name ? updatedRow : metadata
        );
        setColumnMetadata(updatedMetadata);
    }

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!file) return;
        onError('');
        setLoading(true);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('column_metadata', JSON.stringify(columnMetadata));

        try {
            const response = await fetch('http://127.0.0.1:5000/api/anonymize/csv', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (data.error) {
                onError(data.error);
            } else {
                // Add an id to each row for the DataGrid component
                setAnonymizedData(data.map((row: any, index: number) => ({ id: index, ...row })));
            }
        } catch (error) {
            console.error('Error:', error);
            onError('An error occurred while processing the request.');
        } finally {
            setLoading(false);
        }
    };

    const columns: GridColDef[] = [
        { field: 'name', headerName: 'Name', flex: 1 },
        {
            field: 'dataType',
            headerName: 'Data Type',
            editable: true,
            type: 'singleSelect',
            valueOptions: ['date', 'number', 'string'],
            flex: 1,
        },
        {
            field: 'sensitivityType',
            headerName: 'Sensitivity Type',
            editable: true,
            type: 'singleSelect',
            valueOptions: ['identifier', 'insensitive', 'quasi-identifier', 'sensitive'],
            flex: 1,
        },
    ];

    return (
        <div className="max-w-2xl mx-auto">
            <form onSubmit={handleSubmit} className="bg-white shadow-md rounded p-8 mb-4">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="file">
                        CSV File
                    </label>
                    <input
                        type="file"
                        id="file"
                        onChange={handleFileChange}
                        className="shadow appearance-none border rounded w-full p-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    />
                </div>

                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Column Metadata</label>
                    <div>
                        <DataGrid
                            autoHeight
                            rows={columnMetadata}
                            columns={columns}
                            getRowId={(row) => row.name}
                            processRowUpdate={(updatedRow) => handleMetadataChange(updatedRow as ColumnMetadata)}
                            onProcessRowUpdateError={(error) => console.error('Error:', error)}
                        />
                    </div>
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
                        Anonymized Data
                    </label>
                    {!loading && anonymizedData.length === 0 && <p className="text-sm text-gray-500">The anonymized data will appear here.</p>}
                    {loading && <p className="text-sm text-gray-500">Loading...</p>}
                    {anonymizedData.length > 0 && (
                        <div className="shadow-md rounded">
                            <DataGrid
                                autoHeight
                                rows={anonymizedData}
                                columns={
                                    anonymizedData.length
                                        ? Object.keys(anonymizedData[0]).filter((key) => key !== 'id').map((key) => ({ field: key, headerName: key, flex: 1 }))
                                        : []
                                }
                                slots={{ toolbar: GridToolbar }}
                            />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CSVAnonymization; 