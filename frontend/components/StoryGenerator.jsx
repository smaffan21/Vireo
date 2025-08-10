import { motion } from 'framer-motion';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000';

const StoryGenerator = ({ story }) => {
  const downloadVideo = () => {
    if (story.video_url) {
      const link = document.createElement('a');
      link.href = `${API_BASE}${story.video_url}`;
      link.download = `story_${story.story_id}.mp4`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {/* Generated Script */}
      <div className="bg-slate-800/50 rounded-xl p-6">
                 <h3 className="text-xl font-bold text-slate-200 mb-4 flex items-center font-poppins">
           <span className="text-2xl mr-3">📝</span>
           Generated Script
         </h3>
        <p className="text-slate-300 leading-relaxed">{story.script}</p>
      </div>

      {/* Scene Breakdown */}
      <div className="bg-slate-800/50 rounded-xl p-6">
                 <h3 className="text-xl font-bold text-slate-200 mb-4 flex items-center font-poppins">
           <span className="text-2xl mr-3">🎬</span>
           Scene Breakdown
         </h3>
        <div className="space-y-4">
          {story.scenes.map((scene, index) => (
            <motion.div
              key={index}
              className="bg-slate-700/50 rounded-lg p-4"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex items-start justify-between mb-2">
                                 <h4 className="font-semibold text-slate-200 font-poppins">
                   Scene {index + 1}
                 </h4>
                <span className="text-sm text-slate-400 bg-slate-600 px-2 py-1 rounded">
                  {scene.duration}s
                </span>
              </div>
              <p className="text-slate-300 text-sm mb-2">{scene.description}</p>
              <p className="text-slate-400 text-xs italic">
                "{scene.prompt}"
              </p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Final Video */}
      {story.video_url && (
        <div className="bg-slate-800/50 rounded-xl p-6">
                                     <h3 className="text-xl font-bold text-slate-200 mb-4 flex items-center font-poppins">
           <span className="text-2xl mr-3">🎥</span>
           Final Video
         </h3>
          <div className="space-y-4">
            <video
              controls
              className="w-full rounded-lg"
              src={`${API_BASE}${story.video_url}`}
            >
              Your browser does not support the video tag.
            </video>
            
            <motion.button
              onClick={downloadVideo}
              className="w-full py-3 px-6 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 rounded-lg font-semibold text-white transition-all duration-300 flex items-center justify-center"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Download Video
            </motion.button>
          </div>
        </div>
      )}

      {/* Status */}
      <div className="bg-slate-800/50 rounded-xl p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-3 animate-pulse"></div>
            <span className="text-slate-200 font-semibold">
              {story.status === 'completed' ? 'Generation Complete' : 'Processing...'}
            </span>
          </div>
          <span className="text-sm text-slate-400">
            ID: {story.story_id.slice(0, 8)}
          </span>
        </div>
      </div>
    </motion.div>
  );
};

export default StoryGenerator;
