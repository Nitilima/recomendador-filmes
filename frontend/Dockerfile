# Usa uma imagem base do Node.js
FROM node:16 AS build

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY package.json package-lock.json ./

# Instala as dependências
RUN npm install

# Copia o restante do código
COPY . .

# Constrói o projeto
RUN npm run build

# Usa uma imagem leve para servir o frontend
FROM nginx:alpine

# Copia os arquivos de build para o servidor Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Expõe a porta 80
EXPOSE 80

# Inicia o servidor Nginx
CMD ["nginx", "-g", "daemon off;"]