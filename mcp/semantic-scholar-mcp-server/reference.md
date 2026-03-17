## 01-论文关键词搜索（1积分）

根据关键词搜索学术论文

```python
import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 搜索论文
def search_papers(query, limit=10):
    url = f"{BASE}/graph/v1/paper/search"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    params = {
        'query': query,
        'limit': limit,
        'fields': 'paperId,title,authors,year,abstract,citationCount,venue'
    }

    
    try:
    response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {data.get('total', 0)} 篇论文")
        for paper in data.get('data', []):
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
            print(f"引用数: {paper.get('citationCount')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    results = search_papers("machine learning", limit=5)
```


## 02-论文批量搜索 （2积分）

支持复杂查询语法（AND/OR/短语等）

```python
import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 论文批量搜索（支持复杂查询语法）
def search_papers_bulk(query, limit=10):
    url = f"{BASE}/graph/v1/paper/search/bulk"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'query': query,
        'limit': limit,
        'fields': 'paperId,title,authors,year,abstract,citationCount,venue'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('data', []))} 篇论文")
        for paper in data.get('data', []):
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例（支持 OR/AND/短语等复杂查询）
if __name__ == "__main__":
    search_papers_bulk("machine learning | deep learning", limit=5)
```

## 03-论文标题匹配 （1积分）

根据精确标题匹配论文

```python
import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 论文标题匹配
def match_paper_by_title(title):
    url = f"{BASE}/graph/v1/paper/search/match"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'query': title,
        'fields': 'paperId,title,authors,year,abstract,citationCount,venue'
    }
    
    try:
    response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('data', []))} 篇匹配论文")
        for paper in data.get('data', []):
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
            authors = ', '.join([a.get('name', '') for a in paper.get('authors', [])])
            print(f"作者: {authors}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    match_paper_by_title("Attention Is All You Need")
```

## 04-查询建议（补全）（1积分）

标题/作者补全建议

```python
import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 查询建议（补全）
def get_autocomplete(query):
    url = f"{BASE}/graph/v1/paper/autocomplete"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {'query': query}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('matches', []))} 条建议")
        for match in data.get('matches', []):
            print(f"- {match}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    get_autocomplete("attention")
```

## 05-获取论文详情 （1积分）

通过论文ID获取完整信息

```python

import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 获取论文详情
def get_paper_details(paper_id):
    url = f"{BASE}/graph/v1/paper/{paper_id}"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'fields': 'paperId,title,authors,year,abstract,citationCount,venue,references,citations'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        paper = response.json()
        print(f"标题: {paper.get('title')}")
        print(f"年份: {paper.get('year')}")
        print(f"引用数: {paper.get('citationCount')}")
        print(f"\n作者:")
        for author in paper.get('authors', []):
            print(f"  - {author.get('name')}")
        print(f"\n摘要: {paper.get('abstract', 'N/A')}")
        return paper
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    paper = get_paper_details("649def34f8be52c8b66281af98ae884c09aef38b")

```

## 06-获取论文作者 （1积分）

获取指定论文的所有作者

```python

import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 获取论文作者
def get_paper_authors(paper_id):
    url = f"{BASE}/graph/v1/paper/{paper_id}/authors"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('data', []))} 位作者")
        for author in data.get('data', [])[:10]:
            print(f"\n姓名: {author.get('name')}")
            print(f"Author ID: {author.get('authorId')}")
            if author.get('affiliations'):
                print(f"机构: {', '.join(author['affiliations'])}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    get_paper_authors("649def34f8be52c8b66281af98ae884c09aef38b")

```

## 07-获取引用文献 （1积分）

查询引用该论文的文献

```python

import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 获取引用文献
def get_paper_citations(paper_id, limit=10):
    url = f"{BASE}/graph/v1/paper/{paper_id}/citations"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'limit': limit,
        'fields': 'paperId,title,authors,year,citationCount'
    }
    
    try:
    response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('data', []))} 篇引用文献")
        for item in data.get('data', []):
            paper = item.get('citingPaper') or item.get('citedPaper') or item
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    get_paper_citations("649def34f8be52c8b66281af98ae884c09aef38b", limit=10)

```

