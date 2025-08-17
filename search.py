"""
search.py - WebWanderer Search Interface
Step 4 & 5: Command-line search of indexed pages
"""
from supabase import create_client, Client
import config

# Initialize Supabase client
supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def search_pages(query):
    # Search for query in title (case-insensitive)
    title_response = supabase.table("pages").select("title", "url") \
        .filter("title", "ilike", f"%{query}%") \
        .execute()
    # Search for query in content (case-insensitive)
    content_response = supabase.table("pages").select("title", "url") \
        .filter("content", "ilike", f"%{query}%") \
        .execute()
    # Combine results, remove duplicates by URL
    seen_urls = set()
    results = []
    for resp in [title_response, content_response]:
        if hasattr(resp, 'data'):
            for page in resp.data:
                if page['url'] not in seen_urls:
                    results.append(page)
                    seen_urls.add(page['url'])
    return results

if __name__ == "__main__":
    print("Welcome to WebWanderer Search!")
    while True:
        user_query = input("Enter your search query (or type 'exit' to quit): ").strip()
        if user_query.lower() == 'exit':
            print("Goodbye!")
            break
        results = search_pages(user_query)
        if results:
            print("\nSearch Results:")
            for idx, page in enumerate(results, 1):
                print(f"{idx}. {page['title']} - [{page['url']}]")
            print()
        else:
            print("No results found. Try a different query.\n")
