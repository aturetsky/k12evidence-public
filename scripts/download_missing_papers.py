"""
Attempt open-access downloads for all missing papers.
Uses Unpaywall API (free, no key needed for polite use) and direct NBER/SSRN URLs.
"""

import os
import re
import time
import requests
from pathlib import Path

REPO = Path("/home/ubuntu/k12-education-research")
OUTPUT_DIR = REPO / "literature" / "papers" / "missing_downloads"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EMAIL = "avi.turetsky@case.edu"  # polite Unpaywall usage

# The 49 missing papers with their known DOIs or NBER/SSRN numbers
# Format: (bib_key, title, first_author, year, doi_or_url)
MISSING_PAPERS = [
    ("angrist2019", "Maimonides Rule Redux", "Angrist", "2019", "10.1093/qje/qjz001"),
    ("bailey2021", "Prep School for Poor Kids: Head Start", "Bailey", "2021", "10.1257/aer.20181801"),
    ("blazar2018", "Validating Teacher Effects on Students Attitudes", "Blazar", "2018", "10.3102/0162373718759442"),
    ("campbell2014", "Early Childhood Investments Substantially Boost Adult Health", "Campbell", "2014", "10.1126/science.1248429"),
    ("campbell2021", "Developing Teachers as Professionals", "Campbell", "2021", "10.1177/0895904821993830"),
    ("cook2015", "Not Too Late: Improving Academic Outcomes for Disadvantaged Youth", "Cook", "2015", "https://nber.org/papers/w21001"),
    ("credostanford2015", "Urban Charter School Study", "CREDO", "2015", "https://credo.stanford.edu/wp-content/uploads/2021/08/urban_charter_school_study_report_2015.pdf"),
    ("darlinghammond2010", "The Flat World and Education", "Darling-Hammond", "2010", None),
    ("deming2009", "Early Childhood Intervention and Life-Cycle Skill Development", "Deming", "2009", "10.1257/app.1.3.111"),
    ("duckworth2009", "Development and Validation of the Short Grit Scale", "Duckworth", "2009", "10.1177/1073191109350193"),
    ("durlak2011", "The Impact of Enhancing Students Social and Emotional Learning", "Durlak", "2011", "10.1111/j.1467-8624.2010.01564.x"),
    ("ehri2001", "Systematic Phonics Instruction Helps Students Learn to Read", "Ehri", "2001", "10.3102/00346543071003393"),
    ("fryer2014", "Injecting Charter School Best Practices into Traditional Public Schools", "Fryer", "2014", "10.1093/qje/qju011"),
    ("goldhaber2022", "Consequences of Remote and Hybrid Instruction During the Pandemic", "Goldhaber", "2022", "https://nber.org/papers/w30010"),
    ("greenberg2009", "How Citation Distortions Create Unfounded Authority", "Greenberg", "2009", "10.1136/bmj.b2680"),
    ("guryan2023", "Not Too Late: Improving Academic Outcomes Among Adolescents", "Guryan", "2023", "https://nber.org/papers/w28531"),
    ("hanford2018", "Hard Words: Why Aren't Kids Being Taught to Read", "Hanford", "2018", "https://www.apmreports.org/episode/2018/09/10/hard-words-why-american-kids-cant-read"),
    ("hanushek2003", "The Failure of Input-Based Schooling Policies", "Hanushek", "2003", "10.1111/1468-0297.00099"),
    ("hanushek2011", "The Economic Value of Higher Teacher Quality", "Hanushek", "2011", "10.1016/j.econedurev.2010.12.006"),
    ("hanushek2015", "The Knowledge Capital of Nations", "Hanushek", "2015", None),
    ("howell2002", "School Vouchers and Academic Performance", "Howell", "2002", "10.1177/0895904802016003002"),
    ("hoxby2009", "Charter Schools in New York City", "Hoxby", "2009", "https://nber.org/papers/w14852"),
    ("jackson2018b", "What Do Test Scores Miss", "Jackson", "2018", "10.1086/699018"),
    ("jones2019", "The Evidence Base for How We Learn", "Jones", "2019", "https://www.aspeninstitute.org/wp-content/uploads/2019/09/SEAD-Research-Brief-9.17.19.pdf"),
    ("kjeldsen2014", "Gains from Training in Phonological Awareness in Kindergarten", "Kjeldsen", "2014", "10.1007/s11145-013-9459-2"),
    ("krueger1999", "Experimental Estimates of Education Production Functions", "Krueger", "1999", "10.1162/003355399556052"),
    ("lipsey2018", "Effects of the Tennessee Voluntary Prekindergarten Program", "Lipsey", "2018", "10.3102/0002831217751054"),
    ("mourshed2010", "How the Worlds Most Improved School Systems Keep Getting Better", "Mourshed", "2010", "https://www.mckinsey.com/~/media/mckinsey/industries/public%20and%20social%20sector/our%20insights/how%20the%20worlds%20most%20improved%20school%20systems%20keep%20getting%20better/how_the_worlds_most_improved_school_systems_keep_getting_better.pdf"),
    ("nickow2020", "The Impressive Effects of Tutoring on PreK-12 Learning", "Nickow", "2020", "https://nber.org/papers/w27476"),
    ("porter2022", "Implementing the Every Student Succeeds Act", "Porter", "2022", "10.1177/08959048211070739"),
    ("reardon2011", "The Widening Academic Achievement Gap Between the Rich and the Poor", "Reardon", "2011", None),
    ("rivkin2005", "Teachers Schools and Academic Achievement", "Rivkin", "2005", "10.1111/j.1468-0262.2005.00584.x"),
    ("rouse1998", "Private School Vouchers and Student Achievement", "Rouse", "1998", "10.1162/003355398555568"),
    ("sahlberg2020", "Finnish Lessons 3.0", "Sahlberg", "2020", None),
    ("shanahan2010", "The National Early Literacy Panel", "Shanahan", "2010", None),
    ("sims2023", "Quantifying Promising Trials Bias in RCTs", "Sims", "2023", "10.1080/19345747.2022.2090470"),
    ("sisk2018", "To What Extent Are Growth Mindsets Important", "Sisk", "2018", "10.1177/0956797617739704"),
    ("tan2020", "Education-Related Intensive Parenting", "Tan", "2020", "10.1007/s10648-020-09529-x"),
    ("walters2018", "The Demand for Effective Charter Schools", "Walters", "2018", "10.1086/697203"),
    # Additional ones that may have been missed by the fuzzy match
    ("angrist2013", "Stand and Deliver: Effects of Boston's Charter Schools", "Angrist", "2013", "https://nber.org/papers/w17890"),
    ("abdulkadiroglu2011", "Accountability and Flexibility in Public Schools", "Abdulkadiroglu", "2011", "https://nber.org/papers/w17332"),
    ("cohodes2021", "Can Successful Schools Replicate", "Cohodes", "2021", "10.1257/app.20200005"),
    ("garca2022", "The Lasting Effects of Early Childhood Education", "Garcia", "2022", "https://nber.org/papers/w30004"),
    ("heckman2010", "The Rate of Return to the HighScope Perry Preschool Program", "Heckman", "2010", "https://nber.org/papers/w15471"),
    ("jackson2016", "The Effects of School Spending on Educational and Economic Outcomes", "Jackson", "2016", "https://nber.org/papers/w20847"),
    ("lafortune2018", "School Finance Reform and Distribution of Student Achievement", "Lafortune", "2018", "https://nber.org/papers/w22011"),
    ("nickow2024", "The Promise of Tutoring for PreK-12 Learning", "Nickow", "2024", "https://nber.org/papers/w27476"),
    ("angrist2002", "New Evidence on Classroom Computers and Pupil Learning", "Angrist", "2002", "10.1111/1468-0297.00068"),
    ("greenberg2009", "How Citation Distortions Create Unfounded Authority", "Greenberg", "2009", "10.1136/bmj.b2680"),
]

