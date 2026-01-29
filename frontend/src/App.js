import React, { useState } from "react";
import Editor from "@monaco-editor/react";
import axios from "axios";

const App = () => {
  const [fileContent, setFileContent] = useState("");
  const [fileName, setFileName] = useState("");

  const handleSave = async () => {
    try {
      const response = await axios.post(
        `/site/your-site/upload/`,
        {
          fileName: fileName,
          content: fileContent,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log(response.data);
    } catch (error) {
      console.error("Failed to save file.", error);
    }
  };

  return (
    <div>
      <h1>Hosting Manager - File Editor</h1>
      <input
        type="text"
        placeholder="File Name"
        value={fileName}
        onChange={(e) => setFileName(e.target.value)}
      />
      <Editor
        height="60vh"
        defaultLanguage="html"
        defaultValue="<h1>Edit your code here!</h1>"
        onChange={(value) => setFileContent(value)}
      />
      <button onClick={handleSave}>Save</button>
    </div>
  );
};

export default App;