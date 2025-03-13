from django.shortcuts import render, get_object_or_404
from .models import Article,News
from bs4 import BeautifulSoup
import pandas as pd
from django.utils.text import slugify
import requests
import time
import logging
import random
import httpx
from django.core.files import File
from io import BytesIO
import os
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
logging.basicConfig(level=logging.INFO)

def scrape_jianshu_article(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        with httpx.Client(verify=False) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').get_text(strip=True)
        paragraphs = soup.find_all('p')
        content = '\n'.join(p.get_text(strip=True) for p in paragraphs)
        img_tag = soup.find('img', class_='img-blur-done')  # 找到指定类名的图片
        image_url = img_tag['src'] if img_tag else None
        return content,image_url
    except Exception as e:
        print(f"抓取失败: {e}")
        return None
def save_image(image_url, folder='media/articles') :
    if not image_url :
        return None
    image_name = os.path.join(folder, image_url.split("/")[-1])  # 设置图片存储路径
    image_data = requests.get(image_url).content
    image_file = BytesIO(image_data)
    image_file.name = os.path.basename(image_name)
    return image_file
def fetch_articles() :
    base_url = "https://www.jianshu.com/c/05ad48507de4"
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }
    articles = []
    max_pages = 10
    for page in range(2, max_pages + 1) :
        url = f"{base_url}?order_by=added_at&page={page}"
        print(f"Fetching page {page}: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code != 200 :
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        image_list=soup.find_all('li',class_='have-img')
        if not image_list :
            print(f"No articles found on page {page}. Stopping.")
            break
        for article in image_list :
            try :
                image_tag = article.find('a', class_='wrap-img')
                title_tag = article.find('a', class_='title')
                if not title_tag :
                    continue
                title = title_tag.get_text(strip=True)
                link = "https://www.jianshu.com" + title_tag['href']
                short_description = article.find('p').get_text(strip=True) if article.find('p') else "No description"
                print(image_tag,'111')
                image_url = image_tag.find('img')['src'] if image_tag else None
                print(f"Found image URL: {image_url}")
                print(link,image_url)
                content = scrape_jianshu_article(link)
                image_file = save_image(image_url)
                article_instance = Article.objects.create(
                    title=title,
                    short_description=short_description,
                    content=content,
                )
                print(image_url)
                if image_file :
                    article_instance.image.save(image_file.name, File(image_file), save=True)
                    print(f"Downloaded and saved image: {image_file.name}")
                articles.append(title)
                print(f"Saved article: {title}")
                time.sleep(random.uniform(1, 3))
            except Exception as e :
                print(f"Error processing article: {e}")
                continue
    print(f"Fetched and saved {len(articles)} articles.")
    return articles
"""def fetch_article_details(link, headers):
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:  # Too Many Requests
            print("Hit rate limit, retrying after sleep...")
            time.sleep(60)  # 暂停后重试
            return fetch_article_details(link, headers)  # 递归调用
        else:
            print(f"Error fetching article details: {link}, {e}")
            return None

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', class_='show-content')
    if content_div:
        return "\n".join(p.get_text(strip=True) for p in content_div.find_all('p'))
    return None"""
def crawl_articles_view(request) :
    if request.method == 'POST' :
        articles = fetch_articles()
        return render(request, 'environment/article_crawl_result.html', {'articles' : articles})
    return render(request, 'environment/crawl_trigger.html')
def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'environment/article_list.html', {'page_obj': page_obj})
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article_content1 = article.content
    article_content1 = article_content1.replace("\\n", "<br></br>")
    article_content1=article_content1.replace('None','')
    article_content1=article_content1.replace("('",'')
    article_content1 = article_content1.replace("', )", '')
    print("去除换行符后的内容:", repr(article_content1))
    return render(request, 'environment/article_detail.html', {'article': article, 'article_content': article_content1})
def search(request):
    query = request.GET.get('query', '')
    articles = Article.objects.filter(title__icontains=query)
    return render(request, 'environment/search_results.html', {
        'articles': articles,
        'query': query
    })


