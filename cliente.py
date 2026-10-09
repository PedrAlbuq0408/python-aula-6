import re

REGEX_EMAIL = r"^\w+([.\-]\w+)*@\w+([.\-]\w+)*\.[a-zA-Z]{2,}$"


class Cliente:
    """Representa um cliente do banco."""

    def __init__(self, nome, email, cpf):
        self.nome = nome
        self.email = email
        self.cpf = cpf

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres.")
        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not re.match(REGEX_EMAIL, valor):
            raise ValueError(f"E-mail inválido: '{valor}'")
        self._email = valor

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        so_digitos = re.sub(r"\D", "", str(valor))
        if len(so_digitos) != 11:
            raise ValueError(f"CPF inválido: '{valor}' (precisa ter 11 dígitos)")
        self._cpf = so_digitos

    def __str__(self):
        return f"{self._nome} <{self._email}>"

    def __repr__(self):
        return f"Cliente(nome={self._nome!r}, email={self._email!r}, cpf={self._cpf!r})"

    def __eq__(self, outro):
        if not isinstance(outro, Cliente):
            return NotImplemented
        return self._cpf == outro._cpf

    def __lt__(self, outro):
        if not isinstance(outro, Cliente):
            return NotImplemented
        return self._nome < outro._nome

    def __hash__(self):
        return hash(self._cpf)