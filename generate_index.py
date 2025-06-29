import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# 配置参数
ROOT_DIR = "docs"  # 站点根目录
IGNORE_PREFIXES = (".", "_")  # 忽略以这些字符开头的文件/目录
SORT_OPTIONS = ["name", "modified", "size", "type"]  # 排序选项
ICON_MAP = {
    "directory": "fas fa-folder",
    "default": "fas fa-file",
    # 按扩展名映射的图标
    ".zip": "fas fa-file-archive",
    ".gz": "fas fa-file-archive",
    ".tar": "fas fa-file-archive",
    ".7z": "fas fa-file-archive",
    ".mp3": "fas fa-file-audio",
    ".wav": "fas fa-file-audio",
    ".mp4": "fas fa-file-video",
    ".avi": "fas fa-file-video",
    ".mov": "fas fa-file-video",
    ".jpg": "fas fa-file-image",
    ".png": "fas fa-file-image",
    ".gif": "fas fa-file-image",
    ".svg": "fas fa-file-image",
    ".pdf": "fas fa-file-pdf",
    ".py": "fab fa-python",
    ".js": "fab fa-js",
    ".html": "fab fa-html5",
    ".css": "fab fa-css3",
    ".txt": "fas fa-file-alt",
    ".md": "fas fa-file-alt",
    ".json": "fas fa-file-code",
    ".xml": "fas fa-file-code",
    ".yaml": "fas fa-file-code",
    ".yml": "fas fa-file-code",
}

def get_icon_class(file_path):
    """获取文件对应的图标类"""
    if file_path.is_dir():
        return ICON_MAP["directory"]
    
    ext = file_path.suffix.lower()
    return ICON_MAP.get(ext, ICON_MAP["default"])

def human_readable_size(size):
    """将字节大小转换为易读格式"""
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while size >= 1024 and unit_index < len(units)-1:
        unit_index += 1
        size /= 1024.0
    return f"{size:.1f} {units[unit_index]}"

