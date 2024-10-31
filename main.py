'''граф зависимостей между коммитами Git и его визуализация с помощью Graphviz'''

import os #для работы с операционной системой, например, для проверки, существует ли файл или папка
import subprocess #для выполнения команд в командной строке из кода Python
import argparse #позволяет обрабатывать аргументы командной строки, такие как --repo_path, --since_date и т.д.
import datetime #чтобы проверять, правильно ли введена дата, и использовать её для фильтрации коммитов
from graphviz import Digraph


# Функция для получения списка коммитов в заданном репозитории после определенной даты
def get_commits(repo_path, since_date):
    # repo_path (путь к репозиторию) и since_date (дата) для поиска коммитов после этой даты
    # Формируем команду для получения коммитов Git
    git_log_cmd = ['git', '-C', repo_path, 'log', '--pretty=format:%H %p %ci', '--since', since_date]
    #git -C <путь>: указывает Git работать в указанной папке репозитория
    #log --pretty=format:%H %p %ci: выводит каждый коммит в формате:
    # -%H: хеш коммита -%p: хеш родительских коммитов -%ci: дата коммита
    # --since: указывает фильтр по дате — берём коммиты только после since_date
    try:
        result = subprocess.run(git_log_cmd, stdout=subprocess.PIPE, text=True, check=True)
        # stdout=subprocess.PIPE: позволяет читать стандартный вывод
        # text=True: возвращает вывод в текстовом формате, а не в байтах

        # удаляем лишние пробелы и разделяем результат по строкам
        commit_lines = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении git команды: {e}")
        return []

    commits = [] #для сохранения информации о коммитах
    for line in commit_lines:
        parts = line.split() #Разделяем строку на части (слова)
        commit_hash = parts[0]  # Первый элемент — это хеш коммита
        parents = parts[1:-2]  # Остальные — хеши родительских коммитов (зависимости)
        commit_date = parts[-2]  # Последний элемент — это дата коммита
        # Добавляем коммит в список
        commits.append((commit_hash, parents, commit_date))
    return commits


# Функция для построения графа зависимостей
def build_graph(commits):
    # Создаёт объект для графа, где будем добавлять узлы и связи
    dot = Digraph(comment='Commit Dependency Graph')
    dot.attr(rankdir='LR')  # Выстраиваем граф слева направо

    # Проходим по каждому коммиту
    for commit_hash, parents, commit_date in commits:
        # Добавляем узел для каждого коммита
        dot.node(commit_hash, label=f"{commit_hash[:7]}\n{commit_date}")
        #label=f"{commit_hash[:7]}\n{commit_date}": метка узла, которая состоит из первых 7 символов хеша и даты

        # Добавляем ребра для зависимостей
        for parent in parents:
            # Рисуем ребро от каждого родителя к текущему коммиту
            dot.edge(parent, commit_hash)
    return dot


# Основная функция
def main():
    # Параметры командной строки
    #Создание объектa для обработки аргументов командной строки
    parser = argparse.ArgumentParser(description="Генератор графа зависимостей коммитов")
    #настройка каждого из аргументов:
    #путь к папке для сохранения графа
    parser.add_argument("--visualizer_path", type=str, help="Путь к Graphviz для отображения графа", required=True)
    #путь к репозиторию
    parser.add_argument("--repo_path", type=str, help="Путь к анализируемому репозиторию", required=True)
    #дата для фильтрации коммитов
    parser.add_argument("--since_date", type=str, help="Дата коммитов в формате ГГГГ-ММ-ДД", required=True)

    args = parser.parse_args()

    # Проверяем, что дата введена корректно
    try:
        datetime.datetime.strptime(args.since_date, "%Y-%m-%d")
    except ValueError:
        print("Ошибка: Неверный формат даты. Используйте формат ГГГГ-ММ-ДД.")
        return

    # Получаем коммиты и строим граф
    commits = get_commits(args.repo_path, args.since_date)
    if not commits:
        print("Не найдено коммитов для указанной даты.")
        return

    # Создаем граф и выводим его на экран
    graph = build_graph(commits)
    graph.view(directory=args.visualizer_path)


if __name__ == "__main__":
    main()
