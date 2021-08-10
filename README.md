# ACL-Anthology-Crawler
A toolkit to automatically crawl the paper list and download paper pdfs of ACL Anthology (https://aclanthology.org).

## parameters
- page_url: the url of the conference page of ACL Anthology.
- conf_name: customized folder name.
- conf_id: the html element id of the paper list block, e.g., `2020-acl-main`. Try to find the element id in the Chrome DevTools (F12). 

## Run
```
python crawl.py
```

## Dependency
bs4
