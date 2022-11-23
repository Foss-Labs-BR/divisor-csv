# Divisor CSV

Este projeto é um simples divisor CSV - Comma Separated Values, Valores Separados por Vírgula, tipo de arquivo simples que pode ser aberto como planilha.

Ele pode ser usado para diversas finalidades. A finalidade principal é subdividir os arquivos CSV para que possam ser organizados para outras tarefas de preenchimento e importação nos diversos bancos de dados existentes.

O Divisor tem 2 métodos de divisão: por `linhas` ou  `partes`:

* **Divisão por linhas**: o divisor irá pegar o arquivo `.csv` e ira dividir por linhas. ```Exemplo: arquivo .csv de 10k de linhas -> divisão com numero de linhas: 1k -> divisão em 10 arquivos com 1k de linhas cada.```

* **Divisão por partes**: o divisor irá pegar o arquivo `.csv` e irá subdividir pelo número de partes especificadas. ```Exemplo: arquivo .csv de 10k -> divisão em 2 partes -> divisão em 2 arquivos cada um com 5k de linhas.```

<sub>* Os valores de cada divisão, seja número de linhas ou partes, podem ser especificados no arquivo `.env`.</sub>

## Requerimentos

* **Docker Engine**: versão 20.10.18 ou mais recente.
* **Docker Compose**: versão 2.10.2 ou mais recente.

## Scripts

Os scripts estão na pasta `scripts/` e pode ser rodados a partir da pasta do projeto dando primeiro a permissão via `chmod +x ./scripts/*.sh`. Após dada a devida permissão, rode-os usando a sintaxe `./scripts/[nome_script].sh`.

## Entrada e Saída

### Entrada

Coloque os seus arquivos `.csv` na pasta `in/`, em forma de `árvores de diretórios` ou de `arquivos simples`, basta colocar os arquivos `.csv` na pasta. Este divisor tem suporte à divisão de múltiplos arquivos de forma simultânea.

### Saída

Após rodar o divisor, será gerado várias subdivisões do arquivo na pasta `splits-[unix_timestamp]`

## Como rodar o Divisor CSV

1) Copie o arquivo `.env.sample` e renomeie-o para `.env` e edite ele conforme preferir. Caso contrário, o script seguinte gerará um automaticamente com as configurações padrão existentes no `.env.sample`. Após a geração do `.env`, o divisor poderá ser personalizado conforme a necessidade do uso.

2) Após dada a permissão adequada aos scripts, rode o seguinte script:

```
$ ./scripts/up.sh
```

---

Há também um script extra para apagar o container se ocorrer um problema de execução no passo 2:

```
$ ./scripts/down.sh
```

Este script irá rodar o `docker compose down`e apagar todas as configurações do compose seguidas no `docker-compose.yml`.

## Depuração via VS Code:

Há presentes nesse repositório a configuração necessária para realizar a depuração do script caso necessário.

Para realizar a depuração do script `main.py` dentro do container Docker, descomente a linha que está presente no arquivo `Dockerfile`:

```Dockerfile
#CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client main.py
```

E comente a linha principal:

```
CMD python main.py
```

Após realizar as alterações no `Dockerfile`, rode o script como documentado na seção `Como rodar o Divisor CSV` logo acima.

O script só irá rodar depois que o cliente de depuração do **VS Code** for inicializado corretamente. Veja este vídeo de exemplo no **YouTube** demostrando seu uso:

https://www.youtube.com/watch?v=ywfsLKRLmf4

## Outros scripts importantes

* `scripts/clear.sh` - limpa a pasta `out/` com os arquivos subdivididos.

* `scripts/gen-csv-sample.sh` - gera um arquivo `sample.csv` com 3M de linhas na pasta `/in`, recurso utilizado para testar a carga do divisor na hora de carregar o arquivo para a memória.

## Licença

[GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)