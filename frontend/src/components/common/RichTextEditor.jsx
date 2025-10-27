import React, { useState, useRef, useCallback } from 'react';
import './RichTextEditor.css';

const RichTextEditor = ({ value = '', onChange, placeholder = '请输入内容...' }) => {
  const [content, setContent] = useState(value);
  const editorRef = useRef(null);
  const [isBold, setIsBold] = useState(false);
  const [isItalic, setIsItalic] = useState(false);
  const [isUnderline, setIsUnderline] = useState(false);

  // 处理内容变化
  const handleInput = useCallback((e) => {
    const newContent = e.target.innerHTML;
    setContent(newContent);
    onChange?.(newContent);
  }, [onChange]);

  // 格式化文本
  const formatText = useCallback((command, value = null) => {
    document.execCommand(command, false, value);
    editorRef.current?.focus();
    
    // 更新按钮状态
    setIsBold(document.queryCommandState('bold'));
    setIsItalic(document.queryCommandState('italic'));
    setIsUnderline(document.queryCommandState('underline'));
  }, []);

  // 插入链接
  const insertLink = useCallback(() => {
    const url = prompt('请输入链接地址:');
    if (url) {
      formatText('createLink', url);
    }
  }, [formatText]);

  // 插入图片
  const insertImage = useCallback(() => {
    const url = prompt('请输入图片地址:');
    if (url) {
      formatText('insertImage', url);
    }
  }, [formatText]);

  // 清除格式
  const clearFormat = useCallback(() => {
    formatText('removeFormat');
  }, [formatText]);

  // 工具栏按钮
  const ToolbarButton = ({ children, onClick, active = false, title }) => (
    <button
      className={`toolbar-btn ${active ? 'active' : ''}`}
      onClick={onClick}
      title={title}
      type="button"
    >
      {children}
    </button>
  );

  return (
    <div className="rich-text-editor">
      {/* 工具栏 */}
      <div className="toolbar">
        <div className="toolbar-group">
          <ToolbarButton
            onClick={() => formatText('bold')}
            active={isBold}
            title="加粗"
          >
            <span className="toolbar-icon">B</span>
          </ToolbarButton>
          
          <ToolbarButton
            onClick={() => formatText('italic')}
            active={isItalic}
            title="斜体"
          >
            <span className="toolbar-icon">I</span>
          </ToolbarButton>
          
          <ToolbarButton
            onClick={() => formatText('underline')}
            active={isUnderline}
            title="下划线"
          >
            <span className="toolbar-icon">U</span>
          </ToolbarButton>
        </div>
        
        <div className="toolbar-group">
          <ToolbarButton
            onClick={() => formatText('insertUnorderedList')}
            title="无序列表"
          >
            <span className="toolbar-icon">•</span>
          </ToolbarButton>
          
          <ToolbarButton
            onClick={() => formatText('insertOrderedList')}
            title="有序列表"
          >
            <span className="toolbar-icon">1.</span>
          </ToolbarButton>
        </div>
        
        <div className="toolbar-group">
          <ToolbarButton
            onClick={insertLink}
            title="插入链接"
          >
            <span className="toolbar-icon">🔗</span>
          </ToolbarButton>
          
          <ToolbarButton
            onClick={insertImage}
            title="插入图片"
          >
            <span className="toolbar-icon">🖼️</span>
          </ToolbarButton>
        </div>
        
        <div className="toolbar-group">
          <ToolbarButton
            onClick={clearFormat}
            title="清除格式"
          >
            <span className="toolbar-icon">🧹</span>
          </ToolbarButton>
        </div>
      </div>

      {/* 编辑器区域 */}
      <div
        ref={editorRef}
        className="editor-content"
        contentEditable
        onInput={handleInput}
        dangerouslySetInnerHTML={{ __html: content }}
        placeholder={placeholder}
        suppressContentEditableWarning={true}
      />

      {/* 字符计数 */}
      <div className="editor-footer">
        <span className="char-count">
          字符数: {content.replace(/<[^>]*>/g, '').length}
        </span>
      </div>
    </div>
  );
};

export default RichTextEditor;