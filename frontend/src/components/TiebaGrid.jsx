import React, { useState } from 'react';
import './TiebaGrid.css';

const TiebaGrid = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  // 模拟热门贴吧数据
  const tiebas = [
    {
      id: 1,
      name: '英雄联盟',
      members: '2.3万',
      posts: '15.6万',
      description: 'LOL游戏讨论、攻略分享',
      avatar: 'https://via.placeholder.com/60x60/667eea/ffffff?text=LOL',
      category: '游戏',
      isHot: true
    },
    {
      id: 2,
      name: '考研',
      members: '8.9万',
      posts: '45.2万',
      description: '考研经验分享、资料交流',
      avatar: 'https://via.placeholder.com/60x60/764ba2/ffffff?text=考研',
      category: '学习',
      isHot: true
    },
    {
      id: 3,
      name: '美食',
      members: '5.6万',
      posts: '32.1万',
      description: '各地美食推荐、烹饪技巧',
      avatar: 'https://via.placeholder.com/60x60/f093fb/ffffff?text=美食',
      category: '生活',
      isHot: false
    },
    {
      id: 4,
      name: '编程',
      members: '4.2万',
      posts: '28.7万',
      description: '编程技术交流、项目分享',
      avatar: 'https://via.placeholder.com/60x60/4facfe/ffffff?text=编程',
      category: '技术',
      isHot: true
    },
    {
      id: 5,
      name: '健身',
      members: '3.1万',
      posts: '18.9万',
      description: '健身计划、营养指导',
      avatar: 'https://via.placeholder.com/60x60/43e97b/ffffff?text=健身',
      category: '健康',
      isHot: false
    },
    {
      id: 6,
      name: '旅游',
      members: '6.8万',
      posts: '39.4万',
      description: '旅游攻略、景点推荐',
      avatar: 'https://via.placeholder.com/60x60/f5576c/ffffff?text=旅游',
      category: '生活',
      isHot: true
    },
    {
      id: 7,
      name: '摄影',
      members: '2.9万',
      posts: '16.3万',
      description: '摄影技巧、作品分享',
      avatar: 'https://via.placeholder.com/60x60/ffd89b/ffffff?text=摄影',
      category: '艺术',
      isHot: false
    },
    {
      id: 8,
      name: '电影',
      members: '7.5万',
      posts: '42.8万',
      description: '电影推荐、影评交流',
      avatar: 'https://via.placeholder.com/60x60/96e6a1/ffffff?text=电影',
      category: '娱乐',
      isHot: true
    }
  ];

  // 过滤贴吧
  const filteredTiebas = tiebas.filter(tieba =>
    tieba.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    tieba.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
    tieba.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // 处理搜索
  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  // 处理贴吧点击
  const handleTiebaClick = (tieba) => {
    console.log('进入贴吧:', tieba.name);
    // 这里可以添加路由跳转逻辑
  };

  return (
    <div className="tieba-grid">
      <div className="tieba-header">
        <h2 className="section-title">热门贴吧</h2>
        <div className="search-container">
          <input
            type="text"
            placeholder="搜索贴吧..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
          <button className="search-btn">🔍</button>
        </div>
      </div>

      <div className="tieba-container">
        {filteredTiebas.length > 0 ? (
          <div className="grid">
            {filteredTiebas.map((tieba) => (
              <div
                key={tieba.id}
                className={`tieba-card ${tieba.isHot ? 'hot' : ''}`}
                onClick={() => handleTiebaClick(tieba)}
              >
                <div className="tieba-header">
                  <img src={tieba.avatar} alt={tieba.name} className="tieba-avatar" />
                  <div className="tieba-info">
                    <h3 className="tieba-name">{tieba.name}</h3>
                    <span className="tieba-category">{tieba.category}</span>
                  </div>
                  {tieba.isHot && <span className="hot-badge">🔥 热门</span>}
                </div>
                
                <p className="tieba-description">{tieba.description}</p>
                
                <div className="tieba-stats">
                  <div className="stat">
                    <span className="stat-label">成员</span>
                    <span className="stat-value">{tieba.members}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">帖子</span>
                    <span className="stat-value">{tieba.posts}</span>
                  </div>
                </div>
                
                <button className="join-btn">
                  加入贴吧
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-results">
            <p>没有找到相关的贴吧</p>
          </div>
        )}
      </div>

      <div className="tieba-footer">
        <button className="view-all-btn">
          查看全部贴吧
        </button>
      </div>
    </div>
  );
};

export default TiebaGrid;