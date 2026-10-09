from contas import Conta, formatar_reais


class Banco:
    """Guarda as contas e faz operações em conjunto (composição)."""

    def __init__(self, nome):
        self.nome = nome
        self._contas = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome do banco não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def contas(self):
        return list(self._contas)

    def adicionar_conta(self, conta):
        if not isinstance(conta, Conta):
            raise ValueError("Só é possível adicionar objetos do tipo Conta.")
        if conta in self._contas: 
            raise ValueError(f"A conta Nº {conta.numero} já está cadastrada.")
        self._contas.append(conta)

    def total_depositado(self):
        return sum(conta.saldo for conta in self._contas)

    def fechar_mes_todas(self):
        """Chama fechar_mes() em cada conta. Cada tipo reage do seu jeito (polimorfismo)."""
        return {conta.numero: conta.fechar_mes() for conta in self._contas}

    def __len__(self):
        return len(self._contas)

    def __str__(self):
        return (
            f"{self._nome} | {len(self._contas)} contas | "
            f"Total depositado: {formatar_reais(self.total_depositado())}"
        )

    def __repr__(self):
        return f"Banco(nome={self._nome!r}, contas={len(self._contas)})"