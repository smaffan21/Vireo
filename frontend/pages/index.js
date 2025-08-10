import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import Image from 'next/image';
import ImageUpload from '@/components/ImageUpload';
import StyleSelector from '@/components/StyleSelector';
import StoryGenerator from '@/components/StoryGenerator';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000';

export default function Home() {
  const [images, setImages] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('cinematic');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedStory, setGeneratedStory] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim() || images.length === 0) {
      alert('Please provide a prompt and upload at least one image');
      return;
    }

    setIsGenerating(true);
    
    try {
      const formData = new FormData();
      formData.append('prompt', prompt);
      formData.append('style', selectedStyle);
      
      images.forEach((image, index) => {
        formData.append('images', image.file);
      });

      const response = await fetch(`${API_BASE}/generate-story`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setGeneratedStory(result);
      } else {
        const error = await response.text();
        alert(`Error generating story: ${error}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate story. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

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
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Particle Background */}
      <div className="particles">
        {Array.from({ length: 50 }, (_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 30}s`,
              animationDuration: `${20 + Math.random() * 15}s`
            }}
          />
        ))}
      </div>
      
      {/* Hero Section */}
      <div className="relative z-10">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="text-center pt-20 pb-16 px-4"
        >
                     <motion.div 
             className="flex justify-center mb-6"
             initial={{ scale: 0.8 }}
             animate={{ scale: 1 }}
             transition={{ duration: 0.8, ease: "easeOut" }}
           >
             <div className="logo-title-container">
               <Image
                 src="/vireo-logo.png"
                 alt="Vireo Logo"
                 width={200}
                 height={80}
                 className="vireo-logo"
                 priority
                 onError={(e) => {
                   // Fallback to text if image fails to load
                   e.target.style.display = 'none';
                 }}
               />
                               <h1 className="text-5xl md:text-7xl font-black gradient-text animate-gradient font-inter tracking-wider">
                  IREO
                </h1>
             </div>
           </motion.div>
          <motion.p 
            className="text-xl md:text-2xl text-slate-300 mb-8 max-w-3xl mx-auto leading-relaxed"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            Transform your images into captivating video stories with AI-powered generation
          </motion.p>
          
          
        </motion.div>
      </div>

      {/* Main Content */}
      <motion.div 
        className="max-w-6xl mx-auto px-4 pb-20"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div 
          className="glass rounded-3xl p-8 mb-8"
          variants={itemVariants}
        >
                     <h2 className="text-3xl font-bold mb-6 gradient-text-secondary text-center font-poppins">
             Create Your Story
           </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Column - Input */}
            <div className="space-y-6">
              <div>
                <label className="block text-lg font-semibold mb-3 text-slate-200 font-poppins">
                  Upload Images (1-2 images)
                </label>
                <ImageUpload 
                  images={images} 
                  setImages={setImages} 
                  maxImages={2}
                />
              </div>
              
              <div>
                <label className="block text-lg font-semibold mb-3 text-slate-200 font-poppins">
                  What should the video be about?
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe the story you want to create... (e.g., 'A magical journey through a mystical forest')"
                  className="w-full h-32 p-4 rounded-xl bg-slate-800 border border-slate-600 text-slate-200 placeholder-slate-400 focus:border-purple-500 focus:outline-none resize-none"
                />
              </div>
              
              <div>
                <label className="block text-lg font-semibold mb-3 text-slate-200 font-poppins">
                  Video Style
                </label>
                <StyleSelector 
                  selectedStyle={selectedStyle} 
                  onStyleChange={setSelectedStyle} 
                />
              </div>
              
              <motion.button
                onClick={handleGenerate}
                disabled={isGenerating || !prompt.trim() || images.length === 0}
                className="w-full py-4 px-8 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl font-bold text-white text-lg transition-all duration-300 transform hover:scale-105"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {isGenerating ? (
                  <div className="flex items-center justify-center">
                    <div className="spinner mr-3"></div>
                    Generating Story...
                  </div>
                ) : (
                  'Generate Story Video'
                )}
              </motion.button>
            </div>
            
            {/* Right Column - Preview/Results */}
            <div className="space-y-6">
              {generatedStory ? (
                <StoryGenerator story={generatedStory} />
              ) : (
                <div className="h-full flex items-center justify-center">
                  <div className="text-center text-slate-400">
                    <div className="text-6xl mb-4">🎬</div>
                    <p className="text-lg">Your generated story will appear here</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </motion.div>

             {/* Footer */}
       <motion.footer
         className="relative z-10 mt-20 pb-8"
         initial={{ opacity: 0, y: 20 }}
         animate={{ opacity: 1, y: 0 }}
         transition={{ delay: 1.2, duration: 0.8 }}
       >
         <div className="max-w-6xl mx-auto px-4">
           <div className="glass rounded-2xl p-6 text-center">
             <div className="flex flex-col items-center space-y-2">
               <p className="text-slate-300 text-sm font-inter">
                 Developed for{' '}
                 <span className="gradient-text font-semibold">Hack-Nation's 2nd Global AI Hackathon</span>
               </p>
               <div className="flex items-center space-x-2">
                 <span className="text-slate-400 text-xs">Track:</span>
                 <span className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
                   #12) Viral Video Maker
                 </span>
               </div>
             </div>
           </div>
         </div>
       </motion.footer>

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


