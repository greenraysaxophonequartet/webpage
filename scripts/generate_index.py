import os
import glob
import re
from datetime import datetime

# 設定
PAGES_DIR = 'pages'
OUTPUT_FILE = 'index.html'

# HTMLのヘッダー部分（Tailwind CSSを使ってデザインを整えています）
HTML_HEADER = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>社内連絡ポータル</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="max-w-3xl mx-auto py-10 px-4">
        <header class="mb-8 text-center">
            <h1 class="text-3xl font-bold text-gray-800">社内連絡ポータル</h1>
            <p class="text-gray-500 mt-2">最新の連絡事項一覧</p>
        </header>
        
        <main class="bg-white shadow rounded-lg overflow-hidden">
            <ul class="divide-y divide-gray-200">
"""

# HTMLのフッター部分
HTML_FOOTER = """            </ul>
        </main>
        
        <footer class="text-center text-gray-400 text-sm mt-8">
            <p>最終更新: {update_time}</p>
        </footer>
    </div>
</body>
</html>
"""

def get_page_info(filepath):
    """HTMLファイルからタイトルと更新日を取得する"""
    filename = os.path.basename(filepath)
    title = filename # デフォルトはファイル名

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # <title>タグの中身を探す
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if match:
                title = match.group(1)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    # ファイルの作成日時（またはファイル名に含まれる日付）を取得
    # ここではシンプルにファイルの更新時刻を使用
    mod_time = os.path.getmtime(filepath)
    date_str = datetime.fromtimestamp(mod_time).strftime('%Y/%m/%d')
    
    return {
        'path': filepath,
        'title': title,
        'date': date_str,
        'filename': filename
    }

def main():
    # pagesフォルダ内のhtmlファイルを取得
    files = glob.glob(os.path.join(PAGES_DIR, '*.html'))
    
    # ファイル名で逆順ソート（日付が新しいものが上に来るように、ファイル名は「YYYY-MM-DD」で始めるのを推奨）
    files.sort(reverse=True)

    items_html = ""
    
    if not files:
        items_html = '<li class="p-4 text-center text-gray-500">記事がありません</li>'
    else:
        for filepath in files:
            info = get_page_info(filepath)
            
            # リストアイテムの生成
            items_html += f"""
                <li class="hover:bg-gray-50 transition duration-150 ease-in-out">
                    <a href="{info['path']}" class="block p-4 sm:px-6">
                        <div class="flex items-center justify-between">
                            <p class="text-lg font-medium text-blue-600 truncate">{info['title']}</p>
                            <div class="ml-2 flex-shrink-0 flex">
                                <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                    News
                                </p>
                            </div>
                        </div>
                        <div class="mt-2 sm:flex sm:justify-between">
                            <div class="sm:flex">
                                <p class="flex items-center text-sm text-gray-500">
                                    📄 {info['filename']}
                                </p>
                            </div>
                            <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                                <p>📅 {info['date']}</p>
                            </div>
                        </div>
                    </a>
                </li>
            """

    # 現在時刻
    now = datetime.now().strftime('%Y/%m/%d %H:%M')
    
    # 最終的なHTMLを結合
    full_html = HTML_HEADER + items_html + HTML_FOOTER.format(update_time=now)

    # index.htmlに書き込み
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
