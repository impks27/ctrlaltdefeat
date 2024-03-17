import React, { useState } from "react";

interface PdfFile {
  file: File;
  documentURL: string;
}

const PdfUploadComponent: React.FC = () => {
  const [rows, setRows] = useState<PdfFile[][]>([[]]);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [yearOfReport, setYearOfReport] = useState<string>("");

  const handleFileChange = (
    rowIndex: number,
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const files = Array.from(e.target.files || []);
    const errorMessage = files.some((file) => file.type !== "application/pdf")
      ? "Please select only PDF files."
      : "";
    setRows((prevRows) => {
      const newRows = [...prevRows];
      newRows[rowIndex] = files.map((file) => ({
        file,
        documentURL: "",
      }));
      return newRows;
    });
    setErrorMessage(errorMessage);
  };

  const handleAddRow = () => {
    setRows((prevRows) => [...prevRows, []]);
  };

  const handleYearOfReportChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setYearOfReport(e.target.value);
  };

  const handleUpload = async () => {
    try {
      const formData = new FormData();
      rows.flat().forEach((pdfFile, index) => {
        formData.append(`documentName`, pdfFile.file); // Correct field name
        formData.append(`DocumentURL`, pdfFile.documentURL); // Correct field name
      });
      formData.append("YearOfReport", yearOfReport); // Append YearOfReport once
      const response = await fetch("http://127.0.0.1:8000/esgreports/upload", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error("Failed to upload PDF files");
      }
      setRows([[]]);
      setErrorMessage("");
      setYearOfReport("");
      console.log("PDF files uploaded successfully");
    } catch (error) {
      console.error("Error uploading PDF files:", error);
      setErrorMessage("Failed to upload PDF files");
    }
  };

  return (
    <div className="p-4">
      <div className="mb-4">
        <input
          type="text"
          placeholder="Enter Year of Report"
          value={yearOfReport}
          onChange={handleYearOfReportChange}
          className="mb-2"
        />
      </div>
      {rows.map((row, rowIndex) => (
        <div key={rowIndex} className="mb-4">
          <input
            type="file"
            accept=".pdf"
            multiple
            onChange={(e) => handleFileChange(rowIndex, e)}
            className="mb-2"
          />
          {row.map((pdf, fileIndex) => (
            <div key={fileIndex} className="mb-2">
              <span className="mr-2">{pdf.file.name}</span>
              <span>({(pdf.file.size / 1024).toFixed(2)} KB)</span>
              <input
                type="text"
                placeholder="Document URL"
                value={pdf.documentURL}
                onChange={(e) => {
                  const newRows = [...rows];
                  newRows[rowIndex][fileIndex].documentURL = e.target.value;
                  setRows(newRows);
                }}
                className="ml-2 mr-2"
              />
            </div>
          ))}
        </div>
      ))}
      <button
        onClick={handleAddRow}
        className="bg-blue-500 text-white px-4 py-2 rounded mr-2 hover:bg-blue-600"
      >
        Add PDF
      </button>
      <button
        disabled={!rows.flat().length || errorMessage.length > 0}
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Upload
      </button>
      {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}
    </div>
  );
};

export default PdfUploadComponent;
