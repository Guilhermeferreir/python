# XlsxWriter

## 📊 Descrição

**XlsxWriter** é um projeto de exemplo e referência para trabalhar com a biblioteca **XlsxWriter** em Python. XlsxWriter é uma ferramenta poderosa para criar arquivos Excel (.xlsx) do zero, permitindo criar planilhas, formatar células, adicionar gráficos e muito mais - tudo programaticamente, sem precisar do Excel instalado.

## 🎯 Funcionalidades

- **Criar Arquivos Excel**: Gera arquivos .xlsx sem dependências do MS Office
- **Formatação de Células**: Cores, fontes, bordas, alinhamento
- **Fórmulas**: Suporte completo para fórmulas Excel
- **Gráficos**: Cria gráficos diversos (barras, linhas, pizza, etc)
- **Múltiplas Abas**: Adiciona várias worksheets em um workbook
- **Validação de Dados**: Implementa validação e restrições
- **Imagens**: Insere imagens em células
- **Estilos Avançados**: Condicionamento, merged cells, etc

## 📁 Estrutura do Projeto

```
xlsxwriter/
└── example.py              # Exemplo básico
```

## 📋 Requisitos

- Python 3.6+
- XlsxWriter

### Instalação de Dependências

```bash
pip install xlsxwriter
```

## 🚀 Como Usar

### 1. Exemplo Básico

Execute o arquivo de exemplo:

```bash
cd xlsxwriter
python example.py
```

Isso criará um arquivo `expense.xlsx` com dados de despesas.

### 2. Estrutura do Código

```python
import xlsxwriter

# 1. Criar workbook e worksheet
workbook = xlsxwriter.Workbook('expense.xlsx')
worksheet = workbook.add_worksheet()

# 2. Dados
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)

# 3. Escrever dados
row = 0
col = 0
for item, cost in expenses:
    worksheet.write(row, col, item)
    worksheet.write(row, col + 1, cost)
    row += 1

# 4. Adicionar total com fórmula
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')

# 5. Fechar
workbook.close()
```

## 📝 Conceitos Principais

### Workbook
Um arquivo Excel completo:
```python
workbook = xlsxwriter.Workbook('arquivo.xlsx')
```

### Worksheet
Uma aba dentro do workbook:
```python
worksheet = workbook.add_worksheet('Nome da Aba')
```

### Escrita de Dados
```python
worksheet.write(row, col, valor)
worksheet.write(0, 0, 'Texto')
worksheet.write(0, 1, 123)
worksheet.write(0, 2, 45.67)
worksheet.write(0, 3, '=A1+A2')
```

### Formatos
```python
# Criar formato
bold = workbook.add_format({'bold': True})
currency = workbook.add_format({'num_format': '$#,##0.00'})

# Usar formato
worksheet.write(0, 0, 'Total', bold)
worksheet.write(1, 0, 1000, currency)
```

## 💡 Exemplos Prácticos

### 1. Planilha de Relatório

```python
import xlsxwriter

workbook = xlsxwriter.Workbook('relatorio.xlsx')
worksheet = workbook.add_worksheet('Vendas')

# Formatos
header = workbook.add_format({
    'bold': True,
    'bg_color': '#4472C4',
    'font_color': 'white',
    'border': 1
})

money = workbook.add_format({
    'num_format': '$#,##0.00',
    'border': 1
})

# Headers
worksheet.write('A1', 'Produto', header)
worksheet.write('B1', 'Quantidade', header)
worksheet.write('C1', 'Preço', header)
worksheet.write('D1', 'Total', header)

# Dados
produtos = [
    ('Produto A', 10, 100),
    ('Produto B', 5, 50),
    ('Produto C', 20, 75),
]

row = 1
for produto, qtd, preco in produtos:
    worksheet.write(row, 0, produto)
    worksheet.write(row, 1, qtd)
    worksheet.write(row, 2, preco, money)
    worksheet.write(row, 3, f'=B{row+1}*C{row+1}', money)
    row += 1

# Ajustar largura das colunas
worksheet.set_column('A:D', 15)

workbook.close()
```

### 2. Planilha com Gráfico

```python
import xlsxwriter

workbook = xlsxwriter.Workbook('vendas_grafico.xlsx')
worksheet = workbook.add_worksheet()

# Dados
dados = [
    ['Mês', 'Vendas', 'Custos'],
    ['Janeiro', 5000, 2000],
    ['Fevereiro', 6000, 2500],
    ['Março', 5500, 2200],
    ['Abril', 7000, 3000],
]

# Escrever dados
for row_num, row_data in enumerate(dados):
    for col_num, cell_data in enumerate(row_data):
        worksheet.write(row_num, col_num, cell_data)

# Criar gráfico
chart = workbook.add_chart({'type': 'column'})

# Adicionar séries ao gráfico
chart.add_series({
    'name': '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$5',
    'values': '=Sheet1!$B$2:$B$5',
})

chart.add_series({
    'name': '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$5',
    'values': '=Sheet1!$C$2:$C$5',
})

# Configurar gráfico
chart.set_title({'name': 'Vendas vs Custos'})
chart.set_x_axis({'name': 'Mês'})
chart.set_y_axis({'name': 'Valor ($)'})

# Inserir gráfico
worksheet.insert_chart('E2', chart)

workbook.close()
```

