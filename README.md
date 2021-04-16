# Google Scholar Profile Scrapper
Extract metadata and citation info from a Google Scholar Profile html page

Example of usage:
```python
import GoogleScholarProfile as gsp
import requests
import pandas as pd

file=requests.get('https://scholar.google.com/citations?user=1sKULCoAAAAJ&hl=en').text
l=gsp.GoogleScholarProfile(file,prefix='')

pd.DataFrame(l)[:2]
```
