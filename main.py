import pandas as pd #Importa a biblioteca 'pandas' para manipulação de dados

#funções para leitura dos arquivos
#essas funções utilizam o 'pandas' para ler os arquivos e retornam DataFrames, que são estruturas de dados que facilitam a manipulação de tabelas
def ler_nome_basics():
    return pd.read_csv('name.basics.tsv', sep='\t')

def ler_title_akas():
    return pd.read_csv('title.akas.tsv', sep='\t')

def ler_title_basics():
    return pd.read_csv('title.basics.tsv', sep='\t', dtype={'startYear': 'str', 'endYear': 'str'}, low_memory=False)

def ler_title_crew():
    return pd.read_csv('title.crew.tsv', sep='\t')

def ler_title_episode():
    return pd.read_csv('title.episode.tsv', sep='\t')

def ler_title_principals():
    return pd.read_csv('title.principals.tsv', sep='\t')

def ler_title_ratings():
    return pd.read_csv('title.ratings.tsv', sep='\t')

#menu
def menu_interativo():
    while True:
        print("\nMenu de Consultas:")
        print("1. Quais são as categorias de filmes mais comuns no IMDB?")
        print("2. Qual o número de títulos por gênero?")
        print("3. Qual a mediana de avaliação dos filmes Por Gênero?")
        print("4. Qual a mediana de avaliação dos filmes em relação ao ano de estreia?")
        print("5. Qual o número de filmes avaliados por gênero em relação ao ano de estreia?")
        print("6. Qual o filme com maior tempo de duração?")
        print("7. Qual a relação entre duração e gênero?")
        print("8. Qual é a relação entre o orçamento dos filmes e sua avaliação? (Não implementado)") #não possuí dados de orçamento associados!
        print("9. Qual o número de filmes produzidos por país?")
        print("10. Quais são os top 15 melhores filmes e 15 piores filmes?")
        print("11. Quais são os gêneros mais populares em cada década?")
        print("12. Faça uma análise dos filmes e mostre para o investidor uma análise gerencial dos filmes no dataset.")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            categorias_comuns()
        elif escolha == '2':
            titulos_por_genero()
        elif escolha == '3':
            mediana_avaliacao_por_genero()
        elif escolha == '4':
            mediana_avaliacao_por_ano()
        elif escolha == '5':
            filmes_avaliados_por_genero_e_ano()
        elif escolha == '6':
            filme_maior_duracao()
        elif escolha == '7':
            relacao_duracao_genero()
        elif escolha == '8':
            print("Opção 8 não implementada.")
        elif escolha == '9':
            filmes_por_pais()
        elif escolha == '10':
            top_e_piores_filmes()
        elif escolha == '11':
            generos_populares_por_decada()
        elif escolha == '12':
            analise_gerencial()
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Escolha novamente.")

#1 - nesta função, primeiro lemos os dados dos títulos de filmes. 
#depois, filtramos apenas os filmes e contamos quantas vezes cada gênero aparece. 
#por fim, exibimos os 10 gêneros mais comuns.
def categorias_comuns():
    basics_df = ler_title_basics() #lê o arquivo especificado
    filmes = basics_df[basics_df['titleType'] == 'movie'] #filtra apenas os filmes
    categorias_count = filmes['genres'].str.split(',').explode().value_counts() #faz a contagem dos generos mais comuns
    categorias_df = categorias_count.reset_index() #reseta o índice do DataFrame
    categorias_df.columns = ['Categoria', 'Contagem'] #renomeia as colunas do DataFrame
    print("Categorias de filmes mais comuns no IMDB:")
    print(categorias_df.head(10)) #exibe 10 resultados

#2 - esta função conta quantos títulos de filmes existem para cada gênero no conjunto de dados do IMDB.
#filtramos apenas os filmes dentro desse conjunto de dados.
#utilizamos a coluna genres, que pode conter múltiplos gêneros separados por vírgula. 
#dividimos esses gêneros e contamos quantas vezes cada um aparece.
def titulos_por_genero():
    basics_df = ler_title_basics()
    filmes = basics_df[basics_df['titleType'] == 'movie'] #filtra apenas os filmes
    generos_count = filmes['genres'].str.split(',').explode().value_counts() #faz a contagem dos titulos por gênero
    generos_df = generos_count.reset_index() #reseta o índice do DataFrame
    generos_df.columns = ['Gênero', 'Contagem'] #renomeia as colunas do DataFrame
    print("Número de títulos por gênero:")
    print(generos_df)