### 3. Planilha com Formatação Condicional

```python
import xlsxwriter

workbook = xlsxwriter.Workbook('formatacao_condicional.xlsx')
worksheet = workbook.add_worksheet()

# Formatos para condições
red = workbook.add_format({
    'bg_color': '#FF0000',
    'font_color': 'white'
})

green = workbook.add_format({
    'bg_color': '#00B050',
    'font_color': 'white'
})

# Dados
notas = [85, 92, 45, 78, 95, 38, 88]

# Escrever notas
for i, nota in enumerate(notas):
    if nota >= 70:
        worksheet.write(i, 0, nota, green)
    else:
        worksheet.write(i, 0, nota, red)

worksheet.set_column('A:A', 15)

workbook.close()
```

### 4. Planilha com Merged Cells

```python
import xlsxwriter

workbook = xlsxwriter.Workbook('merged_cells.xlsx')
worksheet = workbook.add_worksheet()

# Formato para título
title = workbook.add_format({
    'bold': True,
    'font_size': 16,
    'align': 'center',
    'valign': 'vcenter',
})

# Mesclar células e adicionar título
worksheet.merge_range('A1:D1', 'Relatório Mensal', title)

# Conteúdo abaixo
worksheet.write('A3', 'Dados:')

workbook.close()
```

## 🎨 Formatação Disponível

### Cores
```python
format = workbook.add_format({
    'bg_color': '#FF0000',      # Cor de fundo (hex)
    'font_color': '#FFFFFF',    # Cor da fonte (hex)
})
```

### Fontes
```python
format = workbook.add_format({
    'font_name': 'Arial',
    'font_size': 12,
    'bold': True,
    'italic': True,
    'underline': True,
})
```

### Alinhamento
```python
format = workbook.add_format({
    'align': 'center',          # left, center, right
    'valign': 'vcenter',        # top, vcenter, bottom
    'text_wrap': True,          # Quebra de linhas
})
```

### Bordas
```python
format = workbook.add_format({
    'border': 1,                # Todas as bordas
    'border_color': '#000000',  # Cor da borda
    'border_width': 2,          # Espessura
})
```

### Números
```python
format = workbook.add_format({
    'num_format': '$#,##0.00',      # Moeda
    'num_format': '0.00%',          # Percentual
    'num_format': 'yyyy-mm-dd',     # Data
})
```

## 📊 Tipos de Gráficos

```python
# Coluna
chart = workbook.add_chart({'type': 'column'})

# Linha
chart = workbook.add_chart({'type': 'line'})

# Pizza
chart = workbook.add_chart({'type': 'pie'})

# Área
chart = workbook.add_chart({'type': 'area'})

# Dispersão
chart = workbook.add_chart({'type': 'scatter'})

# Bolha
chart = workbook.add_chart({'type': 'bubble'})
```

## 🔧 Operações Úteis

### Ajustar Largura de Coluna
```python
worksheet.set_column('A:A', 20)        # Coluna A com 20 unidades
worksheet.set_column('A:D', 15)        # Colunas A até D com 15
worksheet.set_column('A:Z', 'auto')    # Auto-ajustar
```

### Congelar Panes
```python
worksheet.freeze_panes(1, 0)  # Congelar primeira linha
```

### Ocultar Colunas/Linhas
```python
worksheet.set_column('A:A', None, None, {'hidden': True})
worksheet.set_row(0, None, None, {'hidden': True})
```

### Validação de Dados
```python
worksheet.data_validation('A2:A10', {
    'validate': 'list',
    'source': ['Opção 1', 'Opção 2', 'Opção 3']
})
```

## 🐛 Troubleshooting

### Erro: "No module named xlsxwriter"
```bash
pip install xlsxwriter
```

### Caracteres especiais não aparecem
```python
# Usar encoding UTF-8
import xlsxwriter

workbook = xlsxwriter.Workbook('arquivo.xlsx')
# Escrever normalmente (UTF-8 é padrão)
```

### Arquivo fica corrompido
```python
# Certifique-se de fechar o workbook
workbook.close()  # IMPORTANTE!
```

## 📚 Documentação Oficial

- [XlsxWriter Documentation](https://xlsxwriter.readthedocs.io/)
- [Excel Format Specifications](https://en.wikipedia.org/wiki/Office_Open_XML)

## 🎓 Casos de Uso

✅ **Bom para:**
- Gerar relatórios
- Exportar dados de banco de dados
- Criar planilhas de configuração
- Automatizar criação de documentos
- Teste de dados

❌ **Não é bom para:**
- Modificar arquivos Excel existentes (use `openpyxl`)
- Ler dados de Excel (use `pandas` ou `openpyxl`)

## 💡 Próximas Melhorias no Projeto

- [ ] Criar exemplo com múltiplas abas
- [ ] Adicionar exemplo com gráficos
- [ ] Exemplo com imagens
- [ ] Exemplo com validação de dados
- [ ] Exemplo com formatação condicional
- [ ] Performance com grandes volumes de dados
- [ ] Integração com banco de dados
- [ ] Testes automatizados

## 📝 Licença

XlsxWriter é de código aberto sob licença BSD.
