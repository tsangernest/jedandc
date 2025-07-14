from invoke import task


@task(aliases=["venv"])
def virtualenvironment(c, update=False):
    print(f"\n***\nCreating VirtualEnvironment\n***\n")

    c.run("python3.13 -m venv .venv/", pty=True)
    c.run("source .venv/bin/activate", pty=True)
    c.run("pip install --upgrade pip", pty=True)
    c.run("pip install -U pip-tools setuptools wheel psycopg2-binary", pty=True)

    if update:
        c.run("pip-compile requirements.in", pty=True)

    c.run("pip install -r requirements.txt --no-cache-dir", pty=True)


@task
def startapp(c, build=True):
    if build:
        c.run("docker compose down", pty=True)
        c.run("docker compose build", pty=True)

    c.run("docker compose up", pty=True)
    print(f"\n***\nGo to port:8000 for djang-web-app\n***\n")


@task
def exec(c, container="django"):
    print(f"\n***\nJumping into django\n***\n")
    c.run(f"docker exec -it {container} /bin/bash", pty=True)


@task
def down(c):
    print(f"\n***\nDestroying Containers\n***\n")
    c.run("docker compose down", pty=True)
    c.run("docker system prune -a -f", pty=True)

