import { motion } from 'framer-motion';

const styles = [
  {
    id: 'cinematic',
    name: 'Cinematic',
    description: 'Movie-like dramatic style',
    icon: '🎬',
    color: 'from-red-500 to-orange-500'
  },
  {
    id: 'animation',
    name: 'Animation',
    description: 'Animated cartoon style',
    icon: '🎨',
    color: 'from-blue-500 to-purple-500'
  },
  {
    id: 'futuristic',
    name: 'Futuristic',
    description: 'Sci-fi futuristic style',
    icon: '🚀',
    color: 'from-cyan-500 to-blue-500'
  },
  {
    id: 'documentary',
    name: 'Documentary',
    description: 'Realistic documentary style',
    icon: '📹',
    color: 'from-green-500 to-teal-500'
  },
  {
    id: 'artistic',
    name: 'Artistic',
    description: 'Creative artistic style',
    icon: '🎭',
    color: 'from-pink-500 to-rose-500'
  },
  {
    id: 'minimalist',
    name: 'Minimalist',
    description: 'Clean minimalist style',
    icon: '⚪',
    color: 'from-gray-500 to-slate-500'
  }
];

const StyleSelector = ({ selectedStyle, onStyleChange }) => {
  return (
    <div className="grid grid-cols-2 gap-3">
      {styles.map((style) => (
        <motion.button
          key={style.id}
          onClick={() => onStyleChange(style.id)}
          className={`relative p-4 rounded-xl border-2 transition-all duration-300 ${
            selectedStyle === style.id
              ? 'border-purple-500 bg-purple-500/10'
              : 'border-slate-600 hover:border-slate-500 bg-slate-800/50'
          }`}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <div className="text-center">
            <div className="text-2xl mb-2">{style.icon}</div>
                         <div className="font-semibold text-slate-200 text-sm mb-1 font-poppins">
               {style.name}
             </div>
            <div className="text-xs text-slate-400">
              {style.description}
            </div>
          </div>
          
          {selectedStyle === style.id && (
            <motion.div
              className="absolute top-2 right-2 w-4 h-4 bg-purple-500 rounded-full flex items-center justify-center"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            >
              <svg className="w-2 h-2 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </motion.div>
          )}
        </motion.button>
      ))}
    </div>
  );
};

export default StyleSelector;
