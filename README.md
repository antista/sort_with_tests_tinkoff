# task-2
Версия 1.0

Автор: Антипенкова Анастасия

## Описание
Утилита командной строки sort. Команда sort сортирует строки, входящие во все файлы, и выдает результат на стандартный вывод (stdout). Если имена файлов не указаны, информация берется со стандартного ввода (stdin).

### Примеры запуска
* `echo ... | python -m sort`
* `python -m sort filename [filename...]`

### Запуск тестов
* `python -m pytest`

### Запуск линтера
* `flake8 sort`