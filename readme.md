# Sistema Bancário Orientado a Objetos

Sistema em Python que modela clientes, contas bancárias e um banco, aplicando classes, encapsulamento, herança, polimorfismo e classes abstratas.

## Como executar

```bash
python main.py
```

## Classes

- `Cliente`: nome, e-mail e CPF, todos validados
- `Conta` (abstrata): base de todas as contas
- `ContaCorrente`, `ContaPoupanca` e `ContaInvestimento`: filhas de `Conta`
- `Banco`: guarda as contas e opera sobre todas elas

## Onde está cada conceito

- **Classe abstrata:** `Conta(ABC)` com `@abstractmethod` em `calcular_rendimento` e `tarifa_mensal` (`contas.py`)
- **Herança e `super()`:** as 3 contas filhas chamam `super().__init__(...)`
- **Encapsulamento com `@property`:** nome, e-mail, CPF, saldo, titular, tarifa e taxa de rendimento têm getter e setter com validação. Um objeto inválido nunca é criado.
- **Polimorfismo:** `calcular_rendimento()` e `tarifa_mensal()` respondem diferente em cada tipo de conta, e `fechar_mes()` usa os dois
- **`__init__` e `__str__`:** presentes em todas as classes
- **Métodos especiais:** `__repr__`, `__eq__`, `__lt__`, `__hash__` e `__len__`
- **Testes:** `main.py` cria 14 objetos, itera sobre contas de tipos diferentes e captura 13 entradas inválidas com `try/except`

## Regras das contas

| Conta | Rendimento | Tarifa mensal |
|---|---|---|
| Corrente | nenhum | R$ 12,00 (padrão) |
| Poupança | 0,5% a.m. (padrão) | nenhuma |
| Investimento | 1,2% a.m. (padrão) | R$ 5,00 |

A conta investimento exige depósito inicial mínimo de R$ 500,00.