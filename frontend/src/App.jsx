import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [video, setVideo] = useState(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [email, setEmail] = useState("");
  const [sentiment, setSentiment] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [keywords, setKeywords] = useState([]);
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [youtubeLink, setYoutubeLink] = useState("");
  const [token, setToken] = useState("");

  useEffect(() => {
    // Cek apakah ada token di URL setelah login Google
    const query = new URLSearchParams(window.location.search);
    const tokenParams = query.get("token");
    if (tokenParams) {
      setToken(tokenParams);
      // Bersihkan URL agar bersih
      window.history.replaceState({}, document.title, "/");
    }
  }, []);

  const handleConnectGoogle = async () => {
    try {
      const res = await axios.get("/auth/url");
      window.location.href = res.data.url;
    } catch (error) {
      alert("Failed to get auth URL");
    }
  };

  // Validasi email
  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const handleUpload = async () => {
    if (!token) {
      alert("Please connect your YouTube account first!");
      return;
    }

    // Validasi semua field
    if (!video || !title.trim() || !description.trim() || !email.trim()) {
      alert("Please fill in all fields and choose a video!");
      return;
    }

    if (!validateEmail(email)) {
      alert("Please enter a valid email address!");
      return;
    }

    setLoading(true);
    setSentiment(null);
    setConfidence(null);
    setKeywords([]);
    setYoutubeLink("");

    try {
      const formData = new FormData();
      formData.append("video", video);
      formData.append("title", title);
      formData.append("description", description);
      formData.append("email", email);
      formData.append("token", token);

      const res = await axios.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setSentiment(res.data.sentiment);
      setConfidence(res.data.confidence);
      setKeywords(res.data.keywords || []);
      setCategory(res.data.category);
      setYoutubeLink(res.data.youtube_link);
      alert("Video uploaded successfully!");
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.error || "Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-black via-gray-900 to-purple-900 text-white px-8 py-10">
      <div className="grid md:grid-cols-2 gap-10 items-center w-full max-w-6xl">
        {/* Left Section */}
        <div>
          <div className="mb-5 inline-block bg-gray-800 text-gray-300 text-sm px-4 py-1 rounded-full">
            2025 • Machine Learning
          </div>
          <h1 className="text-6xl font-extrabold leading-none mb-7">
            <span className="text-white">smart</span>
            <br />
            <span className="text-whitefont-bold">uploader</span>
          </h1>
          <p className="italic text-lg text-blue-300 mb-3">
            AutoVid Connect — upload once, share everywhere.
          </p>
          <p className="text-gray-300 max-w-md leading-relaxed mb-8">
            Automatically post your videos to YouTube and get instant notifications via WhatsApp and email when it’s done.
          </p>

          {/* Connect Button */}
          {!token ? (
            <button
              onClick={handleConnectGoogle}
              className="bg-white text-black px-6 py-3 rounded-full font-bold flex items-center gap-3 hover:bg-gray-200 transition"
            >
              <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/768px-Google_%22G%22_logo.svg.png" className="w-6 h-6" alt="Google" />
              Connect YouTube Account
            </button>
          ) : (
            <div className="bg-green-600/20 text-green-400 px-6 py-3 rounded-full font-bold flex items-center gap-3 border border-green-500/50 w-fit">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
              Connected to YouTube
            </div>
          )}
        </div>

        {/* Right Section - Upload Form */}
        <div className={`bg-white text-black rounded-3xl shadow-2xl p-8 w-full max-w-md mx-auto transition-opacity ${!token ? 'opacity-50 pointer-events-none grayscale' : ''}`}>
          <div className="flex items-center mb-5">
            <label className="bg-[#0040ff] text-white font-medium py-2 px-8 rounded-full cursor-pointer hover:bg-blue-700 transition">
              Choose File
              <input
                type="file"
                accept="video/mp4" // hanya boleh mp4
                onChange={(e) => {
                  const file = e.target.files[0];
                  if (file && file.type !== "video/mp4") {
                    alert("Only MP4 files are allowed!");
                    e.target.value = null; // reset input
                    setVideo(null);
                    return;
                  }
                  setVideo(file);
                }}
                className="hidden"
                required
              />
            </label>
            <span className="ml-3 text-gray-500 text-sm truncate max-w-[150px]">
              {video ? video.name : "No File Chosen"}
            </span>
          </div>


          <input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full p-3 mb-3 border border-gray-300 rounded-full focus:border-[#7a1eff] focus:ring-2 focus:ring-[#7a1eff] focus:outline-none transition"
          />
          <input
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            className="w-full p-3 mb-3 border border-gray-300 rounded-full focus:border-[#7a1eff] focus:ring-2 focus:ring-[#7a1eff] focus:outline-none transition"
          />
          <input
            placeholder="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full p-3 mb-3 border border-gray-300 rounded-full focus:border-[#7a1eff] focus:ring-2 focus:ring-[#7a1eff] focus:outline-none transition"
          />

          <button
            onClick={handleUpload}
            disabled={loading}
            className="w-full bg-purple-600 text-white py-3 rounded-full font-semibold hover:bg-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : "Upload & Analyze"}
          </button>
        </div>
      </div>

      {/* Result Section (Full Width) */}
      {sentiment && (
        <div className="w-full max-w-6xl mt-12 bg-gray-800/50 p-8 rounded-3xl backdrop-blur-sm border border-gray-700 shadow-2xl animate-fade-in-up">
          <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
            AI Analysis Result
          </h3>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Sentiment */}
            <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-700/50 text-center">
              <span className="text-gray-400 text-xs uppercase tracking-widest mb-2 block">Sentiment</span>
              <p className={`text-4xl font-extrabold ${sentiment === 'positive' ? 'text-green-400' : 'text-red-400'}`}>
                {sentiment.toUpperCase()}
              </p>
            </div>

            {/* Confidence */}
            {confidence && (
              <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-700/50 col-span-2">
                <span className="text-gray-400 text-xs uppercase tracking-widest mb-4 block">Confidence Score</span>
                <div className="flex items-center gap-4">
                  <div className="flex-1 h-4 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-purple-500 to-blue-500 rounded-full transition-all duration-1000 ease-out"
                      style={{ width: confidence }}
                    ></div>
                  </div>
                  <span className="font-mono text-2xl font-bold text-white">{confidence}</span>
                </div>
              </div>
            )}
          </div>

          {/* Keywords */}
          {keywords.length > 0 && (
            <div className="mt-8">
              <span className="text-gray-400 text-xs uppercase tracking-widest block mb-3">Key Topics Detected</span>
              <div className="flex flex-wrap gap-3">
                {keywords.map((word, idx) => (
                  <span key={idx} className="bg-purple-900/30 text-purple-200 px-4 py-2 rounded-xl text-sm border border-purple-500/30 hover:bg-purple-900/50 transition">
                    #{word}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Smart Category */}
          {category && (
            <div className="mt-8 bg-blue-900/20 p-4 rounded-xl border border-blue-500/30 flex items-center gap-4">
              <div className="bg-blue-600 p-2 rounded-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 0 013 12V7a4 4 0 014-4z"></path></svg>
              </div>
              <div>
                <span className="text-blue-300 text-xs uppercase tracking-wider block">Smart Category</span>
                <p className="text-xl font-bold text-white">{category || "Umum"}</p>
              </div>
            </div>
          )}

          {youtubeLink && (
            <div className="mt-8 pt-6 border-t border-gray-700 flex justify-end">
              <a
                href={youtubeLink}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-blue-400 hover:text-blue-300 font-semibold transition group"
              >
                Watch on YouTube
                <svg className="w-5 h-5 group-hover:translate-x-1 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
