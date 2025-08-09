import { motion } from 'framer-motion';

const TrendCard = ({ trend, onClick, index }) => {
  const gradients = [
    'from-purple-500 via-pink-500 to-red-500',
    'from-blue-500 via-cyan-500 to-teal-500',
    'from-green-500 via-emerald-500 to-teal-500',
    'from-orange-500 via-red-500 to-pink-500',
    'from-indigo-500 via-purple-500 to-pink-500',
    'from-yellow-500 via-orange-500 to-red-500'
  ];

  const icons = ['🎭', '🚀', '💡', '🔥', '⭐', '🎪'];
  
  return (
    <motion.div
      className="group cursor-pointer"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      whileHover={{ y: -5 }}
      whileTap={{ scale: 0.98 }}
    >
      <div 
        className="glass-dark rounded-3xl p-8 h-full relative overflow-hidden group-hover:shadow-2xl transition-all duration-500"
        onClick={onClick}
      >
        {/* Background gradient overlay */}
        <div className={`absolute inset-0 bg-gradient-to-br ${gradients[index % gradients.length]} opacity-0 group-hover:opacity-10 transition-opacity duration-500`} />
        
        {/* Icon */}
        <div className="text-6xl mb-6 text-center group-hover:scale-110 transition-transform duration-300">
          {icons[index % icons.length]}
        </div>
        
        {/* Title */}
        <h3 className="text-2xl font-bold mb-4 text-center group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-purple-400 transition-all duration-300">
          {trend.title}
        </h3>
        
        {/* Description */}
        <p className="text-slate-300 text-center mb-6 leading-relaxed group-hover:text-slate-200 transition-colors duration-300">
          {trend.description}
        </p>
        
        {/* Template preview */}
        <div className="glass rounded-2xl p-4 mb-6 text-center">
          <p className="text-sm text-slate-400 mb-2">Template:</p>
          <p className="font-mono text-sm bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            {trend.template}
          </p>
        </div>
        
        {/* CTA Button */}
        <div className="text-center">
          <motion.button
            className="btn-primary w-full group-hover:shadow-lg group-hover:shadow-blue-500/25"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <span className="flex items-center justify-center">
              Create Video
              <svg className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
          </motion.button>
        </div>
        
        {/* Hover effect overlay */}
        <div className="absolute inset-0 rounded-3xl border border-transparent group-hover:border-blue-400/30 transition-all duration-500" />
        
        {/* Shimmer effect on hover */}
        <div className="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500">
          <div className="shimmer absolute inset-0 rounded-3xl" />
        </div>
      </div>
    </motion.div>
  );
};

export default TrendCard;


