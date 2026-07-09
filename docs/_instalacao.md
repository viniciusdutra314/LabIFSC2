
# Instalação em ambiente virtual

O ecossistema Python é cheio de gerenciadores de pacotes/ambientes ([pipx](https://github.com/pypa/pipx), [poetry](https://python-poetry.org/), [uv](https://astral.sh/blog/uv), [miniconda](https://docs.anaconda.com/miniconda/), etc.). Sinta-se livre para escolher o de sua preferência. Caso seja um iniciante no assunto, recomendamos testar o [uv](https://astral.sh/blog/uv).

Iremos descrever aqui como uma instalação local é feita usando somente as ferramentas nativas do Python (pip, venv).

Com o comando abaixo, estamos chamando o módulo (python -m) venv (virtual environment) e criando um ambiente virtual na pasta .venv (na maioria dos sistemas operacionais, isso será uma pasta oculta, visto que começa com ponto):
```bash
python -m venv .venv
```

Dentro da pasta .venv, temos um pequeno script que irá isolar o Python do seu projeto do Python global. Podemos usar o comando `source` para executá-lo. Como isso depende do seu shell, aqui está o comando exato que você deve executar:

**Fonte: retirado da [documentação](https://docs.python.org/3/library/venv.html) do CPython**

| Plataforma | Shell     | Comando para ativar o ambiente virtual               |
|------------|-----------|------------------------------------------------------|
| POSIX      | bash/zsh  | `$ source <venv>/bin/activate`                       |
|            | fish      | `$ source <venv>/bin/activate.fish`                  |
|            | csh/tcsh  | `$ source <venv>/bin/activate.csh`                   |
|            | pwsh      | `$ <venv>/bin/Activate.ps1`                          |
| Windows    | cmd.exe   | `C:\<venv>\Scripts\activate.bat`                     |
|            | PowerShell| `PS C:\<venv>\Scripts\Activate.ps1`                  |

Agora, toda vez que você instalar algo com o pip, na verdade será instalado na pasta .venv/lib.

```bash
pip install LabIFSC2
```

