import subprocess

def get_git_objects():
    # Получаем список всех объектов в репозитории
    try:
        # Выполняем команду git rev-list для получения всех объектов
        result = subprocess.run(['git', 'rev-list', '--all'], stdout=subprocess.PIPE, text=True, check=True)
        object_hashes = result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        return

    # Выводим содержимое каждого объекта
    for obj_hash in object_hashes:
        try:
            # Выполняем команду git cat-file -p для получения содержимого объекта
            result = subprocess.run(['git', 'cat-file', '-p', obj_hash], stdout=subprocess.PIPE, text=True, check=True)
            print(f"Содержимое объекта {obj_hash}:\n{result.stdout}\n")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при получении содержимого объекта {obj_hash}: {e}")

if __name__ == "__main__":
    get_git_objects()
