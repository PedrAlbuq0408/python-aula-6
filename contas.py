from abc import ABC, abstractmethod

from cliente import Cliente


def formatar_reais(valor):
    """Formata um número como moeda brasileira. Ex: R$ 1.234,56"""
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def _validar_numero(valor, nome, minimo=None, maximo=None):
    """Garante que o valor é número (int/float) e está dentro dos limites."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{nome} deve ser um número.")
    if minimo is not None and valor < minimo:
        raise ValueError(f"{nome} não pode ser menor que {minimo}.")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{nome} não pode ser maior que {maximo}.")
    return float(valor)


class Conta(ABC):
    """Classe abstrata: define o que toda conta tem, mas não pode ser criada diretamente."""

    TIPO = "Conta"
    _proximo_numero = 1001  

    def __init__(self, titular, saldo_inicial=0.0):
        self.titular = titular         
        self.saldo = saldo_inicial     
        self._numero = Conta._proximo_numero
        Conta._proximo_numero += 1

    @property
    def numero(self):
        return self._numero

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, valor):
        if not isinstance(valor, Cliente):
            raise ValueError("Titular deve ser um objeto da classe Cliente.")
        self._titular = valor

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = _validar_numero(valor, "Saldo", minimo=0)

    def depositar(self, valor):
        valor = _validar_numero(valor, "Valor do depósito")
        if valor <= 0:
            raise ValueError("Valor do depósito deve ser maior que zero.")
        self.saldo += valor

    def sacar(self, valor):
        valor = _validar_numero(valor, "Valor do saque")
        if valor <= 0:
            raise ValueError("Valor do saque deve ser maior que zero.")
        if valor > self._saldo:
            raise ValueError(
                f"Saldo insuficiente: saldo de {formatar_reais(self._saldo)}, "
                f"saque de {formatar_reais(valor)}."
            )
        self.saldo -= valor

    @abstractmethod
    def calcular_rendimento(self):
        """Quanto a conta rende no mês."""

    @abstractmethod
    def tarifa_mensal(self):
        """Quanto o banco cobra de tarifa no mês."""

    
    def fechar_mes(self):
        """Aplica rendimento e tarifa. Retorna o ganho (ou perda) líquido do mês."""
        rendimento = self.calcular_rendimento()
        tarifa = min(self.tarifa_mensal(), self._saldo + rendimento)
        self.saldo = self._saldo + rendimento - tarifa
        return rendimento - tarifa
    def __str__(self):
        return (
            f"[{self.TIPO}] Nº {self._numero} | "
            f"Titular: {self._titular.nome} | Saldo: {formatar_reais(self._saldo)}"
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}(numero={self._numero}, "
            f"titular={self._titular.nome!r}, saldo={self._saldo:.2f})"
        )

    def __eq__(self, outro):
        if not isinstance(outro, Conta):
            return NotImplemented
        return self._numero == outro._numero

    def __lt__(self, outro):
        if not isinstance(outro, Conta):
            return NotImplemented
        return self._saldo < outro._saldo

    def __hash__(self):
        return hash(self._numero)


class ContaCorrente(Conta):
    """Não rende nada e cobra uma tarifa mensal."""

    TIPO = "Conta Corrente"

    def __init__(self, titular, saldo_inicial=0.0, tarifa=12.0):
        super().__init__(titular, saldo_inicial)
        self.tarifa = tarifa

    @property
    def tarifa(self):
        return self._tarifa

    @tarifa.setter
    def tarifa(self, valor):
        self._tarifa = _validar_numero(valor, "Tarifa", minimo=0)

    def calcular_rendimento(self):
        return 0.0

    def tarifa_mensal(self):
        return self._tarifa

    def __str__(self):
        return super().__str__() + f" | Tarifa: {formatar_reais(self._tarifa)}"


class ContaPoupanca(Conta):
    """Rende uma taxa mensal sobre o saldo e não cobra tarifa."""

    TIPO = "Conta Poupança"

    def __init__(self, titular, saldo_inicial=0.0, taxa_rendimento=0.005):
        super().__init__(titular, saldo_inicial)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor):
        self._taxa_rendimento = _validar_numero(valor, "Taxa de rendimento", minimo=0, maximo=1)

    def calcular_rendimento(self):
        return self._saldo * self._taxa_rendimento

    def tarifa_mensal(self):
        return 0.0

    def __str__(self):
        return super().__str__() + f" | Rende: {self._taxa_rendimento * 100:.2f}% a.m."


class ContaInvestimento(Conta):
    """Rende mais que a poupança, mas exige depósito mínimo e cobra tarifa fixa."""

    TIPO = "Conta Investimento"
    DEPOSITO_MINIMO = 500.0
    TARIFA_FIXA = 5.0

    def __init__(self, titular, saldo_inicial=0.0, taxa_rendimento=0.012):
        super().__init__(titular, saldo_inicial)
        if self._saldo < self.DEPOSITO_MINIMO:
            raise ValueError(
                f"Conta Investimento exige depósito inicial de pelo menos "
                f"{formatar_reais(self.DEPOSITO_MINIMO)}."
            )
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor):
        self._taxa_rendimento = _validar_numero(valor, "Taxa de rendimento", minimo=0, maximo=1)

    def calcular_rendimento(self):
        return self._saldo * self._taxa_rendimento

    def tarifa_mensal(self):
        return self.TARIFA_FIXA

    def __str__(self):
        return super().__str__() + f" | Rende: {self._taxa_rendimento * 100:.2f}% a.m."