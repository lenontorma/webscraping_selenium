# 1. Fontes de Dados

O projeto extrai informações do site da **Casarão Imóveis**, focando nos imóveis disponíveis para aluguel em **Pelotas/RS**.

## 🌐 Site alvo

- **URL principal**:  
  [https://casaraoimoveis.com.br/imoveis/alugueis/pelotas/todos-os-tipos/](https://casaraoimoveis.com.br/imoveis/alugueis/pelotas/todos-os-tipos/)

## 🔍 Estrutura da Página

A listagem de imóveis está em um container com ID `#imoveis`, onde cada card representa um imóvel.

### Exemplos de elementos capturados:

- **Endereço**:  
  Extraído do seletor `p.endereco` em cada página individual do imóvel.
  
- **Características** (aluguel, condomínio, IPTU, total etc):  
  Coletadas a partir de um container com várias `div.row`, onde cada linha tem:
  - Nome (ex: "Aluguel", "IPTU")
  - Valor correspondente (ex: "R$ 4.100,00")

- **Tipo de imóvel** (casa, apartamento, loja, etc...):
  - Coletado a partir da URL do card.

## 🧭 Estratégia de navegação

1. A página principal exige **scroll infinito** para carregar todos os imóveis.
![Demonstração do scroll infinito](docs/assets/scroll-infinito.png)
2. Cada imóvel possui um link para sua **página individual**.
3. As informações completas são acessadas apenas ao abrir cada página de imóvel.

## 🧪 Considerações

- Alguns cards podem ser **propagandas** e não possuem link (`<a>`), sendo ignorados.
- Alguns campos, como **"Condomínio"** ou **"IPTU"**, podem conter `""---"` quando ausentes.
- Há alguns endereços que o logradouro vem com abreviados como "R"(rua), "Prç"(praça), "Av"(avenida). 
- No momento do Extract, a chave `"TOTAL"` pode aparecer duplicada com variações como:
  - `"TOTAL:\nR$ 4.100,00"`
  - `"TOTAL:"`

Essas inconsistências são tratadas na etapa de transformação de dados.
