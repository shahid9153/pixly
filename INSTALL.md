## Pixly Quick Start Guide 
A guide to setup Pixly in your desktop.
### 📋 Prerequisites
<div>

<table>
<tr>
<td align="center" width="25%">

**🐍 Python 3.11+**
```bash
python --version
```

</td>
<td align="center" width="25%">

**🪟 Windows 10/11**
```bash
node --version
```

</td>
<td align="center" width="25%">

**⚡ uv Package Manager**

```bash
pip install uv
```
</td>

<td align="center" width="25%">

**🔧 Git**
```bash
git --version
```

</td>
</tr>
</table>
</div>


### Quick Setup

1. Clone the repository : 
```bash 
git clone https://github.com/MLSAKIIT/pixly.git
cd hacktoberfest
```
2. Open a powershell terminal as administrator and run the setup.bat file.
```bash
.\setup.bat
```
### Manual Setup 
1. Clone the repository : 
```bash 
git clone https://github.com/MLSAKIIT/pixly.git
cd hacktoberfest
```
1. Install uv package manager 
```bash 
pip install uv
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```
1. Install dependencies 
```bash
uv sync
```
1. Set up environment variables : 
   1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   2. Create a new API key
   3. Add to `.env`:
```bash
GEMINI_API_KEY=your_gemini_key_here
```

1. Make a folder called `vector_db`

2. Start the application, Create two powershell terminals 

Terminal 1 - Start Backend:
```bash
uv run run.py
```
Wait for the backend to start then in Terminal 2 - Start Frontend:
```bash 
uv run overlay.py
```

## Debugging 

To test the various parts of the backend pipeline :

1. Start the server in Terminal 1 :
```bash
uv run run.py
```
1. Start the test script in Terminal 2 : 
```bash
uv run test_system.py
```