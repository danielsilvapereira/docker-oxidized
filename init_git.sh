#!/bin/sh

# Diretório do repositório Git
GIT_REPO_DIR=/root/.config/oxidized/output/configs.git

# Verificar se o diretório já existe
if [ ! -d "$GIT_REPO_DIR" ]; then
  # Criar o diretório e inicializar o repositório Git
  mkdir -p "$GIT_REPO_DIR"
  git init --bare "$GIT_REPO_DIR"
  echo "Initialized empty Git repository in $GIT_REPO_DIR"
fi

# Iniciar o Oxidized
exec oxidized "$@"