def try_unpaywall(doi, output_path):
    """Try to get open-access PDF via Unpaywall API."""
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if data.get("best_oa_location") and data["best_oa_location"].get("url_for_pdf"):
                pdf_url = data["best_oa_location"]["url_for_pdf"]
                return download_pdf(pdf_url, output_path)
    except Exception as e:
        pass
    return False

def download_pdf(url, output_path):
    """Download a PDF from a URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (research; mailto:avi.turetsky@case.edu)"}
        r = requests.get(url, timeout=30, headers=headers, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 10000:
            # Check it's actually a PDF
            if r.content[:4] == b'%PDF' or 'pdf' in r.headers.get('content-type', '').lower():
                with open(output_path, 'wb') as f:
                    f.write(r.content)
                return True
    except Exception as e:
        pass
    return False

results = {"downloaded": [], "failed": []}

for key, title, author, year, doi_or_url in MISSING_PAPERS:
    output_path = OUTPUT_DIR / f"{key}_{author.lower().replace(' ', '_')}_{year}.pdf"
    
    if output_path.exists() and output_path.stat().st_size > 10000:
        print(f"  ALREADY EXISTS: {key}")
        results["downloaded"].append((key, title, str(output_path)))
        continue
    
    print(f"  Trying: {key} ({author} {year})...")
    success = False
    
    if doi_or_url:
        if doi_or_url.startswith("http"):
            # Direct URL
            success = download_pdf(doi_or_url, output_path)
        else:
            # DOI - try Unpaywall first
            success = try_unpaywall(doi_or_url, output_path)
            if not success:
                # Try sci-hub style direct DOI resolve
                direct_url = f"https://doi.org/{doi_or_url}"
                # Try unpaywall PDF link directly
                try:
                    r = requests.get(f"https://api.unpaywall.org/v2/{doi_or_url}?email={EMAIL}", timeout=15)
                    if r.status_code == 200:
                        data = r.json()
                        locs = data.get("oa_locations", [])
                        for loc in locs:
                            if loc.get("url_for_pdf"):
                                success = download_pdf(loc["url_for_pdf"], output_path)
                                if success:
                                    break
                except:
                    pass
    
    if success:
        size = output_path.stat().st_size
        print(f"    ✓ Downloaded ({size//1024}KB)")
        results["downloaded"].append((key, title, str(output_path)))
    else:
        print(f"    ✗ Failed - needs CWRU access")
        results["failed"].append((key, title, author, year, doi_or_url))
    
    time.sleep(1)  # polite rate limiting

print(f"\n=== RESULTS ===")
print(f"Successfully downloaded: {len(results['downloaded'])}")
print(f"Still need CWRU access: {len(results['failed'])}")

# Save the list of papers still needing CWRU access
with open(REPO / "literature" / "needs_cwru_access.md", "w") as f:
    f.write("# Papers Needing CWRU Library Access\n\n")
    f.write("Use these Google Scholar search terms to find and download each paper.\n\n")
    f.write("| # | Search Term | Author | Year | DOI/URL |\n")
    f.write("|---|---|---|---|---|\n")
    for i, (key, title, author, year, doi) in enumerate(results["failed"], 1):
        search_term = f'"{title[:50]}" {author}'
        doi_str = doi if doi else "N/A"
        f.write(f"| {i} | `{search_term}` | {author} | {year} | {doi_str} |\n")

print(f"CWRU list saved to literature/needs_cwru_access.md")
