<template>
  <div class="tieba-detail">
    <!-- 贴吧头部信息区 -->
    <TiebaHeader 
      :tieba="currentTieba"
      @follow="handleFollow"
      @join="handleJoin"
    />
    
    <!-- 操作按钮栏 -->
    <ActionBar 
      @create-post="handleCreatePost"
      @search="handleSearch"
      :is-followed="isFollowed"
      :is-member="isMember"
    />
    
    <!-- 帖子列表表格 -->
    <PostTable 
      :posts="posts"
      :loading="loading"
      @post-click="handlePostClick"
    />
    
    <!-- 分页组件 -->
    <Pagination 
      :current-page="currentPage"
      :total-pages="totalPages"
      :total-items="totalItems"
      @page-change="handlePageChange"
    />
    
    <!-- 发帖模态框 -->
    <div v-if="showPostModal" class="post-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>发布新帖子</h3>
          <button class="close-btn" @click="showPostModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="post-title">帖子标题</label>
            <input 
              id="post-title"
              v-model="newPost.title"
              type="text"
              placeholder="请输入帖子标题"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="post-content">帖子内容</label>
            <RichTextEditor 
              v-model="newPost.content"
              placeholder="请输入帖子内容..."
            />
          </div>
          <div class="form-group">
            <label>帖子标签</label>
            <div class="tags-container">
              <button 
                v-for="tag in availableTags" 
                :key="tag"
                :class="['tag-btn', { active: newPost.tags.includes(tag) }]"
                @click="toggleTag(tag)"
              >
                {{ tag }}
              </button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showPostModal = false">取消</button>
          <button class="btn btn-primary" @click="submitPost" :disabled="!newPost.title || !newPost.content">
            发布帖子
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import TiebaHeader from '@/components/tieba/TiebaHeader.vue'
import ActionBar from '@/components/tieba/ActionBar.vue'
import PostTable from '@/components/tieba/PostTable.vue'
import Pagination from '@/components/common/Pagination.vue'
import RichTextEditor from '@/components/common/RichTextEditor.jsx'

// 路由参数
const route = useRoute()
const tiebaId = route.params.id

// 响应式数据
const currentTieba = ref({})
const posts = ref([])
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const isFollowed = ref(false)
const isMember = ref(false)
const showPostModal = ref(false)

// 新帖子数据
const newPost = reactive({
  title: '',
  content: '',
  tags: []
})

// 可用标签
const availableTags = ['攻略', '讨论', '求助', '分享', '图片', '视频', '精华']

// 计算属性
const pageSize = 10

// 模拟贴吧数据
const mockTiebaData = {
  id: tiebaId,
  name: '游戏吧',
  avatar: '游戏',
  description: '欢迎来到游戏吧!这里是游戏爱好者的聚集地,分享游戏心得、攻略、资讯的好地方。',
  stats: {
    members: 1230000,
    posts: 56000,
    heat: 9.8
  }
}

// 模拟帖子数据
const mockPosts = [
  {
    id: 1,
    title: '【攻略】新手上路必看的游戏技巧',
    author: { name: '张三', avatar: '张' },
    replies: 234,
    lastReplyTime: '2024-01-15 14:30',
    tags: ['精华', '攻略']
  },
  {
    id: 2,
    title: '【讨论】这款游戏的剧情你怎么看?',
    author: { name: '李四', avatar: '李' },
    replies: 156,
    lastReplyTime: '2024-01-15 13:45',
    tags: ['讨论']
  },
  {
    id: 3,
    title: '【求助】BOSS战打不过,求攻略',
    author: { name: '王五', avatar: '王' },
    replies: 89,
    lastReplyTime: '2024-01-15 12:20',
    tags: ['求助']
  },
  {
    id: 4,
    title: '【分享】我的游戏截图合集',
    author: { name: '赵六', avatar: '赵' },
    replies: 67,
    lastReplyTime: '2024-01-15 11:15',
    tags: ['分享', '图片']
  }
]

// 生命周期
onMounted(() => {
  loadTiebaData()
  loadPosts()
})

// 方法
const loadTiebaData = async () => {
  // 模拟API调用
  currentTieba.value = mockTiebaData
}

const loadPosts = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    posts.value = mockPosts
    totalItems.value = 156
    totalPages.value = Math.ceil(totalItems.value / pageSize)
  } catch (error) {
    console.error('加载帖子失败:', error)
  } finally {
    loading.value = false
  }
}

const handleFollow = async () => {
  isFollowed.value = !isFollowed.value
  // 模拟API调用
  console.log(isFollowed.value ? '关注贴吧' : '取消关注')
}

const handleJoin = async () => {
  isMember.value = !isMember.value
  // 模拟API调用
  console.log(isMember.value ? '加入会员' : '退出会员')
}

const handleCreatePost = () => {
  showPostModal.value = true
}

const handleSearch = (keyword) => {
  console.log('搜索关键词:', keyword)
  // 实现搜索逻辑
}

const handlePostClick = (post) => {
  console.log('点击帖子:', post)
  // 跳转到帖子详情页
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadPosts()
}

const toggleTag = (tag) => {
  const index = newPost.tags.indexOf(tag)
  if (index > -1) {
    newPost.tags.splice(index, 1)
  } else {
    newPost.tags.push(tag)
  }
}

const submitPost = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('发布帖子:', newPost)
    showPostModal.value = false
    // 重置表单
    Object.assign(newPost, {
      title: '',
      content: '',
      tags: []
    })
    // 重新加载帖子列表
    loadPosts()
  } catch (error) {
    console.error('发布帖子失败:', error)
  }
}
</script>

<style scoped>
.tieba-detail {
  min-height: 100vh;
  background: #f5f5f5;
}

.post-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 5px;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #007AFF;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
}

.tag-btn.active {
  background: #007AFF;
  color: white;
  border-color: #007AFF;
}

.tag-btn:hover {
  border-color: #007AFF;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-primary {
  background: #007AFF;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056CC;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 20px;
  }
  
  .tags-container {
    justify-content: center;
  }
}
</style>