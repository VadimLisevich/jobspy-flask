from flask import Flask, request
from jobspy import scrape_jobs
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h2>JobSpy Scraper</h2>
        <form action="/scrape">
            Search term: <input name="term" value="project manager"><br>
            Location (optional): <input name="location" placeholder="e.g. Lisbon, Portugal or worldwide"><br>
            <input type="submit" value="Scrape Jobs">
        </form>
    '''

@app.route('/scrape')
def scrape():
    term = request.args.get('term', 'project manager')
    location = request.args.get('location', '').strip()
    if not location:
        location = 'worldwide'

    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=term,
            location=location,
            results_wanted=10,
            hours_old=24,
            country_indeed="portugal"
        )
    except Exception as e:
        return f"<p>Error while scraping: {str(e)}</p>"

    if jobs.empty:
        return "<p>No jobs found.</p>"

    # Отладочная информация в логах Render
    print("🔎 Получены столбцы:", list(jobs.columns))

    result = "<h3>Found Jobs:</h3><ul>"
    for _, row in jobs.iterrows():
        title = row.get('title', 'No Title')
        company = row.get('company', 'Unknown Company')
        link = row.get('url', '#')
        result += f"<li><a href='{link}' target='_blank'>{title} – {company}</a></li>"
    result += "</ul>"

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
