import aiohttp
import asyncio
import csv
from bs4 import BeautifulSoup

# Cabeçalhos globais para requisições
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def extract_movie_details(session, movie_link):
    html_content = await fetch(session, movie_link)
    movie_soup = BeautifulSoup(html_content, 'html.parser')

    title = None
    date = None
    rating = None
    plot_text = None

    # Encontrando o título do filme
    title_tag = movie_soup.find('h1')
    if title_tag:
        title = title_tag.get_text()

    # Encontrando a data de lançamento
    date_tag = movie_soup.find('a', href=lambda href: href and 'releaseinfo' in href)
    if date_tag:
        date = date_tag.get_text().strip()

    # Encontrando a classificação do filme
    rating_tag = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
    if rating_tag:
        rating = rating_tag.get_text()

    # Encontrando a sinopse do filme
    plot_tag = movie_soup.find('span', attrs={'data-testid': 'plot-xs_to_m'})
    if plot_tag:
        plot_text = plot_tag.get_text().strip()

    # Salvar no arquivo CSV
    if all([title, date, rating, plot_text]):
        with open('movies.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([title, date, rating, plot_text])
        print(title, date, rating, plot_text)

async def extract_movies():
    base_url = 'https://www.imdb.com'
    popular_movies_url = f'{base_url}/chart/moviemeter/?ref_=nv_mv_mpm'

    async with aiohttp.ClientSession() as session:
        html_content = await fetch(session, popular_movies_url)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontrando os links dos filmes
        movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
        movie_links = [base_url + movie.find('a')['href'] for movie in movies_table.find_all('li')]

        # Limitar a quantidade de tarefas assíncronas simultâneas
        tasks = [extract_movie_details(session, link) for link in movie_links]
        await asyncio.gather(*tasks)

def main():
    asyncio.run(extract_movies())

if __name__ == '__main__':
    main()