#3 - esta função calcula a mediana das avaliações dos filmes para cada gênero no conjunto de dados do IMDB.
#combinamos esses dados para ter informações completas sobre avaliações e gêneros de filmes.
#cada filme pode ter múltiplos gêneros listados. Usamos assign() e explode() para separar esses gêneros em linhas individuais.
#calculamos a mediana das avaliações (averageRating) agrupadas por gênero, ordenando do maior para o menor.
def mediana_avaliacao_por_genero():
    ratings_df = ler_title_ratings()
    basics_df = ler_title_basics()
    filmes_com_avaliacao = pd.merge(ratings_df, basics_df, on='tconst', how='inner') #combina os arquivos para análise
    filmes_com_avaliacao = filmes_com_avaliacao.assign(genres=filmes_com_avaliacao['genres'].str.split(',')).explode('genres') #divide os generos
    mediana_avaliacao = filmes_com_avaliacao.groupby('genres')['averageRating'].median().sort_values(ascending=False) #calcula a mediana
    mediana_df = mediana_avaliacao.reset_index()
    mediana_df.columns = ['Gênero', 'Mediana de Avaliação']
    print("Mediana de avaliação dos filmes por gênero:")
    print(mediana_df)

#4 - esta função calcula a mediana das avaliações dos filmes para cada ano de estreia no conjunto de dados do IMDB.
#combinamos esses dados para ter informações completas sobre avaliações e anos de estreia dos filmes.
#calculamos a mediana das avaliações (averageRating) agrupadas por ano de estreia dos filmes.
#ordenamos os resultados por ano de estreia e exibimos a mediana de avaliação dos filmes por ano de estreia de forma organizada.
def mediana_avaliacao_por_ano():
    ratings_df = ler_title_ratings()
    basics_df = ler_title_basics()
    filmes_com_avaliacao = pd.merge(ratings_df, basics_df, on='tconst', how='inner') #combina os arquivos para análise
    mediana_avaliacao_ano = filmes_com_avaliacao.groupby('startYear')['averageRating'].median().reset_index() #calcula a mediana de avaliação por ano de estreia
    mediana_avaliacao_ano.columns = ['Ano de Estreia', 'Mediana de Avaliação'] #cria um DataFrame
    mediana_avaliacao_ano = mediana_avaliacao_ano.sort_values(by='Ano de Estreia') #ordena pelos anos
    print("Mediana de avaliação dos filmes por ano de estreia:")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None): #exibe todos os resultados
        print(mediana_avaliacao_ano)

#5 - esta função calcula quantos filmes foram avaliados para cada combinação de gênero e ano de estreia no conjunto de dados do IMDB.
#agrupamos os filmes por gênero e ano de estreia e contamos quantos filmes foram avaliados em cada combinação.
def filmes_avaliados_por_genero_e_ano():
    ratings_df = ler_title_ratings()
    basics_df = ler_title_basics()
    filmes_com_avaliacao = pd.merge(ratings_df, basics_df, on='tconst', how='inner') #combinando arquivos
    filmes_por_genero_ano = filmes_com_avaliacao.groupby(['genres', 'startYear']).size() #agrupando por genero e ano de estreia, e contando
    filmes_genero_ano_df = filmes_por_genero_ano.reset_index()
    filmes_genero_ano_df.columns = ['Gênero', 'Ano de Estreia', 'Contagem'] #criando DataFrame
    print("Número de filmes avaliados por gênero e ano de estreia:")
    print(filmes_genero_ano_df)

#6 - esta função identifica o filme com o maior tempo de duração no conjunto de dados do IMDB.
#convertemos a coluna runtimeMinutes para numérica, ignorando valores inválidos (errors='coerce').
#encontramos o índice do filme com o maior tempo de duração usando idxmax().
#obtemos o título e a duração do filme com maior tempo de duração usando loc[].
def filme_maior_duracao():
    basics_df = ler_title_basics()
    filmes = basics_df[basics_df['titleType'] == 'movie'].copy() #filtrar filmes válidos
    filmes['runtimeMinutes'] = pd.to_numeric(filmes['runtimeMinutes'], errors='coerce') #filtrar valores
    idx_maior_duracao = filmes['runtimeMinutes'].idxmax() #encontrar o maior tempo de duração
    titulo = filmes.loc[idx_maior_duracao, 'primaryTitle'] #selecionar o titulo
    duracao = filmes.loc[idx_maior_duracao, 'runtimeMinutes'] #selecionar o tempo
    print(f"Filme com maior tempo de duração:\nTítulo: {titulo}\nDuração: {duracao} minutos")

#7 - esta função calcula a duração média dos filmes para cada gênero no conjunto de dados do IMDB.
#convertemos a coluna runtimeMinutes para numérica, ignorando valores inválidos (errors='coerce').
#calculamos a duração média dos filmes para cada gênero usando groupby() e mean().
def relacao_duracao_genero():
    basics_df = ler_title_basics()
    filmes = basics_df[basics_df['titleType'] == 'movie'].copy() #filtra os filmes
    filmes['runtimeMinutes'] = pd.to_numeric(filmes['runtimeMinutes'], errors='coerce') #converte a coluna de duração para numérica
    duracao_por_genero = filmes.groupby('genres')['runtimeMinutes'].mean().sort_values(ascending=False) #calcula a duração média por gênero e ordena do maior para o menor
    duracao_genero_df = duracao_por_genero.reset_index()
    duracao_genero_df.columns = ['Gênero', 'Duração Média']
    print("Relação entre duração e gênero:")
    print(duracao_genero_df)

