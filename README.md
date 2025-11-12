# ACL-Anthology-Crawler
A toolkit to automatically crawl the paper list and download paper pdfs of ACL Anthology (https://aclanthology.org).

## Usage

```Bash
python crawl.py -h
usage: crawl.py [-h] [--url URL] [--sec_ids SEC_IDS [SEC_IDS ...]] [--save_path SAVE_PATH] task

positional arguments:
  task                  What to do: show: show sub section ids; get_info: get paper info; download: download all papers.

options:
  -h, --help            show this help message and exit
  --url URL             The URL of the ACL Anthology conference page to crawl, e.g., https://aclanthology.org/events/emnlp-2025/
  --sec_ids SEC_IDS [SEC_IDS ...]
                        The IDs of the sub sections to process. If not provided, only the first section will be processed.
  --save_path SAVE_PATH
                        The path to save the output JSON file. Default to current directory.
```

### Show Sub-section IDs

Each conference may have main conference papers, findings, workshops... You can list all these sub sections by

```Bash
python crawl.py show --url https://aclanthology.org/events/emnlp-2025/
```

The output is:
```Text
Section ID: 2025emnlp-main, Title: Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing
Section ID: 2025emnlp-demos, Title: Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: System Demonstrations
Section ID: 2025emnlp-industry, Title: Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Industry Track
Section ID: 2025emnlp-tutorials, Title: Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Tutorial Abstracts
Section ID: 2025findings-emnlp, Title: Findings of the Association for Computational Linguistics: EMNLP 2025
Section ID: 2025arabicnlp-main, Title: Proceedings of The Third Arabic Natural Language Processing Conference
Section ID: 2025arabicnlp-sharedtasks, Title: Proceedings of The Third Arabic Natural Language Processing Conference: Shared Tasks
...
```

### Get Paper List of One (or more) Sub-Sections

For example, you can get the paper list (title, pdf_url) of the main conference of EMNLP 2025 by

```Bash
python crawl.py get_info --url https://aclanthology.org/events/emnlp-2025/ --sec_ids 2025emnlp-main
# if you don't specify sec_ids, it will default to download the first section, which is usually the main conference.
```

The output file's each line is a JSON string:
```json
{"title": "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing", "url": "https://aclanthology.org/2025.emnlp-main.0/", "pdf_url": "https://aclanthology.org/2025.emnlp-main.0.pdf", "section_id": "2025emnlp-main"}
```


## Run
```
python crawl.py
```

## Dependency
bs4
