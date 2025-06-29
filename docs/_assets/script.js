
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
    