## 08-获取参考文献 （1积分）

获取该论文的参考文献

```python

import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 获取参考文献
def get_paper_references(paper_id, limit=10):
    url = f"{BASE}/graph/v1/paper/{paper_id}/references"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'limit': limit,
        'fields': 'paperId,title,authors,year,citationCount'
    }
    
    try:
    response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('data', []))} 篇参考文献")
        for item in data.get('data', []):
            paper = item.get('citingPaper') or item.get('citedPaper') or item
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    get_paper_references("649def34f8be52c8b66281af98ae884c09aef38b", limit=10)

```

## 09-批量获取论文详情 （2积分）

一次获取多篇论文

```python

import requests
import json

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 批量获取论文详情
def get_papers_batch(paper_ids, fields='paperId,title,authors,year,abstract,citationCount,venue'):
    url = f"{BASE}/graph/v1/paper/batch"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    # 注意：fields 必须放在 URL 参数中，不能放在 body 里
    params = {'fields': fields}
    body = {'ids': paper_ids}
    
    try:
        response = requests.post(url, headers=headers, params=params, json=body)
        response.raise_for_status()
        data = response.json()
        print(f"获取到 {len(data)} 篇论文")
        for paper in data:
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
            print(f"引用数: {paper.get('citationCount')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    ids = ['649def34f8be52c8b66281af98ae884c09aef38b', 'CorpusId:37567854']
    get_papers_batch(ids)

```

## 10-搜索作者 （1积分）

根据姓名搜索作者

```python
import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 搜索作者
def search_authors(query, limit=10):
    url = f"{BASE}/graph/v1/author/search"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'query': query,
        'limit': limit,
        'fields': 'authorId,name,paperCount,citationCount,hIndex'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('data', []))} 位作者")
        for author in data.get('data', []):
            print(f"\n姓名: {author.get('name')}")
            print(f"论文数: {author.get('paperCount', 'N/A')}")
            print(f"引用数: {author.get('citationCount', 'N/A')}")
            print(f"h-index: {author.get('hIndex', 'N/A')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    search_authors("Geoffrey Hinton", limit=10)
```

## 11-获取作者详情 （1积分）

获取作者的详细信息

```python

import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 获取作者详情
def get_author_details(author_id):
    url = f"{BASE}/graph/v1/author/{author_id}"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(f"姓名: {data.get('name')}")
        print(f"论文数: {data.get('paperCount', 'N/A')}")
        print(f"引用数: {data.get('citationCount', 'N/A')}")
        print(f"h-index: {data.get('hIndex', 'N/A')}")
        if data.get('homepage'):
            print(f"主页: {data['homepage']}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    get_author_details("1741101")

```

## 12-获取作者论文 （1积分）

作者发表论文列表

```python

import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 获取作者论文
def get_author_papers(author_id, limit=20):
    url = f"{BASE}/graph/v1/author/{author_id}/papers"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'limit': limit,
        'fields': 'paperId,title,year,citationCount,venue'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('data', []))} 篇论文")
        for paper in data.get('data', [])[:10]:
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
            print(f"引用数: {paper.get('citationCount')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    get_author_papers("1741101", limit=20)

```

## 13-批量获取作者 （2积分）

一次获取多位作者信息

```python

import requests
import json

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 批量获取作者
def get_authors_batch(author_ids):
    url = f"{BASE}/graph/v1/author/batch"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    body = {'ids': author_ids}
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        print(f"获取到 {len(data)} 位作者")
        for author in data:
            print(f"\n姓名: {author.get('name')}")
            print(f"论文数: {author.get('paperCount', 'N/A')}")
            print(f"h-index: {author.get('hIndex', 'N/A')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    ids = ['1741101', '2109393']
    get_authors_batch(ids)

```

## 14-文本片段搜索 （1积分）

返回最匹配的文本片段

