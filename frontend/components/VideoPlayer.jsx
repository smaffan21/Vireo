import { motion } from 'framer-motion';

const VideoPlayer = ({ videoUrl }) => {
  if (!videoUrl) return null;

  return (
    <motion.div
      className="relative group"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Video container with glass effect */}
      <div className="glass rounded-3xl overflow-hidden shadow-2xl">
        {/* Video element */}
        <video
          src={videoUrl}
          controls
          className="w-full h-auto max-h-96 object-cover"
          poster="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'%3E%3Crect width='16' height='9' fill='%231a1a2e'/%3E%3C/svg%3E"
        >
          Your browser does not support the video tag.
        </video>
        
        {/* Video overlay with play button */}
        <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <motion.div
            className="w-20 h-20 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center shadow-2xl"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            <svg className="w-8 h-8 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z"/>
            </svg>
          </motion.div>
        </div>
      </div>
      
      {/* Video info */}
      <motion.div
        className="mt-4 p-4 glass rounded-2xl"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-semibold text-lg gradient-text">
            Your Viral Video
          </h4>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full font-medium">
              ✓ Generated
            </span>
          </div>
        </div>
        
        <p className="text-slate-400 text-sm">
          Your AI-generated video is ready! Click play to preview and use the controls below to download or share.
        </p>
      </motion.div>
      
      {/* Video stats */}
      <motion.div
        className="grid grid-cols-3 gap-4 mt-4"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.5 }}
      >
        <div className="glass rounded-xl p-3 text-center">
          <div className="text-2xl font-bold gradient-text-accent">🎬</div>
          <div className="text-xs text-slate-400 mt-1">Video</div>
        </div>
        <div className="glass rounded-xl p-3 text-center">
          <div className="text-2xl font-bold gradient-text-secondary">🎵</div>
          <div className="text-xs text-slate-400 mt-1">Audio</div>
        </div>
        <div className="glass rounded-xl p-3 text-center">
          <div className="text-2xl font-bold gradient-text">✨</div>
          <div className="text-xs text-slate-400 mt-1">Ready</div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default VideoPlayer;


