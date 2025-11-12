# %%
from bs4 import BeautifulSoup
import json
import numpy as np
import requests
import os
from tqdm import tqdm

# page_url = "https://aclanthology.org/events/emnlp-2025/"
# conf_id = '2025emnlp-main'

# %%
def get_bs_soup_from_url(url):
    """Given a URL, return the BeautifulSoup object of the HTML content."""
    html_doc = requests.get(url).text
    return BeautifulSoup(html_doc, 'html.parser')

def get_main_section(html_soup):
    """Return the main section containing multiple sub sections."""
    return html_soup.find(id = 'main')

def get_sub_sections(main_section):
    """
    Get a list of sub sections in the main section.
    Each sub section is a "div" tag with an "id" attribute.

    Return a list of tuples: (sub_section_id, sub_section_title)
    """
    sub_sections = []
    for div in main_section.find_all('div', recursive = False):
        if 'id' in div.attrs:
            sub_section_id = div['id']
            sub_section_title = find_title(div)
            sub_sections.append((sub_section_id, sub_section_title))
    return sub_sections

def find_title(soup_obj):
    """
    Find the title of the sub section by looking the h tag with class d-sm-flex. Return its text.
    """
    h_tags = soup_obj.find_all(['h2', 'h3', 'h4', 'h5', 'h6'], class_ = 'd-sm-flex')
    for h in h_tags:
        # Find all "a" tag, whose class do not contain "badge"
        for a in h.find_all('a'):
            if 'badge' not in a.get('class', []):
                return a.get_text().strip()
    return "Unknown Section Title"
def find_paper_list(soup, section_id):
    """
    Given the soup object and section id, return the list of paper entries in that section.
    Each paper entry is a "p" tag with class "d-sm-flex".
    """
    paper_list = []
    section_div = soup.find('div', id = section_id)
    for paper_p in section_div.find_all('p', class_ = "d-sm-flex"):
        pdf_url = paper_p.contents[0].contents[0]['href']
        paper_span = paper_p.contents[-1]
        assert paper_span.name == 'span'
        paper_a = paper_span.strong.a
        title = paper_a.get_text()
        url = "https://aclanthology.org" + paper_a['href']
        paper_list.append(
            {"title": title, "url": url, "pdf_url": pdf_url}
        )
    
    return paper_list

def save_papers(paper_list, conf_name):
    if not os.path.exists(conf_name):
        os.mkdir(conf_name)

    illegal_chr = r'\/:*?<>|'
    table = ''.maketrans('', '', illegal_chr)
    for i, paper in tqdm(list(enumerate(paper_list))):
        r = requests.get(paper["pdf_url"])
        n = '{}.{}.pdf'.format(i+1, paper["title"].translate(table))
        with open('./{}/{}'.format(conf_name, n), 'wb') as f:
            f.write(r.content)
# %%
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('task', help = 'What to do: show: show sub section ids; get_info: get paper info; download: download all papers.')
    parser.add_argument('--url', type=str, help='The URL of the ACL Anthology conference page to crawl, e.g., https://aclanthology.org/events/emnlp-2025/')
    parser.add_argument('--sec_ids', type=str, nargs='+', default=None, help='The IDs of the sub sections to process. If not provided, only the first section will be processed.')
    
    parser.add_argument('--save_path', type=str, help='The path to save the output JSON file. Default to current directory.')
    parser.add_argument('--save_dir', type=str, help='The path to save the pdf papers. Default to "./paper_pdf"', default = './paper_pdf')
    args = parser.parse_args()

    if args.url is None:
        raise ValueError("Please provide the URL of the ACL Anthology conference page to crawl using --url argument.")
    soup = get_bs_soup_from_url(args.url)
    main_section = get_main_section(soup)
    sub_sections = get_sub_sections(main_section)

    if args.task == 'show':
        for sec_id, sec_title in sub_sections:
            print(f"Section ID: {sec_id}, Title: {sec_title}")
    else:
        all_papers = []
        target_sec_ids = args.sec_ids if args.sec_ids is not None else [sub_sections[0][0]]
        for sec_id in target_sec_ids:
            papers = find_paper_list(soup, sec_id)
            for paper in papers:
                paper['section_id'] = sec_id
            all_papers.extend(papers)
        print('Total papers found:', len(all_papers))
        
        if args.task == 'get_info':
            save_path = args.save_path if args.save_path is not None else 'paper_list_{}.jsonl'.format(args.url.strip('/').split('/')[-1])
            with open(save_path, 'w', encoding='utf-8') as f:
                for row in all_papers:
                    f.write(json.dumps(row, ensure_ascii=False) + '\n')
        elif args.task == 'download':
            save_papers(all_papers, args.save_dir)