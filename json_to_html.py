import json
import html

def load_json(filename):
    """Load JSON data from file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_questions_recursive(item):
    """Recursively count all questions in an item and its nested subcategories"""
    count = 0
    if item.get('questions'):
        count += len(item['questions'])
    if item.get('subcategories'):
        for subitem in item['subcategories']:
            count += count_questions_recursive(subitem)
    return count

def calculate_stats(data):
    """Calculate statistics about the data"""
    total_questions = 0
    category_stats = []
    
    for category in data:
        cat_questions = count_questions_recursive(category)
        total_questions += cat_questions
        category_stats.append({
            'name': category.get('category', 'Unknown'),
            'count': cat_questions
        })
    
    return total_questions, category_stats

def create_html_from_json(json_file, output_file):
    """Convert JSON to interactive HTML with collapsible sections"""
    data = load_json(json_file)
    total_questions, category_stats = calculate_stats(data)
    
    stats_json = json.dumps(category_stats)
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Visualization</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .stats-section {
            background: white;
            padding: 20px;
            border-bottom: 2px solid #667eea;
        }
        
        .total-questions {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .total-questions .label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        
        .total-questions .value {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }
        
        .category-breakdown {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .category-stat {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #764ba2;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .category-stat .cat-name {
            font-size: 13px;
            color: #666;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .category-stat .cat-count {
            font-size: 24px;
            font-weight: bold;
            color: #764ba2;
        }
        
        .category-stat .cat-label {
            font-size: 11px;
            color: #999;
            margin-top: 5px;
        }
        
        .content {
            padding: 20px;
        }
        
        .category {
            margin-bottom: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .category-header {
            background: #f5f5f5;
            padding: 15px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            user-select: none;
            transition: background 0.3s ease;
        }
        
        .category-header:hover {
            background: #eeeeee;
        }
        
        .category-header .toggle {
            font-size: 18px;
            transition: transform 0.3s ease;
        }
        
        .category-header.active .toggle {
            transform: rotate(180deg);
        }
        
        .category-content {
            display: none;
            padding: 15px;
            background: #fafafa;
        }
        
        .category-content.active {
            display: block;
        }
        
        .subcategory {
            margin-bottom: 12px;
            border-left: 3px solid #667eea;
            padding-left: 15px;
        }
        
        .subcategory-name {
            font-weight: 600;
            color: #667eea;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            user-select: none;
        }
        
        .subcategory-name:hover {
            text-decoration: underline;
        }
        
        .subcategory-name .toggle {
            font-size: 14px;
            margin-left: 10px;
        }
        
        .questions-list {
            display: none;
            margin-top: 10px;
            background: white;
            border-radius: 5px;
            padding: 10px;
        }
        
        .questions-list.active {
            display: block;
        }
        
        .question {
            padding: 8px 0;
            color: #333;
            font-size: 14px;
            line-height: 1.5;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .question:last-child {
            border-bottom: none;
        }
        
        .question::before {
            content: "▪ ";
            color: #764ba2;
            margin-right: 8px;
        }
        
        .footer {
            background: #f5f5f5;
            padding: 15px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Data Visualization</h1>
            <p>Click to expand sections and explore the data</p>
        </div>
        <div class="stats-section">
            <div class="total-questions">
                <div class="label">Total Questions</div>
                <div class="value" id="totalQuestions">""" + str(total_questions) + """</div>
            </div>
            <div class="category-breakdown" id="categoryStats">
            </div>
        </div>
        <div class="content" id="content">
        </div>
        <div class="footer">
            Generated HTML visualization from JSON data
        </div>
    </div>
    
    <script>
        function renderStats(stats) {
            const statsDiv = document.getElementById('categoryStats');
            statsDiv.innerHTML = '';
            
            stats.forEach(stat => {
                const statCard = document.createElement('div');
                statCard.className = 'category-stat';
                statCard.innerHTML = `
                    <div class="cat-name">${escapeHtml(stat.name)}</div>
                    <div class="cat-count">${stat.count}</div>
                    <div class="cat-label">question${stat.count !== 1 ? 's' : ''}</div>
                `;
                statsDiv.appendChild(statCard);
            });
        }
        
        function renderSubcategories(subcategories, parentElement) {
            if (!subcategories || subcategories.length === 0) {
                return;
            }

            subcategories.forEach(subcat => {
                const subcategoryDiv = document.createElement('div');
                subcategoryDiv.className = 'subcategory';

                const subcategoryName = document.createElement('div');
                subcategoryName.className = 'subcategory-name';
                subcategoryName.innerHTML = `
                    <span>${escapeHtml(subcat.name)}</span>
                    <span class="toggle">►</span>
                `;

                const subcategoryContent = document.createElement('div');
                subcategoryContent.className = 'questions-list';

                if (subcat.questions && subcat.questions.length > 0) {
                    subcat.questions.forEach(question => {
                        const questionDiv = document.createElement('div');
                        questionDiv.className = 'question';
                        questionDiv.textContent = question;
                        subcategoryContent.appendChild(questionDiv);
                    });
                }

                if (subcat.subcategories && subcat.subcategories.length > 0) {
                    renderSubcategories(subcat.subcategories, subcategoryContent);
                }

                subcategoryName.addEventListener('click', function() {
                    subcategoryContent.classList.toggle('active');
                    subcategoryName.querySelector('.toggle').textContent =
                        subcategoryContent.classList.contains('active') ? '▼' : '►';
                });

                subcategoryDiv.appendChild(subcategoryName);
                subcategoryDiv.appendChild(subcategoryContent);
                parentElement.appendChild(subcategoryDiv);
            });
        }

        function renderData(data) {
            const contentDiv = document.getElementById('content');
            contentDiv.innerHTML = '';
            
            data.forEach((category, catIndex) => {
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'category';
                
                const categoryHeader = document.createElement('div');
                categoryHeader.className = 'category-header';
                categoryHeader.innerHTML = `
                    <span>${escapeHtml(category.category)}</span>
                    <span class="toggle">▼</span>
                `;
                
                const categoryContent = document.createElement('div');
                categoryContent.className = 'category-content';
                
                if (category.subcategories && category.subcategories.length > 0) {
                    renderSubcategories(category.subcategories, categoryContent);
                }
                
                categoryHeader.addEventListener('click', function() {
                    categoryHeader.classList.toggle('active');
                    categoryContent.classList.toggle('active');
                });
                
                categoryDiv.appendChild(categoryHeader);
                categoryDiv.appendChild(categoryContent);
                contentDiv.appendChild(categoryDiv);
            });
        }
        
        function escapeHtml(text) {
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return text.replace(/[&<>"']/g, m => map[m]);
        }
        
        // Load and render data
        const jsonData = """ + json.dumps(data) + """;
        const statsData = """ + stats_json + """;
        renderStats(statsData);
        renderData(jsonData);
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML file created successfully: {output_file}")
    print(f"  Total questions: {total_questions}")
    print(f"  Categories: {len(category_stats)}")

if __name__ == "__main__":
    json_file = "data.json"
    output_file = "data_visualization.html"
    create_html_from_json(json_file, output_file)