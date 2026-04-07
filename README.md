# 🎬 Multithreading Web Scraper (v2)

Este projeto demonstra a utilização de **multithreading em Python** para
realizar **web scraping de múltiplas páginas simultaneamente**,
melhorando o desempenho na coleta de dados.

## Sobre o projeto

Esta é a **versão 2** do scraper.

-   A **versão 1** realizava scraping diretamente do **IMDb**
-   Porém, devido a mudanças constantes na estrutura do site e
    mecanismos de proteção (como WAF e bloqueios), a abordagem se tornou
    instável

Por isso, nesta versão foi adotado um ambiente controlado, utilizando
um site próprio hospedado no **GitHub Pages**

------------------------------------------------------------------------

## Objetivo

Demonstrar de forma prática:

-   Uso de `requests` para requisições HTTP
-   Parsing de HTML com `BeautifulSoup`
-   Execução concorrente com `ThreadPoolExecutor`
-   Coleta de dados estruturados a partir de múltiplas páginas
-   Escrita de resultados em arquivo `.csv`

------------------------------------------------------------------------

## Tecnologias utilizadas

-   Python 3
-   requests
-   BeautifulSoup (bs4)
-   concurrent.futures

------------------------------------------------------------------------

## Fonte dos dados

Os dados são coletados de um catálogo de filmes fictício hospedado em:

https://havokkmorands.github.io/movie-catalog/

O site foi desenvolvido com **Next.js** e exportado como HTML estático,
garantindo compatibilidade com scraping via `requests`.

------------------------------------------------------------------------

## Dados coletados

Para cada filme:

-   Nome
-   Data de lançamento
-   Nota
-   Sinopse

------------------------------------------------------------------------

## Multithreading

O projeto utiliza:

ThreadPoolExecutor

Para realizar requisições simultâneas das páginas de detalhes dos
filmes, reduzindo significativamente o tempo total de execução.

------------------------------------------------------------------------

## Estrutura do código

-   `main()` → inicia o processo
-   `extract_movies()` → coleta os links dos filmes
-   `extract_movie_details()` → coleta os dados individuais
-   uso de threads para paralelizar as requisições

------------------------------------------------------------------------

## Como executar

1.  Instale as dependências:

pip install requests beautifulsoup4

2.  Execute o script:

python multithreading.py

------------------------------------------------------------------------

## Saída

Os dados são salvos em:

movies.csv

------------------------------------------------------------------------

## Problemas resolvidos nesta versão

-   Correção na construção de URLs
-   Compatibilidade com rotas com `basePath`
-   Estabilidade do scraping em ambiente controlado
-   Eliminação de bloqueios externos (como os encontrados no IMDb)

------------------------------------------------------------------------

## Observações

-   O scraping funciona porque o site é **estático (HTML pronto)**\
-   Sites que dependem de JavaScript podem não funcionar com
    `requests + BeautifulSoup`

------------------------------------------------------------------------

## Possíveis melhorias

-   Adicionar retry automático para falhas
-   Implementar logs estruturados
-   Exportar dados em JSON além de CSV
-   Criar testes automatizados
-   Adicionar controle de rate limiting

------------------------------------------------------------------------

Projeto desenvolvido para fins educacionais, com foco em demonstrar
conceitos de scraping e concorrência em Python.
