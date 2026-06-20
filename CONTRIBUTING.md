# Contribuindo para o Projeto de Auditoria Bancária

Obrigado por demonstrar interesse em melhorar nosso pipeline de conciliação! Para manter a qualidade do código sob governança, siga as diretrizes abaixo:

## 🔀 Workflow de Git
1. Faça um Fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/minha-melhoria`).
3. Siga o padrão de **Conventional Commits** (ex: `feat:`, `fix:`, `docs:`).
4. Abra um Pull Request detalhado para a branch `master`.

## 🎨 Padrões de Código
* Executar o `black .` para formatação automática do Python.
* Verificar regras de linting com `flake8`.
* Garantir que nenhum arquivo binário ou base de dados local (`.csv`, `.parquet`) seja rastreado pelo Git.
