Bütün hissələri, yeni əlavə etdiyimiz professional quraşdırma təlimatlarını, əmrləri və sosial media kəsdirmələrini özündə birləşdirən, birbaşa GitHub-a yapışdıra biləcəyin tam və bütöv README.md faylı abicim:Markdown# 📡 HackHub

<p align="center">
  <img src="https://img.shields.io/badge/Status-Beta-orange?style=for-the-badge&logo=git" alt="Status Beta">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Architecture-AsyncIO-blueviolet?style=for-the-badge&logo=asyncio" alt="Architecture AsyncIO">
  <img src="https://img.shields.io/badge/Developer-res4ad-success?style=for-the-badge&logo=github" alt="Developer res4ad">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License MIT">
</p>

<p align="center">
  <strong>An operator-focused security testing ecosystem designed to simplify session management, logging, scanning, reporting, and future security workflows.</strong>
</p>

<p align="center">
  Core Maintainer: <a href="https://github.com/res4ad">Reshad Rustemov (@res4ad)</a>
</p>

<p align="center">
  <a href="https://github.com/res4ad"><img src="https://img.shields.io/badge/GitHub-res4ad-181717?style=flat-square&logo=github" alt="GitHub"></a>
  <a href="https://linkedin.com/in/res4ad"><img src="https://img.shields.io/badge/LinkedIn-res4ad-0A66C2?style=flat-square&logo=linkedin" alt="LinkedIn"></a>
  <a href="https://instagram.com/res4ad"><img src="https://img.shields.io/badge/Instagram-res4ad-E4405F?style=flat-square&logo=instagram" alt="Instagram"></a>
</p>

---

## ⚡ One Platform. Multiple Security Workflows.

**HackHub** is not just a collection of disconnected standalone utilities; it is engineered as a unified security testing ecosystem. The project's vision is to consolidate separate testing stages—ranging from network listening and vulnerability scanning to campaign orchestration and reporting—into a cohesive, operator-focused workflow. 

By grounding the core infrastructure on a unified user experience and a non-blocking asynchronous codebase, HackHub ensures that your workflows remain responsive, fluid, and scalable.

> [!WARNING]  
> **Development Status:** HackHub is currently in active **Beta**. The core ecosystem layout and database architectures are evolving rapidly. It is recommended strictly for isolated training environments, laboratory research, and authorized evaluation setups.

---

## ❓ Why HackHub?

Security operators routinely struggle with tool fragmentation. Conducting an assessment often forces practitioners to manage multiple disconnected windows, configure independent text logs, and manually cross-reference data points between third-party systems.

HackHub aims to resolve this friction by providing a **unified operator workflow**. By centralizing session management and tracking notes into a single interface, it cuts down context-switching fatigue and ensures that all technical data gathered during an evaluation remains contextualized, readable, and structured for downstream analysis.

---

## 🧬 Ecosystem Architecture

HackHub is engineered around a scalable, decoupled design. While the infrastructure is planned as a comprehensive testing suite, it separates current stable features from long-term platform modules.

### Component Structure Diagram

