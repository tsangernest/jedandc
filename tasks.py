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