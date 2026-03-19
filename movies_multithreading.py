import requests
import time
import csv
import random
import concurrent.futures
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

MAX_THREADS = 10


def extract_movie_details(movie_link):
    time.sleep(random.uniform(0.5, 1.5))
    try:
        response = requests.get(movie_link, headers=headers, timeout=10)
        movie_soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = movie_soup.find('h1')
        title = title_tag.get_text() if title_tag else "N/A"

        date_tag = movie_soup.find('a', href=lambda href: href and 'releaseinfo' in href)
        date = date_tag.get_text().strip() if date_tag else "N/A"

        rating_tag = movie_soup.find('span', attrs={'class': 'sc-bde20123-1 cCwtqy'})
        if not rating_tag:
            rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
        rating = rating_tag.find('span').get_text() if rating_tag and rating_tag.find('span') else "N/A"

        plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xl'})
        if not plot_tag:
            plot_tag = movie_soup.find('span', attrs={'role': 'presentation', 'class': 'sc-466bb6c-0 kddyTf'})
        plot_text = plot_tag.get_text().strip() if plot_tag else "N/A"

        with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
            movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            print(f"Salvando: {title}")
            movie_writer.writerow([title, date, rating, plot_text])

    except Exception as e:
        print(f"Erro ao processar {movie_link}: {e}")


def extract_movies(soup):
    links = []
    for a in soup.find_all('a', href=True):
        if '/title/tt' in a['href'] and 'video' not in a['href'] and 'plotsummary' not in a['href']:
            full_link = 'https://www.imdb.com' + a['href'].split('?')[0]
            if full_link not in links:
                links.append(full_link)

    movie_links = list(set(links))[:50]

    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)


def main():
    with open('movies.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Date', 'Rating', 'Plot'])

    print("Iniciando a extração...")
    start_time = time.time()

    url = 'https://www.imdb.com/chart/top/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    extract_movies(soup)

    end_time = time.time()
    print(f'\nConcluído! Tempo total: {end_time - start_time:.2f} segundos')


if __name__ == '__main__':
    main()