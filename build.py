import subprocess


def lint():
    result = subprocess.run(["flake8"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Linting passed!")
    else:
        print("Linting failed:")
        print(result.stdout)


def build():
    # Agrega aquí tus tareas de construcción adicionales, si las hay
    print("Building...")
    print("implementarlo")


if __name__ == "__main__":
    lint()
    build()
