# Установка pre-commit хуков

## 1. Проверка установки pre-commit
Пакет [pre-commit](https://pre-commit.com/) включен в список зависимостей и устанавливается
командой `poetry install`. Для проверки корректности установки `pre-commit`
нужно выполнить команду:
```bash
pre-commit --version
```
В ответ должна быть выведена версия pre-commit - это значит, что все установлено корректно:
```bash
pre-commit 2.20.0
```

## 2. Установка скриптов git hook
```bash
pre-commit install
pre-commit install --hook-type commit-msg
```
Если установка прошла успешно, то ты увидишь следующее сообщение:
```bash
pre-commit installed at .git/hooks/pre-commit
```
