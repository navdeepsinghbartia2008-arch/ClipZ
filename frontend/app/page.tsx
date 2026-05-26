"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [video, setVideo] = useState<File | null>(null);
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [clips, setClips] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // FILE UPLOAD
  const uploadVideo = async () => {
    if (!video) {
      alert("Please select a video");
      return;
    }

    const formData = new FormData();
    formData.append("file", video);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      setClips(response.data.clips || []);
    } catch (error) {
      console.log(error);
      alert("Upload failed");
    }

    setLoading(false);
  };

  // YOUTUBE LINK
  const uploadYouTube = async () => {
    if (!youtubeUrl) {
      alert("Please enter YouTube URL");
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/youtube",
        {
          url: youtubeUrl,
        }
      );

      setClips(response.data.clips || []);
    } catch (error) {
      console.log(error);
      alert("YouTube processing failed");
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-black text-white overflow-hidden">
      {/* BACKGROUND */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-[-200px] left-[-100px] w-[500px] h-[500px] bg-fuchsia-600 opacity-20 blur-[150px]" />
        <div className="absolute bottom-[-200px] right-[-100px] w-[500px] h-[500px] bg-violet-600 opacity-20 blur-[150px]" />
      </div>

      {/* NAVBAR */}
      <nav className="border-b border-white/10 backdrop-blur-xl sticky top-0 z-50 bg-black/30">
        <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-r from-fuchsia-500 to-violet-600 flex items-center justify-center text-2xl">
              🎬
            </div>

            <h1 className="text-3xl font-black">
              ClipZ
            </h1>
          </div>

          <button className="px-5 py-3 rounded-2xl bg-white/5 border border-white/10">
            AI Powered
          </button>
        </div>
      </nav>

      {/* HERO */}
      <section className="px-6 pt-28 pb-24">
        <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-20 items-center">
          {/* LEFT */}
          <div>
            <div className="inline-flex items-center gap-2 bg-fuchsia-500/10 border border-fuchsia-500/20 px-5 py-2 rounded-full mb-8">
              <span>⚡</span>

              <span className="text-fuchsia-300 font-semibold">
                VIRAL AI CLIPPING
              </span>
            </div>

            <h1 className="text-6xl md:text-8xl font-black leading-none tracking-tight">
              Create
              <br />

              <span className="bg-gradient-to-r from-fuchsia-400 to-violet-500 bg-clip-text text-transparent">
                Viral Clips
              </span>

              <br />
              Instantly
            </h1>

            <p className="text-gray-400 text-xl mt-8 max-w-2xl leading-relaxed">
              Upload videos or paste YouTube links and generate viral clips automatically.
            </p>

            {/* FILE UPLOAD */}
            <div className="mt-12 bg-white/5 border border-white/10 rounded-[30px] p-5 flex flex-col md:flex-row gap-4 items-center">
              <label className="flex-1 w-full cursor-pointer">
                <div className="w-full bg-black/30 border border-white/10 rounded-2xl px-6 py-5 text-gray-300 hover:border-fuchsia-500 transition-all">
                  {video ? video.name : "Choose Video File"}
                </div>

                <input
                  type="file"
                  accept="video/*"
                  onChange={(e) => {
                    if (e.target.files && e.target.files[0]) {
                      setVideo(e.target.files[0]);
                    }
                  }}
                  className="hidden"
                />
              </label>

              <button
                onClick={uploadVideo}
                disabled={loading}
                className="px-10 py-5 rounded-2xl bg-gradient-to-r from-fuchsia-500 to-violet-600 hover:scale-105 transition-all duration-300 font-bold text-lg"
              >
                {loading ? "Processing..." : "Upload"}
              </button>
            </div>

            {/* YOUTUBE */}
            <div className="mt-6 bg-white/5 border border-white/10 rounded-[30px] p-5 flex flex-col md:flex-row gap-4 items-center">
              <input
                type="text"
                placeholder="Paste YouTube video link..."
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                className="flex-1 w-full bg-black/30 border border-white/10 rounded-2xl px-6 py-5 outline-none text-white"
              />

              <button
                onClick={uploadYouTube}
                disabled={loading}
                className="px-10 py-5 rounded-2xl bg-gradient-to-r from-red-500 to-pink-600 hover:scale-105 transition-all duration-300 font-bold text-lg"
              >
                {loading ? "Analyzing..." : "Analyze Link"}
              </button>
            </div>

            <div className="flex gap-8 mt-8 text-gray-500">
              <p>✔ AI Clipping</p>
              <p>✔ Viral Detection</p>
              <p>✔ YouTube Support</p>
            </div>
          </div>

          {/* RIGHT */}
          <div className="relative flex justify-center">
            <div className="absolute w-[500px] h-[500px] bg-fuchsia-500/20 blur-[140px] rounded-full" />

            <div className="relative w-[340px] h-[680px] rounded-[50px] border border-white/10 bg-gradient-to-b from-white/10 to-white/5 backdrop-blur-3xl overflow-hidden flex items-center justify-center">
              <div className="text-center px-8">
                <div className="text-8xl mb-6">
                  🎞️
                </div>

                <h2 className="text-3xl font-black">
                  AI Viral Shorts
                </h2>

                <p className="text-gray-300 mt-3">
                  Upload. Analyze. Clip. Download.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* GENERATED CLIPS */}
      <section className="px-6 pb-32">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-5xl font-black mb-14">
            Generated Clips
          </h2>

          {clips.length === 0 ? (
            <div className="h-[420px] rounded-[40px] border border-white/10 bg-white/5 flex flex-col items-center justify-center">
              <div className="text-8xl mb-8">
                🎬
              </div>

              <h3 className="text-4xl font-bold">
                Your clips will appear here
              </h3>

              <p className="text-gray-400 mt-5 text-lg">
                Upload video or paste YouTube link.
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
              {clips.map((clip, index) => (
                <div
                  key={index}
                  className="rounded-[35px] overflow-hidden border border-white/10 bg-white/5"
                >
                  <video
                    controls
                    className="w-full h-[600px] object-cover bg-black"
                  >
                    <source src={clip.url} type="video/mp4" />
                  </video>

                  <div className="p-6">
                    <a
                      href={clip.url}
                      target="_blank"
                      download
                      className="block w-full py-4 rounded-2xl text-center font-bold bg-gradient-to-r from-fuchsia-500 to-violet-600"
                    >
                      Download Clip
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}