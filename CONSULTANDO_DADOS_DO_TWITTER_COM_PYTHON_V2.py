#!/usr/bin/env python
# coding: utf-8

# In[7]:


#IMPORTANDO BIBLIOTECAS
import tweepy as tw
import pandas as pd
from flatten_json import flatten
from datetime import timedelta,datetime
import sqlalchemy


# In[8]:


#CHAVES DE ACESSO
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#AUTENTICAÇÃO
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)
print("CONEXÃO REALIZADA COM SUCESSO!")
public_tweets = api.home_timeline()


# In[9]:


querie = "DADOS"  + " -filter:retweets"  # BUSCANDO A PALAVRA DADOS E DESCONSIDERANDO OS RETWEETS


# In[10]:


#QUANTIDADE DE REQUISIÇÕES:
cursor_tweets = tw.Cursor(api.search_tweets,q=querie).items(50) #QUANTIDADE DE RESULTADOS / REQUISIÇÕES


# In[11]:


#VENDO OS tweet
for tweet in public_tweets:
    print(tweet.text)


# In[12]:


#CRIANDO UM DICIONÁRIO
twkeys = tweet._json.keys() #CHAMANDO FUNÇÃO DA API
basetwitter ={} #CRIANDO UM DICIONÁRIO VAZIO
basetwitter =  basetwitter.fromkeys(twkeys) #APLICANDO FUNÇÃO DA API NO DICIONÁRIO


# In[13]:


#USANDO COMANDO cursor_tweets OBS: COMANDO DA PRÓPRIA API DE ACORDO COM DOCUMENTAÇÕES.
for tweet in cursor_tweets:
    for key in basetwitter.keys():
        try:
            twvalue = tweet._json[key]
            basetwitter[key].append(twvalue)
        except KeyError:
            twvalue = ""
            if(basetwitter[key] is None):
                basetwitter[key] = [twvalue]
            else:
                basetwitter[key].append(twvalue)
        except:
            basetwitter[key] = [twvalue]


# In[14]:


# TRANSFORMAR EM UM DATA FRAME:
tabelao_original = pd.DataFrame.from_dict(basetwitter) # TEM HORA QUE PARA DE FUNCIONAR


# In[15]:


#CRIANDO UMA CÓPIA DO TABELÃO PARA MODELAGEM DE DADOS:
dfTweetstabelao = tabelao_original


# In[16]:


#TRATANDO / TRANSFORMANDO O TABELÃO:

#CONVERTENDO DATA NO DATAFRAME:
import locale; locale.setlocale(locale.LC_TIME, 'en_US.UTF-8'); 
dfTweetstabelao['created_at'] = pd.to_datetime(dfTweetstabelao['created_at'], format='%a %b %d %H:%M:%S %z %Y').dt.strftime('%Y-%m-%d %H:%M:%S')

#CONVERTENDO A COLUNA PARA DATA
dfTweetstabelao['created_at'] = pd.to_datetime(dfTweetstabelao['created_at']) # TRANFORMANDO COLUNA DE STRING PARA DATATIME BR
dfTweetstabelao['created_at'] = dfTweetstabelao['created_at']-timedelta(hours=3) #SUBTRAINDO 3 HORAS (CONVERTENDO UTC PARA BR)

# TRANSFORMANDO NÚMEROS EM INTEIROS, E DEPOIS PARA STRING
dfTweetstabelao["id"] = dfTweetstabelao["id"].apply(int)
dfTweetstabelao["id_str"] = dfTweetstabelao["id_str"].apply(str)
dfTweetstabelao.drop('id_str', axis=1, inplace=True)


# In[17]:


#TABELA DE USUÁRIOS SENDO EXTRAÍDA DO TABELÃO ORIGINAL.
users = (flatten(u) for u in tabelao_original['user'])
tabelauser = pd.DataFrame(users)

