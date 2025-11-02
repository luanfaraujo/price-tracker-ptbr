# Rastreador Automático de Preços de E-Commerce
Um projeto independente desenvolvido para automatizar o monitoramento diário de preços de produtos dos seguintes sites de e-commerce: KaBuM!, Mercado Livre. Construído usando Python, SQLite e Agendador de Tarefas do Windows para eliminar a verificação manual de preços e possibilitar decisões de compra baseadas em dados.

_If you prefer the English version of this project, [click here](https://github.com/luanfaraujo/price-tracker-en)._

---

## Visão Geral
Este projeto demonstra como web scraping e automação de banco de dados podem resolver problemas do mundo real. O sistema coleta automaticamente dados de preços de produtos diariamente dos seguintes sites de e-commerce: KaBuM!, Mercado Livre, armazena em um banco de dados SQLite normalizado e mantém registros históricos para análise de tendências.

Atualmente suporta KaBuM! e Mercado Livre, com arquitetura projetada para ser extensível a varejistas adicionais. As técnicas centrais—web scraping, design de banco de dados e automação—se aplicam amplamente a cenários de inteligência competitiva, pesquisa de mercado e monitoramento de preços em diversos setores.

---

## Objetivos
- Automatizar a coleta diária de preços de produtos de sites de e-commerce.
- Armazenar dados históricos de preços em um banco de dados estruturado e consultável.
- Contornar sistemas de detecção de bots usando cabeçalhos HTTP apropriados.
- Permitir execução automatizada sem intervenção manual.
- Manter logs de auditoria para monitoramento da saúde do sistema e solução de problemas.
- Fornecer base para futuras análises de preços e suporte a múltiplos varejistas.

---

## Processo

### 1. Desenvolvimento do Web Scraping
- Análise das estruturas HTML dos sites (KaBuM! e Mercado Livre) para localizar dados de preços.
- Implementação de cabeçalhos HTTP para imitar requisições de navegador e contornar detecção de bots.
- Uso de expressões regulares específicas por site para extrair preços de dados JSON incorporados no HTML.
- Construção de tratamento de erros para requisições falhas e padrões de dados ausentes.

### 2. Design do Banco de Dados
- Criação de esquema normalizado com tabelas separadas para produtos e histórico de preços.
- Implementação de relacionamentos de chave estrangeira para vincular preços históricos aos produtos.
- Uso de chaves primárias AUTOINCREMENT para gerenciamento automático de IDs.
- Aplicação de consultas parametrizadas para prevenir vulnerabilidades de injeção SQL.

### 3. Implementação da Automação
- Configuração do Agendador de Tarefas do Windows para execução diária em horários especificados.
- Habilitação de "executar após início perdido" para lidar com tempo de inatividade do sistema.
- Implementação de sistema de logs para rastrear sucesso/falha de execução.
- Adição de registro de timestamp para cada evento de coleta de preços.

### 4. Qualidade de Código e Segurança
- Refatoração de consultas SQL com f-strings para consultas parametrizadas.
- Implementação de tratamento abrangente de erros com blocos try-except.
- Adição de logs em múltiplos níveis (info, warning, error) para diferentes cenários.
- Estruturação do código para manutenibilidade e melhorias futuras.

---

## Resultados e Insights
- Coleta diária de preços de dois grandes sites de e-commerce brasileiros automatizada com sucesso, eliminando ~15 minutos de trabalho manual por dia.
- Banco de dados histórico construído, possibilitando análise de tendências de preços e identificação do momento ideal de compra.
- Execução confiável alcançada através de configuração adequada de automação e recuperação de erros.
- Base de dados escalável criada, suportando múltiplos produtos.

---

## Ferramentas e Habilidades Demonstradas
- **Web Scraping:** requests, correspondência de padrões regex, técnicas de contorno de anti-bot
- **Gerenciamento de Banco de Dados:** SQLite, design de esquema, normalização, chaves estrangeiras, consultas parametrizadas
- **Automação:** Agendador de Tarefas do Windows, logging, tratamento de erros, execução programada
- **Segurança de Dados:** Prevenção de injeção SQL, tratamento adequado de erros, validação de entrada
- **Engenharia de Software:** Preparação para controle de versão, documentação de código, melhoria iterativa

---

## Varejistas Suportados
- **KaBuM!**: Rastreamento completo de preços (original, à vista, parcelado)
- **Mercado Livre**: Rastreamento de preços (à vista e parcelado)

Cada varejista requer:
- Padrões regex personalizados para extração de preços
- Cabeçalhos HTTP específicos por site
- Tratamento de estrutura de URL única

---

## Limitações Atuais e Melhorias Futuras
**Escopo Atual:**
- Atualmente suporta KaBuM! e Mercado Livre
- Padrões regex específicos necessários para cada varejista
- Diferentes formatos de URL entre varejistas

**Melhorias Planejadas:**
- Expandir para varejistas adicionais
- Alertas por e-mail de queda de preço quando produtos atingem valores-alvo
- Dashboard de visualização de dados mostrando tendências de preços ao longo do tempo
- Comparação entre varejistas para o mesmo produto
- Funcionalidade de exportação para CSV/Excel para análise externa
- Migração para GitHub Actions para execução baseada em nuvem
- Análise estatística e recursos de previsão de preços

---

## Notas Técnicas
**Esquema do Banco de Dados:**
- Tabela `products`: Armazena metadados de produtos (nome, URL, varejista)
- Tabela `price_history`: Armazena todos os registros de preços com timestamps e referências de chave estrangeira

**Pontos-Chave de Aprendizado:**
- Compreensão da diferença entre conteúdo renderizado em HTML e JavaScript
- Importância de cabeçalhos HTTP adequados em web scraping
- Diferentes sites exigem diferentes abordagens de parsing (estruturas HTML/JSON específicas por site)
- Princípios de normalização de banco de dados e seus benefícios práticos
- Consultas parametrizadas vs. interpolação de strings para SQL
- Confiabilidade da automação e tratamento de execuções perdidas
