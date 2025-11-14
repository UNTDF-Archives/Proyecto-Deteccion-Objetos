# Proyecto SI - Guía de Configuración

Este proyecto requiere **Python 3.9.19**. El archivo `.python-version` especifica la versión exacta.

## 📋 Instrucciones Paso a Paso

### 1. Instalar pyenv (si no lo tienes)

```bash
# Instalar dependencias (Ubuntu/Debian)
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev \
    libxmlsec1-dev libffi-dev liblzma-dev

# Instalar pyenv
curl https://pyenv.run | bash
```

**Configurar pyenv:** Agrega estas líneas al final de `~/.bashrc` o `~/.zshrc`:

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Luego recarga tu shell: `source ~/.bashrc` o `source ~/.zshrc`

---

### 2. Navegar al proyecto

```bash
cd /ruta/a/Proyecto-si
```

---

### 3. Instalar Python 3.9.19

```bash
pyenv install 3.9.19
pyenv local 3.9.19
python --version  # Debe mostrar: Python 3.9.19
```

---

### 4. Crear entorno virtual

```bash
python -m venv .venv
```

---

### 5. Activar entorno virtual

```bash
source .venv/bin/activate
```

---

### 6. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota:** Si hay timeout, usar: `pip install --timeout 300 --retries 5 -r requirements.txt`

---

### 7. Verificar instalación

```bash
python test_imports.py
```

Deberías ver: `✅ Todos los módulos se importaron correctamente.`

---