```python

import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 文本片段搜索
def search_snippets(query, limit=5):
    url = f"{BASE}/graph/v1/snippet/search"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {'query': query, 'limit': limit}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"找到 {len(data.get('data', []))} 条片段")
        for snippet in data.get('data', []):
            text = snippet.get('text', '')
            print(f"\n片段: {text[:200]}...")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    search_snippets("deep learning", limit=5)

```

## 15-单篇论文推荐 （1积分）

为指定论文推荐相关文献

```python

import requests

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 单篇论文推荐
def get_recommendations_for_paper(paper_id, limit=10):
    url = f"{BASE}/recommendations/v1/papers/forpaper/{paper_id}"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    params = {
        'limit': limit,
        'fields': 'paperId,title,authors,year,citationCount'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        papers = data.get('recommendedPapers', [])
        print(f"推荐了 {len(papers)} 篇论文")
        for paper in papers:
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    get_recommendations_for_paper("649def34f8be52c8b66281af98ae884c09aef38b", limit=10)

```

## 16-获取推荐论文 （1积分）

基于正负例获取推荐

```python

import requests
import json

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

# 获取推荐论文（基于正负例）
def get_recommendations_bulk(positive_ids, negative_ids=None, limit=10):
    url = f"{BASE}/recommendations/v1/papers/"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    body = {
        'positivePaperIds': positive_ids,
        'negativePaperIds': negative_ids or [],
        'fields': 'paperId,title,authors,year,citationCount'
    }
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        papers = data.get('recommendedPapers', [])
        print(f"推荐了 {len(papers)} 篇论文")
        for paper in papers:
            print(f"\n标题: {paper.get('title')}")
            print(f"年份: {paper.get('year')}")
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    positive = ['649def34f8be52c8b66281af98ae884c09aef38b']
    negative = []
    get_recommendations_bulk(positive, negative, limit=10)

```

## 17-论文PDF下载 （1积分）

通过标题/DOI下载论文PDF，支持批量

```python
#!/usr/bin/env python3
"""
论文PDF下载器 - 通过标题或DOI下载学术论文
支持单篇下载和CSV批量下载
"""

import requests
import json
import csv
import os
from pathlib import Path

API_KEY = "your_api_key_here"
BASE = "https://ai4scholar.net"

class PaperDownloader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def get_paper_by_doi(self, doi):
        """通过DOI获取论文信息"""
        url = f"{BASE}/graph/v1/paper/DOI:{doi}"
        params = {'fields': 'paperId,title,authors,year,abstract,citationCount,venue,openAccessPdf,externalIds'}
        response = self.session.get(url, params=params)
        if response.status_code == 404:
        return None
        response.raise_for_status()
        return response.json()
    
    def search_by_title(self, title):
        """通过标题搜索论文"""
        url = f"{BASE}/graph/v1/paper/search"
        params = {'query': title, 'limit': 5, 'fields': 'paperId,title,authors,year,openAccessPdf,externalIds'}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        papers = response.json().get('data', [])
        return papers[0] if papers else None
    
    def download_pdf(self, paper, output_dir='./output'):
        """下载论文PDF"""
        pdf_info = paper.get('openAccessPdf')
        if not pdf_info or not pdf_info.get('url'):
            print(f"❌ 无开放获取PDF: {paper.get('title', 'Unknown')}")
            return False
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        paper_id = paper.get('paperId', 'unknown')
        filepath = os.path.join(output_dir, f"{paper_id}.pdf")
        
        response = self.session.get(pdf_info['url'], stream=True, timeout=60)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ 下载完成: {paper_id}.pdf")
        return True

# 使用示例
if __name__ == "__main__":
    downloader = PaperDownloader(API_KEY)
    
    # 方式1: 通过DOI下载
    paper = downloader.get_paper_by_doi("10.1038/s41586-021-03819-2")
    if paper:
        downloader.download_pdf(paper, './output')
    
    # 方式2: 通过标题下载
    paper = downloader.search_by_title("Attention is All You Need")
    if paper:
        downloader.download_pdf(paper, './output')
```


