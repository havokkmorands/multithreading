import asyncio
import aiohttp
import csv
import random
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
}

async def fetch(session, url):
    await asyncio.sleep(random.uniform(0, 0.2))
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def extract_movie_details(session, movie_link, writer):
    html = await fetch(session, movie_link)
    movie_soup = BeautifulSoup(html, 'html.parser')

    if movie_soup:
        title, date, rating, plot_text = None, None, None, None

        page_section = movie_soup.find('section', attrs={'class': 'ipc-page-section'})
        if page_section:
            divs = page_section.find_all('div', recursive=False)
            if len(divs) > 1:
                target_div = divs[1]

                title_tag = target_div.find('h1')
                if title_tag:
                    title = title_tag.find('span').get_text()

                date_tag = target_div.find('a', href=lambda href: href and 'releaseinfo' in href)
                if date_tag:
                    date = date_tag.get_text().strip()

                rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
                rating = rating_tag.get_text() if rating_tag else None

                plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
                plot_text = plot_tag.get_text().strip() if plot_tag else None

                if all([title, date, rating, plot_text]):
                    print(title, date, rating, plot_text)
                    writer.writerow([title, date, rating, plot_text])

async def extract_movies(session, soup):
    movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
    movies_table_rows = movies_table.find_all('li')
    movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows]

    tasks = []
    with open('movies_async.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for link in movie_links:
            tasks.append(extract_movie_details(session, link, writer))
        await asyncio.gather(*tasks)

async def main():
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, popular_movies_url)
        soup = BeautifulSoup(html, 'html.parser')
        await extract_movies(session, soup)

if __name__ == '__main__':
    asyncio.run(main())
