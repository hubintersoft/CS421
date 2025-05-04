import React, { useState, useEffect } from "react";

function App() {
  const [output, setOutput] = useState(
    "Click a button to fetch student or subject data."
  );

  const fetchStudents = () => {
    fetch("http://127.0.0.1:8000/api/students/")
      .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch students");
        return response.json();
      })
      .then((data) => {
        setOutput(JSON.stringify(data, null, 2));
      })
      .catch((error) => {
        setOutput("Error loading students: " + error.message);
      });
  };

  const fetchSubjects = () => {
    fetch("http://127.0.0.1:8000/api/subjects/")
      .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch subjects");
        return response.json();
      })
      .then((data) => {
        setOutput(JSON.stringify(data, null, 2));
      })
      .catch((error) => {
        setOutput("Error loading subjects: " + error.message);
      });
  };

  // Load Google Font
  useEffect(() => {
    const link = document.createElement("link");
    link.href =
      "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap";
    link.rel = "stylesheet";
    document.head.appendChild(link);
  }, []);

  return (
    <div style={styles.body}>
      <div style={styles.container}>
        <h1 style={styles.heading}>🎓 Student & Subject List</h1>
        <div style={styles.buttonGroup}>
          <button style={styles.button} onClick={fetchStudents}>
            Load Students
          </button>
          <button style={styles.button} onClick={fetchSubjects}>
            Load Subjects
          </button>
        </div>
        <pre style={styles.output}>{output}</pre>
      </div>
    </div>
  );
}

const styles = {
  body: {
    fontFamily: "'Inter', sans-serif",
    margin: 0,
    padding: 0,
    background: "#f9f9f9",
    color: "#333",
    minHeight: "100vh",
  },
  container: {
    maxWidth: "960px",
    margin: "50px auto",
    padding: "20px",
    background: "#ffffff",
    borderRadius: "12px",
    boxShadow: "0 8px 16px rgba(0,0,0,0.1)",
    textAlign: "center",
  },
  heading: {
    color: "#2c3e50",
    marginBottom: "30px",
  },
  buttonGroup: {
    display: "flex",
    justifyContent: "center",
    flexWrap: "wrap",
    gap: "15px",
  },
  button: {
    padding: "14px 28px",
    backgroundColor: "#007bff",
    color: "white",
    fontWeight: "600",
    fontSize: "16px",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    transition: "all 0.3s ease",
  },
  output: {
    textAlign: "left",
    background: "#f0f4f8",
    padding: "20px",
    borderLeft: "6px solid #007bff",
    borderRadius: "10px",
    marginTop: "30px",
    maxHeight: "500px",
    overflowY: "auto",
    fontSize: "14px",
  },
};

export default App;
