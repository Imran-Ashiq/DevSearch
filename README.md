# DevSearch - A Niche Developer Search Engine

DevSearch is a custom-built search engine created from the ground up, designed specifically for developers. It focuses on indexing high-quality tutorials, project ideas, and resources for Python and JavaScript.

**Live Application URL:** [Link to your deployed Google Cloud Run app will go here]

<img width="1780" height="850" alt="Image" src="https://github.com/user-attachments/assets/224c7edc-ca3d-4455-8d38-3a73fa095133" />

## Project Overview
This project was built to explore and implement the core principles of modern web search engines. It's a full-stack application featuring a custom web crawler, a sophisticated search ranking algorithm, and a responsive web interface built with Flask.

Unlike a general-purpose search engine, DevSearch aims for quality over quantity by focusing its index on a curated set of authoritative developer-focused websites.

## Key Features
- **Custom Web Crawler:** An ethical and efficient crawler built with Python (requests & BeautifulSoup) that respects robots.txt and filters by content type.
- **Intelligent Search Ranking:** Results are ranked by relevance using a custom algorithm that scores based on term frequency, title weighting, and an exact-phrase bonus.
- **Dynamic Web Interface:** A modern, responsive frontend built with Flask, HTML, CSS, and JavaScript, featuring a two-state UI, pagination, and a loading indicator.
- **Niche-Focused Index:** The crawler's seed list is curated to focus on high-quality content for Python and JavaScript developers, ensuring relevant results.
- **Production-Ready:** The application is configured for production deployment using Gunicorn and is ready to run on cloud platforms like Google Cloud Run.

## Technology Stack
- **Backend:** Python, Flask, Gunicorn
- **Database & Indexing:** Supabase (PostgreSQL)
- **Web Crawling:** requests, BeautifulSoup
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Deployment:** Google Cloud Run, Git/GitHub

## Local Development Setup
To run this project on your local machine, follow these steps:

### Clone the Repository:
```bash
git clone [your-repo-link]
cd DevSearch
```

### Create and Activate a Virtual Environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Set Up Environment Variables:
This project requires Supabase credentials to run. You must set the following environment variables in your terminal session before launching the application:

```powershell
# In PowerShell (Windows)
$env:SUPABASE_URL="YOUR_SUPABASE_PROJECT_URL"
$env:SUPABASE_KEY="YOUR_SUPABASE_API_KEY"
```
```bash
# In Bash (macOS/Linux)
export SUPABASE_URL="YOUR_SUPABASE_PROJECT_URL"
export SUPABASE_KEY="YOUR_SUPABASE_API_KEY"
```

### Run the Application:
```bash
python app.py
```
The application will be available at http://127.0.0.1:5000.

## Future Roadmap: Making it Even More Intelligent
This project is a solid foundation, and the next steps are focused on enhancing search relevance and quality. Our future vision includes:

- **Content Freshness Ranking:** Integrate a scoring bonus for more recently crawled content, ensuring that the latest articles and tutorials rank higher.
- **Implementing Simplified PageRank:** The ultimate goal is to move beyond simple text analysis. We plan to build a system that analyzes the link graph of our index, giving a higher rank to pages that are linked to by other authoritative pages.
- **Query Suggestion & "Did You Mean?":** Improve the user experience by suggesting corrections for common typos or offering alternative search queries.
- **Expanding the Index:** Methodically add new, high-quality seeds to the crawler to grow the index for other programming languages and tech stacks.