def generate_directory_index(directory):
    """为指定目录生成index.html"""
    # 收集目录内容
    contents = []
    for item in directory.iterdir():
        if item.name.startswith(IGNORE_PREFIXES) or item.name == "index.html":
            continue
            
        is_dir = item.is_dir()
        stat = item.stat()
        contents.append({
            "name": item.name,
            "path": f"./{item.name}" + ("/" if is_dir else ""),
            "is_dir": is_dir,
            "size": stat.st_size if not is_dir else 0,
            "size_human": "" if is_dir else human_readable_size(stat.st_size),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            "modified_ts": stat.st_mtime,
            "icon": get_icon_class(item),
            "type": "directory" if is_dir else "file"
        })
    
    # 当前路径面包屑导航
    breadcrumbs = []
    path_parts = directory.relative_to(ROOT_DIR).parts
    for i in range(len(path_parts)):
        path = "/".join(path_parts[:i+1])
        breadcrumbs.append({
            "name": path_parts[i],
            "path": f"/{path}/" if i < len(path_parts)-1 else None
        })
    
    # 生成HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>斯迪克镜像站 - {directory.relative_to(ROOT_DIR)}</title>
        <link rel="stylesheet" href="/_assets/style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script>
            // 页面初始化时加载的数据
            const directoryData = {{
                path: "{directory.relative_to(ROOT_DIR)}",
                items: {json.dumps(contents, ensure_ascii=False)},
                sortField: localStorage.getItem('sortField') || 'name',
                sortOrder: localStorage.getItem('sortOrder') || 'asc'
            }};
        </script>
    </head>
    <body>
        <header>
            <h1>斯迪克镜像站</h1>
            <div class="breadcrumbs">
                <a href="/">首页</a>
                {' / '.join(f'<a href="/{bc["path"]}">{bc["name"]}</a>' for bc in breadcrumbs if bc["path"])}
                {breadcrumbs[-1]["name"] if breadcrumbs else ''}
            </div>
        </header>
        
        <main>
            <div class="controls">
                <div class="sorting">
                    <label>排序方式:</label>
                    <select id="sortField">
                        <option value="name">名称</option>
                        <option value="modified">修改日期</option>
                        <option value="size">大小</option>
                        <option value="type">类型</option>
                    </select>
                    <select id="sortOrder">
                        <option value="asc">升序</option>
                        <option value="desc">降序</option>
                    </select>
                </div>
                <div class="search">
                    <input type="text" id="searchInput" placeholder="搜索文件...">
                </div>
            </div>
            
            <table id="fileTable">
                <thead>
                    <tr>
                        <th>名称</th>
                        <th>修改日期</th>
                        <th>大小</th>
                        <th>类型</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- 内容由JavaScript动态生成 -->
                </tbody>
            </table>
        </main>
        
        <footer>
            <p>Pseudo Mirror Station of Sdick &copy; {datetime.now().year}</p>
        </footer>
        
        <script src="/_assets/script.js"></script>
    </body>
    </html>
    """
    
    # 写入文件
    index_path = directory / "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

def setup_assets():
    """创建资源目录和文件"""
    assets_dir = Path(ROOT_DIR) / "_assets"
    assets_dir.mkdir(exist_ok=True)
    
    # 创建CSS文件
    css = """
    :root {
        --primary-color: #3498db;
        --secondary-color: #2980b9;
        --background: #f8f9fa;
        --card-bg: #ffffff;
        --text-color: #333333;
        --border-color: #e0e0e0;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: var(--text-color);
        background-color: var(--background);
        margin: 0;
        padding: 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    header {
        background-color: var(--primary-color);
        color: white;
        padding: 20px;
        border-radius: 8px 8px 0 0;
        margin-bottom: 20px;
    }
    
    header h1 {
        margin: 0;
        font-size: 2rem;
    }
    
    .breadcrumbs {
        padding: 10px 0;
        font-size: 0.9rem;
    }
    
    .breadcrumbs a {
        color: #e0f7ff;
        text-decoration: none;
    }
    
    .breadcrumbs a:hover {
        text-decoration: underline;
    }
    
    .controls {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        flex-wrap: wrap;
        gap: 15px;
    }
    
    .sorting, .search {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    select, input {
        padding: 8px 12px;
        border: 1px solid var(--border-color);
        border-radius: 4px;
        font-size: 1rem;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        background-color: var(--card-bg);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-radius: 8px;
        overflow: hidden;
    }
    
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }
    
    th {
        background-color: #f1f1f1;
        font-weight: 600;
        cursor: pointer;
    }
    
    th:hover {
        background-color: #e9e9e9;
    }
    
    tr:last-child td {
        border-bottom: none;
    }
    
    tr:hover {
        background-color: #f9f9f9;
    }
    
    .file-icon {
        margin-right: 10px;
        width: 20px;
        text-align: center;
        color: var(--primary-color);
    }
    
    footer {
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        color: #777;
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        .controls {
            flex-direction: column;
        }
        
        th, td {
            padding: 8px 10px;
        }
    }
    """
    with open(assets_dir / "style.css", "w") as f:
        f.write(css)
    
    # 创建JavaScript文件
    js = """
    document.addEventListener('DOMContentLoaded', () => {
        // 获取DOM元素
        const fileTable = document.getElementById('fileTable');
        const tbody = fileTable.querySelector('tbody');
        const sortField = document.getElementById('sortField');
        const sortOrder = document.getElementById('sortOrder');
        const searchInput = document.getElementById('searchInput');
        
        // 初始化排序选项
        sortField.value = directoryData.sortField;
        sortOrder.value = directoryData.sortOrder;
        
        // 渲染表格函数
        function renderTable(items) {
            tbody.innerHTML = '';
            
            // 添加父目录链接（如果不是根目录）
            if (directoryData.path) {
                const parentRow = document.createElement('tr');
                parentRow.innerHTML = `
                    <td>
                        <i class="fas fa-level-up-alt file-icon"></i>
                        <a href="../">返回上级目录</a>
                    </td>
                    <td></td>
                    <td></td>
                    <td>上级目录</td>
                `;
                tbody.appendChild(parentRow);
            }
            
            // 添加文件和目录项
            items.forEach(item => {
                const row = document.createElement('tr');
                
                const icon = item.is_dir 
                    ? '<i class="fas fa-folder file-icon"></i>' 
                    : `<i class="${item.icon} file-icon"></i>`;
                
                const nameLink = item.is_dir 
                    ? `<a href="${item.path}">${item.name}/</a>` 
                    : `<a href="${item.path}">${item.name}</a>`;
                
                row.innerHTML = `
                    <td>${icon} ${nameLink}</td>
                    <td>${item.modified}</td>
                    <td>${item.size_human}</td>
                    <td>${item.type}</td>
                `;
                tbody.appendChild(row);
            });
        }
        
        // 排序函数
        function sortItems() {
            const field = sortField.value;
            const order = sortOrder.value;
            
            // 保存排序设置
            localStorage.setItem('sortField', field);
            localStorage.setItem('sortOrder', order);
            
            // 排序逻辑
            const sortedItems = [...directoryData.items].sort((a, b) => {
                let valueA, valueB;
                
                switch(field) {
                    case 'name':
                        valueA = a.name.toLowerCase();
                        valueB = b.name.toLowerCase();
                        break;
                    case 'modified':
                        valueA = a.modified_ts;
                        valueB = b.modified_ts;
                        break;
                    case 'size':
                        valueA = a.size;
                        valueB = b.size;
                        break;
                    case 'type':
                        valueA = a.type;
                        valueB = b.type;
                        break;
                    default:
                        valueA = a.name.toLowerCase();
                        valueB = b.name.toLowerCase();
                }
                
                if (valueA < valueB) return order === 'asc' ? -1 : 1;
                if (valueA > valueB) return order === 'asc' ? 1 : -1;
                return 0;
            });
            
            renderTable(sortedItems);
        }
        
        // 搜索函数
        function searchItems() {
            const query = searchInput.value.toLowerCase();
            
            if (!query) {
                sortItems();
                return;
            }
            
            const filteredItems = directoryData.items.filter(item => 
                item.name.toLowerCase().includes(query) ||
                item.type.toLowerCase().includes(query)
            );
            
            renderTable(filteredItems);
        }
        
        // 初始化事件监听
        sortField.addEventListener('change', sortItems);
        sortOrder.addEventListener('change', sortItems);
        searchInput.addEventListener('input', searchItems);
        
        // 初始渲染
        sortItems();
    });
    """
    with open(assets_dir / "script.js", "w") as f:
        f.write(js)

def main():
    # 确保根目录存在
    root_path = Path(ROOT_DIR)
    if not root_path.exists():
        root_path.mkdir()
        print(f"创建根目录: {ROOT_DIR}")
    
    # 设置资源文件
    setup_assets()
    
    # 遍历所有目录并生成索引
    count = 0
    for dirpath, dirnames, filenames in os.walk(root_path):
        # 跳过资源目录
        if "_assets" in dirpath.split(os.sep):
            continue
            
        directory = Path(dirpath)
        generate_directory_index(directory)
        count += 1
        print(f"生成索引: {directory.relative_to(root_path)}")
    
    print(f"完成! 共生成 {count} 个目录索引")

if __name__ == "__main__":
    main()