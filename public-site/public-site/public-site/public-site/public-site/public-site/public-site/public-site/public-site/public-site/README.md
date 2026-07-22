# Enemy Path Site

iOS 风格的关卡路径可视化与编辑工具（纯前端单页应用）。  
支持查看关卡路径图、在画布上编辑路径节点、管理多条龙路径，并导出 JSON / Excel / PNG。

## 主要功能

- 路径总览：按关卡浏览路径图，支持搜索和筛选
- 可视化编辑：画笔新增节点、拖拽节点、框选移动、缩放/平移画布
- 图层管理：每关最多 5 条路径（龙1~龙5）
- 路径参数：编辑龙属性、血量数组、宝箱分布等
- 数据导出：
  - 导出当前编辑数据为 `JSON`
  - 导出当前关卡画布为 `PNG`
  - 导出结构化 `Excel`（`.xlsx`）
- 本地保存：编辑内容可保存到浏览器本地存储

## 快速开始

### 方式 1：直接本地打开

1. 下载仓库
2. 双击打开 `index.html`

### 方式 2：本地静态服务器（推荐）

```bash
cd enemy-path-site
python3 -m http.server 8080
```

打开：`http://localhost:8080`

## 使用流程（编辑模式）

1. 切换到 **编辑器**
2. 选择关卡或新建关卡
3. 在画布绘制/调整路径节点
4. 配置路径属性（如龙参数、宝箱点）
5. 点击 **保存修改**（本地存储）
6. 通过顶部按钮导出：
   - **导出 JSON**
   - **导出 Excel**
   - **导出当前 PNG**

## 数据与导出说明

- 页面内置了初始关卡数据（`seedLevels`）
- 本地编辑缓存使用浏览器 `localStorage`
- JSON 导出文件名：`enemy_path_edits.json`
- Excel 导出文件名：`关卡数据_编辑器导出_YYYY-MM-DD.xlsx`

## 技术栈

- HTML5
- CSS3
- Vanilla JavaScript
- Canvas 2D API
- ExcelJS（浏览器端生成 `.xlsx`）

## 目录结构

```text
enemy-path-site/
├── index.html        # 主页面（UI + 逻辑）
├── assets/           # 关卡图片等静态资源
├── .nojekyll
└── README.md
```

## 适用场景

- 关卡策划路径调试
- 敌人移动路径标注与校验
- 版本间路径差异比对与导出

---

If you need a split version (`data.json` + modular JS files), this repo can be refactored into maintainable modules quickly.