```text
                       +-----------------------+
                       |     HACKHUB CORE      |
                       +-----------+-----------+
                                   |
         +-------------------------+-------------------------+
         |                         |                         |
+--------+--------+       +--------+--------+       +--------+--------+
|    Listener     |       |     Scanner     |       | Payload Studio  |
|   Component     |       |    Component    |       |    Component    |
| (Current Core)  |       |    (Planned)    |       |    (Planned)    |
+--------+--------+       +--------+--------+       +--------+--------+
         |                         |                         |
         +-------------------------+-------------------------+
                                   |
         +-------------------------+-------------------------+
         |                         |                         |
+--------+--------+       +--------+--------+       +--------+--------+
|   Campaigns     |       |    Reporting    |       |  Plugin Engine  |
|   Component     |       |    Component    |       |   & Core API    |
|   (Planned)     |       |    (Planned)    |       |    (Planned)    |
+-----------------+       +-----------------+       +-----------------+
Module Status Breakdown📡 HackHub Listener (Available Now): Handles multiplexed, high-concurrency target links across variable ports. Runs on a tty-managed non-blocking backend.🔍 HackHub Scanner (Planned): Subnet discovery module built to mapping active internal endpoints and audit network asset definitions.🛠️ HackHub Payload Studio (Planned): Staging workshop for customizing script templates and organizing drop-configurations in laboratory setups.🎯 HackHub Campaigns (Planned): Orchestration dashboard designed to group multi-host targets and track connection state topologies over long testing windows.📊 HackHub Reporting & Asset Tracking (Planned): Compilation engine that automatically normalizes text logs, host notes, and metadata trails into crisp documentation.🔌 HackHub Plugins (Planned): Developer API allowing security practitioners to hook directly into session channels to extend terminal text behaviors.📸 Interface PreviewBelow are mock structural blueprints of the active ecosystem control line and interactive menus:Central Analytical Dashboard InterfacePlaintext+------------------------------------------------------------------------+
|                      HACKHUB FRAMEWORK INTERFACE [v0.5-BETA]           |
+------------------------------------------------------------------------+
| Uptime             : 02:44:19      | Bound Sockets      : [1234, 4444]  |
| Connected Hosts    : 4             | Log Writers        : 4 Active      |
+------------------------------------------------------------------------+
| Linux Sessions     : 3             | Windows Sessions   : 1             |
+------------------------------------------------------------------------+
| NAME/TAG      ID       ENDPOINT              PLATFORM       LISTEN_PORT|
| ------------- -------- --------------------- -------------- -----------|
| web-prod-01   e08875   192.168.1.50:46704    Linux 6.18     1234        |
| internal-kali d4f2a1   192.168.1.52:51012    Linux 6.18     4444        |
| sql-db-prod   b8c9d2   192.168.1.60:43219    Linux 5.15     1234        |
| win-work-04   f5e1a3   192.168.1.72:49221    Windows_CMD    4444        |
+------------------------------------------------------------------------+
[1] Session Manager | [2] Session Notes Archive | [4] Telemetry Log Viewer
[>] Selection: _
📍 Interface Layout PlaceholdersSession Management Engine Console ViewIntegrated Session Log Viewer Layout📊 Technical Capabilities MatrixFeature SetStandard Raw Sockets (nc)Workspace Utilities (tmux/screen)HackHub FrameworkConcurrent Port Binding❌ (Single port per instance)❌ (Requires layout multiplexing)(Native Asynchronous Engine)Status Overview Panel❌❌(Real-Time Performance Overview)Decoupled Data Logging❌ (Manual append loops required)⚠️ (Terse terminal transcripts)(Segmented logs/ Architecture)Workspace Notes Ledger❌❌(Target-Isolated RAM Array)In-Line Sub-Commands❌❌(Dedicated Interactivity Escape Hooks)File Integrity Tracking❌❌(MD5 Cryptographic Verification)⚙️ Installation & DeploymentHackHub is distributed as a Python package through PyPI and can be deployed using either pipx (recommended for system isolation) or standard pip environments.🛡️ Recommended: Isolation via pipxUsing pipx installs HackHub into an isolated environment while automatically injecting the executable binary straight into your user path. This approach prevents dependency conflicts and is the preferred method for Kali Linux and modern Linux distributions adhering to strict environment standards.Bash# Install pipx on Debian/Ubuntu/Kali distributions if not already present
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
🔧 Prerequisites & System CompatibilityTechnical Baseline RequirementsPython Engine: Version 3.9 or higher.Core Libraries: Standard distribution packages (asyncio, termios, tty, argparse). No third-party heavy dependencies required.Host Platform Compatibility MatrixOperating SystemDistribution AlignmentValidation StatusLinux EcosystemKali Linux, Debian Core, Ubuntu Server LTSFull Production VerifiedWindows SubsystemMicrosoft Windows Native CMD Environment⚠️ Experimental Tier Only🕹️ Interactive Interface ControlsWhen interacting directly with a target link, the operator can pass dynamic hooks to query the frame manager without breaking terminal context:📍 Session Escape CommandsCommand HookFunctional Execution Result:sessionsOutputs an optimized text table tracking all active network lines on disk.:switch <id/name>Swaps active terminal input focus straight to the chosen environment target.:addnote <text>Documents a technical observation field string into the current target metadata pool.:notesGenerates a sequential chronology printout of all data notes saved for the target.Ctrl + ADisengages input focus from the shell line and calls up the primary Dashboard Menu.📍 Navigation Shortcut MechanicsESC -> Immediately hides the administrative menu and restores input focus to interactive shell lines.Ctrl + C -> Minimizes terminal windows without breaking network connection states or losing logging descriptors.Q -> Reverts back exactly one level inside nested workspace paths.🗂️ Analytics & Logging Framework StructureThe listener engine automatically provisions a persistent tracking structure inside the runtime workspace path:Plaintextlogs/
├── session_e08875.log  <-- Contains full operational commands, timestamps & traffic loops
├── session_d4f2a1.log
└── session_b8c9d2.log
Operators can quickly query active execution trails by navigating to [4] Telemetry & Transaction Log Viewer inside the main dashboard panel to search via targeted text keywords or refine rows by calendar dates.🚀 Development RoadmapCurrent Iteration (v0.5)[x] Non-blocking multi-port asynchronous socket handling loop.[x] Unified terminal input multiplexing backend engine.[x] Structured diagnostic monitoring dashboard statistics module.[x] Multi-stream logging system separating interactive tasks by target.[x] Cryptographic verification file tracking using local MD5 parameters.Next Major Iteration (v1.0)[ ] Subnet Scanner discovery module engine.[ ] Automated plaintext reporting generation template pipeline.[ ] Developer extension Plugin API hook architecture.[ ] Multi-operator team collaboration access models.[ ] Core REST API support interface layer.[ ] High-density web workspace console application.⚠️ Project Beta StatusHackHub is an active engineering endeavor. Because it resides in a Beta development state, the application programming interfaces (APIs) may change significantly between iterations, and core storage arrays will evolve as optimization progresses. Bug reports, diagnostic logs, and platform architecture feedback are highly welcome through our issue tracker.🛡️ Security & Licensing TermsSecurity NoticeHackHub is intended strictly for authorized security assessments, academic lab research, and localized infrastructure evaluation. Executing this codebase across network configurations without explicit prior consent from the infrastructure asset owner is illegal. The contributors and maintainers assume zero structural liability for operational downtime, policy compliance issues, or downstream architecture damage caused by unauthorized modifications of this system framework.LicenseThis engineering ecosystem codebase is shared open-source under the structural criteria of the MIT License.👥 Developer & AcknowledgmentsLead Developer: Reshad Rustemov (@res4ad) - Core architecture and asynchronous engine implementation.Asynchronous Networking Foundation: The standard library Python Software Foundation maintainers (asyncio).Research & Lab Contributors: For mapping network error profiles and documenting execution edge-case criteria.
