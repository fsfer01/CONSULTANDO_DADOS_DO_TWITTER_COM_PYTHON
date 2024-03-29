![image](https://user-images.githubusercontent.com/78058494/166161865-829573ee-df20-4c84-8aac-828441c97327.png)


## RESULTADO DO PROJETO:
![CONSULTANDO_DADOS_DO_TWITTER_COM_PYTHON](https://user-images.githubusercontent.com/78058494/166161345-5d16caa0-9683-41cd-a2fa-f7c10e771b24.gif)


# PROJETO ETL / CONSULTANDO DADOS DO TWITTER COM PYTHON.

Meu primeiro projeto público para demonstrar meu conhecimento na área de dados. O Objetivo deste projeto é:

• Coletar os dados através de uma API. Neste caso, estou usando uma querie de busca, retornando todos os tweets com a palavra chave "DADOS".

• Realizar uma modelagem de dados, tratando os dados e transformando eles para facilitar os próximos passos.

• Dividindo um único DF em vários, para colocar em prática um relacionamento entre tabelas.

• Fazer ingestão em um banco.

# TECNOLOGIAS USADAS:

• PYTHON

• TWEEPY - LINK DA DOCUMENTAÇÃO: [Documentação TWEEPY](https://www.tweepy.org/)


# REQUISITOS:

Para conseguir rodar esse código localmente, será necessário instalar algumas bibliotecas! Execute os seguintes comandos abaixo:

```python
pip install tweepy
pip install pandas
pip install flatten-json
pip install SQLAlchemy
pip install PyMySQL
```

Após isso, é necessário também providenciar uma conta de desenvolvedor no Twitter para ter acesso a API. Segue link abaixo de como solicitar:



[Como solicitar uma API KEY do TWITTER](https://www.youtube.com/watch?v=p4fZLzKodCg).

# DESAFIOS:

## 1º: COLUNAS COMO UMA ESPÉCIE DE DICIONÁRIO, SEGUE IMAGEM ABAIXO:
![image](https://user-images.githubusercontent.com/78058494/165187939-8954dd36-0236-4071-a228-41a392cdf5c0.png)

As colunas entities  e user estão do modo mostrado no anexo acima. Para resolver esse problema, foi utilizado a biblioteca flatten_json para gerar outra tabela de dados através dessas colunas. Segue link da biblioteca e de sua documentação abaixo:

link: https://github.com/amirziai/flatten

![image](https://user-images.githubusercontent.com/78058494/165192557-cbc012c2-fb71-43fb-8a10-1764927b2de9.png)

## 2º: ADICIONANDO CHAVE PRIMÁRIA EM OUTRAS TABELAS PARA CRUZAMENTOS FUTUROS.
![image](https://user-images.githubusercontent.com/78058494/165651768-f78bb241-90eb-429c-b7e2-67d1438a0766.png)

## 3º: DATA EM FORMATO AMERICANO E EXTENSO.
![image](https://user-images.githubusercontent.com/78058494/166162213-46d48ad2-37db-4c78-9671-f8c5755466e9.png)

Código abaixo:

```python
#CONVERTENDO DATA NO DATAFRAME:
import locale; locale.setlocale(locale.LC_TIME, 'en_US.UTF-8'); 
dfTweetstabelao['created_at'] = pd.to_datetime(dfTweetstabelao['created_at'], format='%a %b %d %H:%M:%S %z %Y').dt.strftime('%Y-%m-%d %H:%M:%S')

#CONVERTENDO A COLUNA PARA DATA
dfTweetstabelao['created_at'] = pd.to_datetime(dfTweetstabelao['created_at']) # TRANFORMANDO COLUNA DE STRING PARA DATATIME BR
dfTweetstabelao['created_at'] = dfTweetstabelao['created_at']-timedelta(hours=3) #SUBTRAINDO 3 HORAS (CONVERTENDO UTC PARA BR)
```

# DIAGRAMA DE RELACIONAMENTO (CHAVE PRIMÁRIA):

![image](https://user-images.githubusercontent.com/78058494/166114197-cb2a864a-f73c-4100-94a4-024d990e0148.png)

# INSERINDO OS DADOS EM UM BANCO DE DADOS:

Neste caso, usei a biblioteca sqlalchemy para fazer a ingestão no Data Source. Existe outros métodos, usarei futuramente em outros projetos. Segue link da documentação abaixo:

Documentação: 

[Documentação](https://docs.sqlalchemy.org/en/14/).

Código abaixo:

```python
#REALIZANDO CONEXÃO COM O BANCO:

user = 'user_banco'
senha = 'senha_banco'
ipbancosql= 'HOST_BANCO'
porta = 'PORTA_BANCO'
nomebanco ='DADOS_DO_TWITTER'

engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+senha+'@'+ipbancosql+':'+porta+'/'+nomebanco+'') # CONEXÃO

print("CONEXÃO REALIZADA COM SUCESSO!")

#INSERIDO TABELÃO NO BANCO
basetabelao.to_sql(
    name = 'tabelao',
    con = engine,
    index = False,
    if_exists ='append'
)
```
# QUERY BÁSICA PARA TESTE:
![image](https://user-images.githubusercontent.com/78058494/166163089-af94e371-555d-4b0d-99a4-3f988e8c1dca.png)


```sql
SELECT tb.created_at AS DATA_CRIACAO_POST,
u.screen_name AS NAME_USER,
U.location AS LOCALIZACAO_USER,
u.followers_count AS QTD_SEGUIDORES,
u.friends_count AS QTD_DE_USERS_SEGUINDO,
tb.id AS ID_POST, tb.text AS TEXTO_POST

FROM dados_do_twitter.tabelao AS tb
LEFT JOIN dados_do_twitter.users AS u ON u.ID_POST_TABELAO = tb.id

ORDER BY tb.created_at ASC;
```

Data da ultima atualização: 01/05/2022.