#CONVERTENDO DATA NO DATAFRAME:
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8'); 
tabelauser['created_at'] = pd.to_datetime(tabelauser['created_at'], format='%a %b %d %H:%M:%S %z %Y').dt.strftime('%Y-%m-%d %H:%M:%S')

#CONVERTENDO A COLUNA PARA DATA
tabelauser['created_at'] = pd.to_datetime(tabelauser['created_at']) # TRANFORMANDO COLUNA DE STRING PARA DATATIME BR
tabelauser['created_at'] = tabelauser['created_at']-timedelta(hours=3) #SUBTRAINDO 3 HORAS (CONVERTENDO UTC PARA BR)
tabelauser.insert(0, 'ID_POST_TABELAO', dfTweetstabelao["id"]) #INSERINDO CHAVE PRIMÁRIA DO TABELÃO

#REMOVENDO COLUNA USER DO TABELÃO, JÁ QUE A MESMA GEROU RESULTOU EM OUTRA TABELA.
dfTweetstabelao.drop('user', axis=1, inplace=True)

#REMOVENDO COLUNAS DUPLICADAS:
del tabelauser['id_str']


# In[18]:


#TABELA DE entities SENDO EXTRAÍDO DO TABELÃO ORIGINAL.
entities = (flatten(e) for e in dfTweetstabelao['entities'])
tabelaentities = pd.DataFrame(entities)
tabelaentities.insert(0, 'ID_POST_TABELAO', dfTweetstabelao["id"]) #INSERINDO CHAVE PRIMÁRIA DO TABELÃO
#REMOVENDO COLUNA entities DO TABELÃO, JÁ QUE A MESMA GEROU RESULTOU EM OUTRA TABELA.
dfTweetstabelao.drop('entities', axis=1, inplace=True)


# In[19]:


#EXPORTANDO
tabelauser.to_csv(r'C:/Users/WORKING USER/Desktop/APITWITTER/user.csv',sep=';',encoding="UTF8" ,index=False)
#EXPORTANDO
tabelaentities.to_csv(r'C:/Users/WORKING USER/Desktop/APITWITTER/tabelaentities.csv',sep=';',encoding="UTF8" ,index=False)
#EXPORTANDO
dfTweetstabelao.to_csv(r'C:/Users/WORKING USER/Desktop/APITWITTER/tabelao.csv',sep=';',encoding="UTF8" ,index=False)


# In[20]:


#LENDO E FAZENDO INGESTÃO NO BANCO MYSQL
basetabelao = pd.read_csv(r'C:/Users/WORKING USER/Desktop/APITWITTER/tabelao.csv',sep=';')
baseuser = pd.read_csv(r'C:/Users/WORKING USER/Desktop/APITWITTER/user.csv',sep=';')
baseentities = pd.read_csv(r'C:/Users/WORKING USER/Desktop/APITWITTER/tabelaentities.csv',sep=';')


# In[21]:


#REALIZANDO CONEXÃO COM O BANCO:

user = 'user_banco'
senha = 'senha_banco'
ipbancosql= 'HOST_BANCO'
porta = 'PORTA_BANCO'
nomebanco ='DADOS_DO_TWITTER'

engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+senha+'@'+ipbancosql+':'+porta+'/'+nomebanco+'') # CONEXÃO

print("CONEXÃO REALIZADA COM SUCESSO!")


# In[22]:


#INSERIDO TABELÃO NO BANCO
basetabelao.to_sql(
    name = 'tabelao',
    con = engine,
    index = False,
    if_exists ='append'
)


# In[23]:


#INSERIDO TABELA USER NO BANCO
baseuser.to_sql(
    name = 'users',
    con = engine,
    index = False,
    if_exists ='append'
)


# In[24]:


#INSERIDO TABELA ENTITIES USER NO BANCO
baseentities.to_sql(
    name = 'entities',
    con = engine,
    index = False,
    if_exists ='append'
)


# In[25]:


print('INGESTÃO CONCLUÍDA COM SUCESSO!')

