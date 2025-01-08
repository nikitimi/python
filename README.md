### Set-up

1. Virtual environment is the ideal set-up:

```bash
    python -m venv .
```

2. Activate the venv:

```bash
    Scripts/activate
```

3. Install all module requirements.

```bash
   python -m pip install -r requirements.txt
```

### Others

- If you encounter error:

        × Getting requirements to build wheel did not run successfully.

You need to update modules:

```bash
    python -m pip install --upgrade setuptools wheel
```

- Add modules in the requirements:

```bash
    python -m pip freeze > requirements.txt
```
