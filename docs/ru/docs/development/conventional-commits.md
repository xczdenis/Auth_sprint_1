# Conventional Commits

Твои комментарии к коммитам должны соответствовать [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
Pre-commit хук `conventional-pre-commit` выполнит проверку комментария перед коммитом.

Если твой комментарий не соответствует конвенции, то в терминале ты увидишь подобное сообщение:
```bash
commitizen check.........................................................Failed
- hook id: conventional-pre-commit
- exit code: 1
```
Для более удобного написания комментариев к коммитам, ты можешь воспользоваться плагином
Conventional Commit для PyCharm:
![conventional-commit-plugin](../img/PyCharm/conventional-commit-plugin.png)
