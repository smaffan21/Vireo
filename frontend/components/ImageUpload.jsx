import { useState, useRef } from 'react';
import { motion } from 'framer-motion';

const ImageUpload = ({ images, setImages, maxImages = 2 }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (files) => {
    const newImages = Array.from(files).slice(0, maxImages - images.length);
    
    const imagePromises = newImages.map(file => {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          resolve({
            file,
            preview: e.target.result,
            name: file.name
          });
        };
        reader.readAsDataURL(file);
      });
    });

    Promise.all(imagePromises).then(newImageData => {
      setImages([...images, ...newImageData]);
    });
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    handleFileSelect(files);
  };

  const removeImage = (index) => {
    const newImages = images.filter((_, i) => i !== index);
    setImages(newImages);
  };

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <motion.div
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
          isDragOver 
            ? 'border-purple-500 bg-purple-500/10' 
            : 'border-slate-600 hover:border-slate-500'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <div className="text-6xl mb-4">📸</div>
                 <p className="text-lg font-semibold text-slate-200 mb-2 font-poppins">
           {isDragOver ? 'Drop images here' : 'Drag & drop images here'}
         </p>
        <p className="text-slate-400 mb-4">
          or click to select files (max {maxImages} images)
        </p>
        <button
          onClick={() => fileInputRef.current?.click()}
          className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold text-white transition-colors"
        >
          Choose Files
        </button>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept="image/*"
          onChange={(e) => handleFileSelect(e.target.files)}
          className="hidden"
        />
      </motion.div>

      {/* Image Previews */}
      {images.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {images.map((image, index) => (
            <motion.div
              key={index}
              className="relative group"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
            >
              <img
                src={image.preview}
                alt={image.name}
                className="w-full h-32 object-cover rounded-lg"
              />
              <button
                onClick={() => removeImage(index)}
                className="absolute top-2 right-2 w-8 h-8 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center text-white font-bold opacity-0 group-hover:opacity-100 transition-opacity"
              >
                ×
              </button>
              <p className="text-sm text-slate-400 mt-2 truncate">{image.name}</p>
            </motion.div>
          ))}
        </div>
      )}

      {/* Upload Progress */}
      {images.length > 0 && (
        <div className="text-sm text-slate-400">
          {images.length} of {maxImages} images selected
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
