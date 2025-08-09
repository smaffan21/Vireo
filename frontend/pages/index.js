import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { motion } from 'framer-motion';
import TrendCard from '@/components/TrendCard';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000';

// Particle background component
const ParticleBackground = () => {
  const particles = Array.from({ length: 50 }, (_, i) => i);
  
  return (
    <div className="particles">
      {particles.map((i) => (
        <div
          key={i}
          className="particle"
          style={{
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 20}s`,
            animationDuration: `${15 + Math.random() * 10}s`
          }}
        />
      ))}
    </div>
  );
};

export default function Home() {
  const router = useRouter();
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/trends`)
      .then(res => res.json())
      .then(data => setTrends(data.trends || []))
      .catch(() => setTrends([]))
      .finally(() => setLoading(false));
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
        ease: "easeOut"
      }
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      <ParticleBackground />
      
      {/* Hero Section */}
      <div className="relative z-10">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="text-center pt-20 pb-16 px-4"
        >
          <motion.h1 
            className="text-6xl md:text-8xl font-black mb-6 gradient-text animate-gradient"
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            VIREO
          </motion.h1>
          <motion.p 
            className="text-xl md:text-2xl text-slate-300 mb-8 max-w-3xl mx-auto leading-relaxed"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            Transform your ideas into viral videos in seconds with AI-powered trend generation
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <div className="glass px-8 py-4 rounded-2xl">
              <span className="text-2xl font-bold gradient-text-accent">⚡</span>
              <span className="ml-3 text-lg font-semibold">Instant Generation</span>
            </div>
            <div className="glass px-8 py-4 rounded-2xl">
              <span className="text-2xl font-bold gradient-text-secondary">🎯</span>
              <span className="ml-3 text-lg font-semibold">Trending Formats</span>
            </div>
            <div className="glass px-8 py-4 rounded-2xl">
              <span className="text-2xl font-bold gradient-text">🚀</span>
              <span className="ml-3 text-lg font-semibold">Viral Ready</span>
            </div>
          </motion.div>
        </motion.div>
      </div>

      {/* Trends Section */}
      <motion.div 
        className="max-w-7xl mx-auto px-4 pb-20"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div 
          className="text-center mb-16"
          variants={itemVariants}
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4 gradient-text-secondary">
            Choose Your Trend
          </h2>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Pick from our curated collection of viral video formats and watch your content go viral
          </p>
        </motion.div>

        {loading ? (
          <motion.div 
            className="flex justify-center items-center py-20"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="text-center">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-xl text-slate-300">Loading trending formats...</p>
            </div>
          </motion.div>
        ) : (
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
            variants={containerVariants}
          >
            {trends.map((trend, index) => (
              <motion.div
                key={trend.id}
                variants={itemVariants}
                whileHover={{ scale: 1.05, y: -10 }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <TrendCard 
                  trend={trend} 
                  onClick={() => router.push(`/trend/${trend.id}`)}
                  index={index}
                />
              </motion.div>
            ))}
          </motion.div>
        )}
      </motion.div>

      {/* Floating Action Button */}
      <motion.div
        className="fixed bottom-8 right-8 z-20"
        initial={{ opacity: 0, scale: 0 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 1, duration: 0.5 }}
      >
        <button 
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          className="glass p-4 rounded-full shadow-2xl hover:shadow-3xl transition-all duration-300 hover:scale-110"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
          </svg>
        </button>
      </motion.div>
    </div>
  );
}


