# Домашнее задание 2 конфигурационное управление
## Вариант 31
### Задание 2
Разработать инструмент командной строки для визуализации графа 
зависимостей, включая транзитивные зависимости. Сторонние программы или 
библиотеки для получения зависимостей использовать нельзя. 
Зависимости определяются для git-репозитория. Для описания графа 
зависимостей используется представление Graphviz. Визуализатор должен 
выводить результат на экран в виде графического изображения графа. 
Построить граф зависимостей для коммитов, в узлах которого содержатся 
номера коммитов в хронологическом порядке. Граф необходимо строить только 
для коммитов позже заданной даты. 
Ключами командной строки задаются: 
- Путь к программе для визуализации графов.
- Путь к анализируемому репозиторию.
- Дата коммитов в репозитории.

Все функции визуализатора зависимостей должны быть покрыты тестами.
### Общее описание
Программа генерирует граф зависимостей между коммитами Git и визуализирует его с помощью Graphviz.

1. **Получение коммитов**: программа использует команду `git log`, чтобы собрать данные о коммитах в указанном репозитории, включая их хеши, родителей и дату. Фильтрация происходит по дате, заданной пользователем.

2. **Построение графа**: на основе данных о коммитах создается направленный граф, где узлы — коммиты, а ребра отображают зависимости (связь с родительскими коммитами).

3. **Визуализация**: граф сохраняется и отображается с использованием Graphviz, а узлы маркируются укороченными хешами и датами.

**Параметры командной строки**:
- `--repo_path`: путь к анализируемому репозиторию.
- `--since_date`: дата начала анализа в формате `ГГГГ-ММ-ДД`.
- `--visualizer_path`: путь для сохранения и отображения графа.

Программа помогает понять структуру и историю ветвления проекта, особенно полезна для анализа больших репозиториев.
### Описание функции get_commits
Функция **`get_commits(repo_path, since_date)`** получает список коммитов из указанного Git-репозитория после заданной даты. 

1. Выполняется команда Git для извлечения данных о коммитах: их хешей, родительских коммитов и дат.
2. Результат разбивается на строки и анализируется. Каждый коммит представляется в виде кортежа: `(commit_hash, parents, commit_date)`.
3. Возвращает список таких кортежей. Если возникает ошибка, возвращается пустой список.
### Описание функции build_graph
Функция **`build_graph(commits)`** создает граф зависимостей коммитов с помощью Graphviz.

1. Инициализирует объект графа, настраивая его отображение слева направо.
2. Для каждого коммита добавляет узел с меткой, содержащей укороченный хеш и дату.
3. Для каждого родительского коммита создает ребро, показывающее связь с текущим коммитом.
4. Возвращает объект графа для дальнейшей визуализации.
### Описание функции main
Функция **`main()`** — это точка входа программы, которая обрабатывает аргументы командной строки, проверяет корректность ввода, получает коммиты, строит граф зависимостей и отображает его.

1. Считывает параметры: путь к репозиторию, дату фильтрации коммитов, путь для сохранения графа.
2. Проверяет формат даты.
3. Вызывает **`get_commits`** для получения списка коммитов.
4. Если коммиты найдены, строит граф с помощью **`build_graph`** и отображает его через Graphviz.
### Тест
