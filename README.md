# PROJETO ETL / CONSULTANDO DADOS DO TWITTER COM PYTHON.

Meu primeiro projeto para demonstrar meu conhecimento na área de dados. O Objetivo deste projeto é:

• Fazer requisições de uma certa quantidade de tweets com uma detarminada # ou palavra chave.

• Tratar o resultado, transformando em um data frame.

• dividindo o data frame em vários data frames, para isso, vamos usar como chave primária o nº do tweet (COMO UM PROTOCOLO OU ALGO DO TIPO).

• Fazer ingestão em um banco.

# TECNOLOGIAS USADAS:

# DESAFIOS:

# 1º: COLUNAS COM UMA ESPÉCIE DE DICIONÁRIO, SEGUE IMAGEM ABAIXO:
![image](https://user-images.githubusercontent.com/78058494/165187939-8954dd36-0236-4071-a228-41a392cdf5c0.png)

As colunas entities, metadata e user estão do modo mostrado no anexo acima. Para resolver esse problema, foi utilizado a biblioteca flatten_json. Segue link da biblioteca e de sua documentação abaixo:

link: https://github.com/amirziai/flatten

![image](https://user-images.githubusercontent.com/78058494/165190806-e4827a9a-e6dc-46bb-90d4-a6d6dec542c0.png)

# DIAGRAMA DE RELACIONAMENTO (CHAVE PRIMÁRIA):

![image](https://user-images.githubusercontent.com/78058494/164996180-08b9108a-9bcd-4008-b732-7809c9f2d26c.png)

