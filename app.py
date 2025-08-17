from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os
import re

app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    page = int(request.args.get('page', 1))
    results_per_page = 10
    start = (page - 1) * results_per_page
    end = start + results_per_page
    if not query:
        return jsonify({'results': [], 'total_results': 0, 'page': page})
    # Tokenize the query
    tokens = [t for t in re.findall(r'\w+', query.lower()) if t]
    # Fetch a larger pool of results
    title_response = supabase.table("pages").select("title", "url", "content") \
        .filter("title", "ilike", f"%{query}%") \
        .limit(100) \
        .execute()
    content_response = supabase.table("pages").select("title", "url", "content") \
        .filter("content", "ilike", f"%{query}%") \
        .limit(100) \
        .execute()
    # Combine results, remove duplicates by URL
    seen_urls = set()
    all_results = []
    for resp in [title_response, content_response]:
        if hasattr(resp, 'data'):
            for page_data in resp.data:
                if page_data['url'] not in seen_urls:
                    all_results.append(page_data)
                    seen_urls.add(page_data['url'])
    # Scoring and ranking
    scored_results = []
    for page_data in all_results:
        score = 0
        content_lower = page_data['content'].lower()
        title_lower = page_data['title'].lower()
        # Score individual tokens
        for token in tokens:
            content_matches = len(re.findall(re.escape(token), content_lower))
            score += content_matches
            title_matches = len(re.findall(re.escape(token), title_lower))
            score += title_matches * 10
        # Exact phrase bonus
        if re.search(re.escape(query), title_lower, re.IGNORECASE):
            score += 100
        if re.search(re.escape(query), content_lower, re.IGNORECASE):
            score += 50
        scored_results.append({'result': page_data, 'score': score})
    # Sort by score descending
    scored_results.sort(key=lambda x: x['score'], reverse=True)
    total_results = len(scored_results)
    paginated_results = scored_results[start:end]
    results = []
    for item in paginated_results:
        page_data = item['result']
        content = page_data['content']
        match = re.search(re.escape(query), content, re.IGNORECASE)
        if match:
            snippet_start = max(match.start() - 100, 0)
            snippet_end = min(match.end() + 200, len(content))
            snippet = content[snippet_start:snippet_end]
            if snippet_start > 0:
                snippet = '...' + snippet
            if snippet_end < len(content):
                snippet = snippet + '...'
        else:
            snippet = content[:300]
            if len(content) > 300:
                snippet += '...'
        if query:
            snippet = re.sub(f"({re.escape(query)})", r"<mark>\1</mark>", snippet, flags=re.IGNORECASE)
        results.append({
            'title': page_data['title'],
            'url': page_data['url'],
            'snippet': snippet
        })
    return jsonify({'results': results, 'total_results': total_results, 'page': page})

if __name__ == '__main__':
    app.run(debug=True)
