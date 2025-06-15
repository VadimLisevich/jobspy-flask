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
            Location: <input name="location" value="Lisbon, Portugal"><br>
            <input type="submit" value="Scrape Jobs">
        </form>
    '''

@app.route('/scrape')
def scrape():
    term = request.args.get('term', 'project manager')
    location = request.args.get('location', 'Lisbon, Portugal')

    jobs = scrape_jobs(
        site_name=["linkedin", "indeed"],
        search_term=term,
        location=location,
        results_wanted=10,
        hours_old=24,
        country_indeed="portugal"
    )

    if jobs.empty:
        return "<p>No jobs found.</p>"

    result = "<h3>Results:</h3><ul>"
    for _, row in jobs.iterrows():
        result += f"<li><a href='{row['url']}' target='_blank'>{row['title']} – {row.get('company', 'N/A')}</a></li>"
    result += "</ul>"

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
