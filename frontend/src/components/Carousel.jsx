import React, { useState, useEffect } from 'react';
import './Carousel.css';

const Carousel = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  
  // 轮播图数据
  const slides = [
    {
      id: 1,
      title: '热门游戏讨论区',
      description: '英雄联盟、王者荣耀、原神等热门游戏专区',
      image: 'https://via.placeholder.com/800x400/667eea/ffffff?text=游戏专区',
      link: '/tiebas/games'
    },
    {
      id: 2,
      title: '学习交流社区',
      description: '考研、编程、外语学习等知识分享平台',
      image: 'https://via.placeholder.com/800x400/764ba2/ffffff?text=学习社区',
      link: '/tiebas/study'
    },
    {
      id: 3,
      title: '生活娱乐天地',
      description: '美食、旅游、健身等生活话题讨论',
      image: 'https://via.placeholder.com/800x400/f093fb/ffffff?text=生活娱乐',
      link: '/tiebas/life'
    },
    {
      id: 4,
      title: '技术交流论坛',
      description: '编程、AI、区块链等技术前沿讨论',
      image: 'https://via.placeholder.com/800x400/4facfe/ffffff?text=技术论坛',
      link: '/tiebas/tech'
    }
  ];

  // 自动轮播
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);

    return () => clearInterval(timer);
  }, [slides.length]);

  // 手动切换
  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  const goToPrev = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  const goToNext = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  return (
    <div className="carousel">
      <div className="carousel-container">
        {slides.map((slide, index) => (
          <div
            key={slide.id}
            className={`carousel-slide ${index === currentSlide ? 'active' : ''}`}
            style={{
              backgroundImage: `url(${slide.image})`,
              transform: `translateX(${(index - currentSlide) * 100}%)`
            }}
          >
            <div className="slide-content">
              <h3 className="slide-title">{slide.title}</h3>
              <p className="slide-description">{slide.description}</p>
              <button 
                className="slide-button"
                onClick={() => console.log('跳转到:', slide.link)}
              >
                立即进入
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* 导航按钮 */}
      <button className="carousel-btn carousel-btn-prev" onClick={goToPrev}>
        ‹
      </button>
      <button className="carousel-btn carousel-btn-next" onClick={goToNext}>
        ›
      </button>

      {/* 指示器 */}
      <div className="carousel-indicators">
        {slides.map((_, index) => (
          <button
            key={index}
            className={`indicator ${index === currentSlide ? 'active' : ''}`}
            onClick={() => goToSlide(index)}
          />
        ))}
      </div>
    </div>
  );
};

export default Carousel;