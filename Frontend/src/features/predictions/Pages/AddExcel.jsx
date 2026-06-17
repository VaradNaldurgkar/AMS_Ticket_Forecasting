import React, { useState, useEffect } from "react";
import axios from "axios";

import {
  FaFileExcel,
  FaUpload,
  FaCheckCircle,
  FaFolderOpen,
  FaCalendarAlt,
  FaDatabase
} from "react-icons/fa";

import "../css/AddExcel.css";

const AddExcel = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const [showSuccess, setShowSuccess] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState("");
  const [uploads, setUploads] = useState([]);

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const fetchUploads = async () => {
  try {
    const response = await axios.get(
      "http://localhost:8000/api/uploads"
    );

    setUploads(response.data);
  } catch (error) {
    console.error(error);
  }
};

useEffect(() => {
  fetchUploads();
}, []);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select an Excel file");
      return;
    }

    try {
      setUploading(true);

      const formData = new FormData();

      formData.append("file", file);

      await axios.post(
        "http://localhost:8000/api/upload-excel",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }
      );

      setUploadedFileName(file.name);

setShowSuccess(true);

setFile(null);

fetchUploads();

    } catch (error) {

      console.error(error);

      if (error.response) {
        alert(
          error.response.data.message ||
          "Upload failed"
        );
      } else {
        alert(
          "Unable to connect to FastAPI server"
        );
      }

    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="excel-page">

      {/* Header */}

      <div className="excel-header">
        <h1>Add Excel File</h1>

        <p>
          Upload Excel datasets for AMS analysis and forecasting.
        </p>
      </div>

      {/* Statistics Cards */}

      <div className="excel-stats-grid">

        <div className="excel-stat-card">
          <div className="excel-stat-icon excel-green">
            <FaFolderOpen />
          </div>

          <div className="excel-stat-info">
            <h4>Total Files</h4>
            <h2>{uploads.length}</h2>
            <span>Uploaded Files</span>
          </div>
        </div>

        <div className="excel-stat-card">
          <div className="excel-stat-icon excel-blue">
            <FaCalendarAlt />
          </div>

          <div className="excel-stat-info">
            <h4>Last Upload</h4>
            <h2>
  {uploads.length > 0
    ? uploads[0].upload_date
    : "--"}
</h2>

<span>Latest File</span>
          </div>
        </div>

        <div className="excel-stat-card">
          <div className="excel-stat-icon excel-orange">
            <FaDatabase />
          </div>

          <div className="excel-stat-info">
            <h4>Datasets</h4>
            <h2>{uploads.length}</h2>
            <span>Active Datasets</span>
          </div>
        </div>

        <div className="excel-stat-card">
          <div className="excel-stat-icon excel-purple">
            <FaFileExcel />
          </div>

          <div className="excel-stat-info">
            <h4>Total Size</h4>
            <h2>
  {uploads
    .reduce(
      (sum, file) => sum + file.size_mb,
      0
    )
    .toFixed(2)}
  {" "}MB
</h2>
            <span>Storage Used</span>
          </div>
        </div>

      </div>

      {/* Upload + Guidelines */}

      <div className="excel-content">

        <div className="excel-upload-card">

          <h2>Upload Excel File</h2>

          <div className="excel-dropzone">

            <FaFileExcel className="excel-icon" />

            <h3 className="excel-upload-title">
              Drag & Drop your Excel file here
            </h3>

            <p className="excel-upload-subtitle">
              or browse your system
            </p>

            <label
              htmlFor="excel-upload"
              className="excel-browse-btn"
            >
              Browse File
            </label>

            <input
              id="excel-upload"
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileChange}
              className="excel-file-input"
            />

          </div>

          {file && (
            <div className="excel-file-preview">

              <div>

                <div className="excel-file-name">
                  📄 {file.name}
                </div>

                <div className="excel-file-size">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </div>

              </div>

              <FaCheckCircle
                size={24}
                color="#16a34a"
              />

            </div>
          )}

          <button
            className="excel-upload-btn"
            onClick={handleUpload}
            disabled={uploading}
          >
            <FaUpload />

            {uploading
              ? "Uploading..."
              : "Upload Dataset"}
          </button>

        </div>

        <div className="excel-guidelines-card">

          <h2>Upload Guidelines</h2>

          <ul className="excel-guidelines-list">

            <li>✓ Upload only Excel files (.xlsx, .xls)</li>

            <li>✓ Maximum file size is 20 MB</li>

            <li>✓ Ensure AMS template is followed</li>

            <li>✓ First row should contain column headers</li>

            <li>✓ No empty rows or columns</li>

            <li>✓ Remove password protection before upload</li>

          </ul>

          <div className="excel-info-box">
            Make sure your data follows AMS standards for
            accurate forecasting and analysis.
          </div>

        </div>

      </div>

      {/* Recent Uploads */}

      <div className="excel-recent-section">

        <div className="excel-recent-header">
          <h2>Recent Uploads</h2>
          <span>View All</span>
        </div>

        <table className="excel-table">

          <thead>
            <tr>
              <th>File Name</th>
              <th>Dataset Type</th>
              <th>Uploaded By</th>
              <th>Upload Date</th>
              <th>Size</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>

  {uploads.length > 0 ? (

    uploads.map((upload, index) => (

      <tr key={index}>

        <td>{upload.file_name}</td>

        <td>Excel Dataset</td>

        <td>Admin</td>

        <td>{upload.upload_date}</td>

        <td>{upload.size_mb} MB</td>

        <td>
          <span className="excel-status-success">
            {upload.status}
          </span>
        </td>

      </tr>

    ))

  ) : (

    <tr>

      <td
        colSpan="6"
        style={{
          textAlign: "center",
          padding: "20px"
        }}
      >
        No files uploaded yet
      </td>

    </tr>

  )}

</tbody>

        </table>

      </div>

      {/* Success Popup */}

      {showSuccess && (
  <div className="excel-modal-overlay">

    <div className="excel-success-modal">

      <div className="excel-success-icon">
        ✓
      </div>

      <h2>Upload Successful</h2>

      <p className="excel-success-text">
        Your file has been uploaded successfully.
      </p>

      <div className="excel-success-file">
        📄 {uploadedFileName}
      </div>

      <div className="excel-success-actions">

        <button
          className="excel-secondary-btn"
          onClick={() => setShowSuccess(false)}
        >
          Upload Another
        </button>

        <button
          className="excel-success-btn"
          onClick={() => setShowSuccess(false)}
        >
          Done
        </button>

      </div>

    </div>

  </div>
)}

    </div>
  );
};

export default AddExcel;