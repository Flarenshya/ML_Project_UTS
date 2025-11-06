import React, { useState } from "react";
import axios from "axios";

function App() {
  const [video, setVideo] = useState(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("video", video);
    formData.append("title", title);
    formData.append("description", description);
    formData.append("email", email);
    formData.append("phone", phone);

    await axios.post("http://localhost:4000/api/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white px-8">
      <div className="grid md:grid-cols-2 gap-10 items-center w-full max-w-6xl">
        {/* Left Section */}
        <div>
          <div className="mb-5 inline-block bg-gray-800 text-gray-300 text-sm px-4 py-1 rounded-full">
            2025 • Machine Learning
          </div>
          <h1 className="text-6xl font-extrabold leading-none mb-7">
            <span className="text-white">smart</span>
            <br />
            <span className="text-whitefont-bold">
              uploader
            </span>
          </h1>
          <p className="italic text-lg text-blue-300 mb-3">
            AutoVid Connect — upload once, share everywhere.
          </p>
          <p className="text-gray-300 max-w-md leading-relaxed">
            Automatically post your videos to YouTube and get instant
            notifications via WhatsApp and email when it’s done.
          </p>
        </div>

        {/* Right Section - Upload Form */}
        <div className="bg-white text-black rounded-3xl shadow-2xl p-8 w-full max-w-md mx-auto">
          <div className="flex items-center mb-5">
            <label className="bg-[#0040ff] text-white font-medium py-2 px-10 rounded-full cursor-pointer hover:bg-blue-700">
              Choose File
              <input
                type="file"
                onChange={(e) => setVideo(e.target.files[0])}
                className="hidden"
              />
            </label>
            <span className="ml-3 text-gray-500 text-sm">
              {video ? video.name : "No File Chosen"}
            </span>
          </div>

          <input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
             className="w-full p-3 mb-3 border border-gray-300 rounded-full focus:border-[#7a1eff] focus:ring-2 focus:ring-[#7a1eff] focus:outline-none"
          />
          <input
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
             className="w-full p-3 mb-3 border border-gray-300 rounded-full focus:border-[#7a1eff] focus:ring-2 focus:ring-[#7a1eff] focus:outline-none"
          />
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
             className="w-full p-3 mb-3 border border-gray-300 rounded-full focus:border-[#7a1eff] focus:ring-2 focus:ring-[#7a1eff] focus:outline-none"
          />
          <input
            placeholder="Phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
             className="w-full p-3 mb-5 border border-gray-300 rounded-full focus:border-[#7a1eff] focus:ring-2 focus:ring-[#7a1eff] focus:outline-none"
          />

          <button
            onClick={handleUpload}
            className="w-full bg-purple-600 text-white py-3 rounded-full font-semibold hover:bg-purple-700 transition"
          >
            Upload File
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
