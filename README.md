Markdown## ⚙️ Installation & Deployment

HackHub is distributed as a Python package through PyPI and can be deployed using either `pipx` (recommended for system isolation) or standard `pip` environments.

### 🛡️ Recommended: Isolation via pipx
Using `pipx` installs HackHub into an isolated environment while automatically injecting the executable binary straight into your user path. This approach prevents dependency conflicts and is the preferred method for Kali Linux and modern Linux distributions adhering to strict environment standards.

```bash
# Install pipx on Debian/Ubuntu/Kali distributions if not already present
sudo apt update && sudo apt install pipx -y
pipx ensurepath

# Restart your terminal session or reload your shell environment
source ~/.bashrc

# Install HackHub globally within an isolated pipeline
pipx install hackhub

# Verify the installation and path binding
hackhub --help
🔹 Alternative: Standard Pip InstallationIf your local deployment environment or virtual environment (venv) allows direct package management, you can install the package via standard pip loops:Bash# Install directly from the PyPI registry
pip install hackhub

# Verify execution syntax
hackhub --help
🐧 Kali Linux Optimization NotesModern Kali Linux releases enforce PEP 668 (Externally Managed Environments), meaning direct system-wide pip install commands will fail with an error.To bypass this safely without destabilizing core system packages, always default to the pipx architecture:Bash# Correct approach for Kali Linux environments
pipx install hackhub
⚡ Quick Start & Core Command SyntaxesOnce installed, the hackhub binary can be called natively from any terminal path directory.1. Enumerate Dynamic Flags & Sub-CommandsBashhackhub --help
2. Initialize a Listener Instance on a Single PortBashhackhub -p 4444
3. Deploy Multi-Port Concurrent Matrix SocketsBashhackhub -p 1234,4444
4. Initialize Multi-Port Array Using Verbose Argument FormatsBashhackhub --port 1234,4444,8080
🔧 Prerequisites & System CompatibilityTechnical Baseline RequirementsPython Engine: Version 3.9 or higher.Core Libraries: Standard distribution packages (asyncio, termios, tty, argparse). No third-party heavy dependencies required.Host Platform Compatibility MatrixOperating SystemDistribution AlignmentValidation StatusLinux EcosystemKali Linux, Debian Core, Ubuntu Server LTSFull Production VerifiedWindows SubsystemMicrosoft Windows Native CMD Environment⚠️ Experimental Tier Only📦 Distribution Packages Registry MetadataRegistry SourceTarget Package IdentifierCommand VectorPyPI Production Repositoryhackhubpip install hackhubIsolated Binary Matrixhackhubpipx install hackhub