#9 - esta função calcula quantos filmes foram produzidos por país ou região de acordo com os dados disponíveis no IMDB.
#combinamos esses dados para ter informações completas sobre os títulos de filmes e suas regiões.
#selecionamos apenas os filmes dentro desses dados combinados.
#contamos quantos filmes estão associados a cada país ou região usando value_counts().
def filmes_por_pais():
    akas_df = ler_title_akas()
    basics_df = ler_title_basics()
    merged_df = pd.merge(akas_df, basics_df, left_on='titleId', right_on='tconst', how='inner') #comparando as informações dentro dos arquivos
    filmes = merged_df[merged_df['titleType'] == 'movie'] #filtrando filmes válidos
    filmes_por_pais = filmes['region'].value_counts() #contar filmes por região
    print("Quantidade de filmes por país/região:")
    print(filmes_por_pais.to_string()) #organizando exibição

#10 - esta função identifica os 15 melhores e os 15 piores filmes com base na média de avaliações dos usuários no IMDB.
#ordenamos os filmes com base na média de avaliação (averageRating), tanto do maior para o menor para encontrar os melhores, quanto do menor para o maior para encontrar os piores.
#selecionamos os top 15 melhores filmes e os 15 piores com base na média de avaliação.
def top_e_piores_filmes():
    ratings_df = ler_title_ratings()
    basics_df = ler_title_basics()
    filmes_com_avaliacao = pd.merge(ratings_df, basics_df, on='tconst', how='inner') #combinando dados
    top_filmes = filmes_com_avaliacao.sort_values(by='averageRating', ascending=False).head(15) #ordena os filmes pela média de avaliação, do maior para o menor, e seleciona os 15 melhores
    piores_filmes = filmes_com_avaliacao.sort_values(by='averageRating').head(15) #ordena os filmes pela média de avaliação, do maior para o menor, e seleciona os 15 piores
    print("Top 15 melhores filmes:")
    print(top_filmes[['primaryTitle', 'averageRating']])
    print("\n15 piores filmes:")
    print(piores_filmes[['primaryTitle', 'averageRating']])

#11 - esta função identifica os gêneros mais populares de filmes em cada década com base nos dados do IMDB.
#convertemos a coluna startYear para numérica, ignorando valores inválidos (errors='coerce').
#dividimos os anos de estreia dos filmes em décadas usando pd.cut().
#para cada década, identificamos o gênero mais popular entre os filmes.
#por fim, criamos um DataFrame com os resultados para exibir de forma organizada os gêneros mais populares em cada década.
def generos_populares_por_decada():
    basics_df = ler_title_basics()
    filmes = basics_df[basics_df['titleType'] == 'movie'].copy() #filtrar filmes
    filmes.loc[:, 'startYear'] = pd.to_numeric(filmes['startYear'], errors='coerce') #conversão de colunas
    decadas = pd.cut(filmes['startYear'], bins=range(1900, 2030, 10), right=False) #dividindo anos em décadas
    generos_populares = filmes.groupby(decadas, observed=False)['genres'].apply(lambda x: x.str.split(',').explode().mode()[0] if not x.empty else None) #agrupar decadas e encontrar o genero mais popular
    generos_populares_df = generos_populares.reset_index()
    generos_populares_df.columns = ['Década', 'Gênero Popular'] #criação de dataFrame
    print("Gêneros mais populares em cada década:")
    print(generos_populares_df)

#12 - esta função realiza uma análise gerencial dos filmes, mostrando a média de avaliação por tipo de título.
#combinamos esses dados para ter informações completas sobre avaliações e detalhes dos filmes.
#calculamos a média de avaliação (averageRating) agrupada por tipo de título usando groupby() e mean().
def analise_gerencial():
    basics_df = ler_title_basics()
    ratings_df = ler_title_ratings()
    filmes_com_avaliacao = pd.merge(ratings_df, basics_df, on='tconst', how='inner') #combinando dados
    media_avaliacao_por_tipo = filmes_com_avaliacao.groupby('titleType')['averageRating'].mean() #calcula média de avaliação por título
    media_avaliacao_df = media_avaliacao_por_tipo.reset_index()
    media_avaliacao_df.columns = ['Tipo de Título', 'Média de Avaliação'] #DataFrame para exibir os resultados
    print("Análise Gerencial - Média de Avaliação por Tipo de Filme:")
    print(media_avaliacao_df)

#executar menu
menu_interativo()