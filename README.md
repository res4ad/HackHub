# ⚡ HackHub

<p align="center">
  <img src="https://img.shields.io/badge/Status-Beta-orange?style=for-the-badge&logo=git" alt="Status Beta">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Architecture-AsyncIO-blueviolet?style=for-the-badge&logo=asyncio" alt="Architecture AsyncIO">
  <img src="https://img.shields.io/badge/Developer-res4ad-success?style=for-the-badge&logo=github" alt="Developer res4ad">
</p>

<p align="center">
  <strong>An operator-focused multi-session listener framework for authorized security testing and lab environments.</strong>
</p>

<p align="center">
  Core Architect & Developer: <strong>Reshad Rustemov (@res4ad)</strong>
</p>

<p align="center">
  <a href="https://github.com/res4ad"><img src="https://img.shields.io/badge/GitHub-res4ad-181717?style=flat-square&logo=github" alt="GitHub"></a>
  <a href="https://linkedin.com/in/res4ad"><img src="https://img.shields.io/badge/LinkedIn-res4ad-0A66C2?style=flat-square&logo=linkedin" alt="LinkedIn"></a>
  <a href="https://instagram.com/res4ad"><img src="https://img.shields.io/badge/Instagram-res4ad-E4405F?style=flat-square&logo=instagram" alt="Instagram"></a>
</p>

---

## 📖 Project Overview

**HackHub** is a streamlined, concurrent session handler designed to aggregate incoming shell connections across multiple network ports simultaneously. Built strictly on top of Python's asynchronous I/O (`asyncio`) subsystem by **Reshad Rustemov**, HackHub minimizes interface freezing, handles dynamic data buffers cleanly, and provides defensive testing professionals with a structured dashboard environment to manage interactive links within isolated laboratory settings.

> [!WARNING]  
> **Beta Status Notice:** This framework is currently in active development (**Beta** phase). Breaking architectural changes may occur between commits. It is recommended strictly for isolated training environments and authorized evaluation setups.

---

## 📸 Interface Preview

Below is a mock blueprint of the active core workflow interface.

```text
+------------------------------------------------------------------------+
|                 HACKHUB OPERATOR CONTROL DASHBOARD [v0.5-BETA]          |
+------------------------------------------------------------------------+
| Framework Uptime   : 01:24:12      | Active Session Links : 3          |
| Bound Listen Ports : [1234, 4444]  | Unique Source Hosts  : 2          |
+------------------------------------------------------------------------+
| Linux Platforms    : 2             | Windows Platforms    : 1          |
+------------------------------------------------------------------------+
| ID     NAME          ENDPOINT              PLATFORM        LISTEN_PORT |
| ------ ------------- --------------------- --------------- ----------- |
| a1b2c3 web-prod-01   192.168.1.50:41220    Linux 6.1.0     1234        |
| d4e5f6 staging-db    192.168.1.62:53110    Linux 5.15.0    4444        |
| g7h8i9 win-lab-01    192.168.1.75:49812    Windows_CMD     4444        |
+------------------------------------------------------------------------+
[>] Options: [1] Session Matrix | [2] Local Intelligence Notes | [Q] Return
✨ Features Matrix⚙️ Core ArchitectureMulti-Port Concurrent Listeners: Spin up individual asynchronous network sockets across variable structural ports under a singular management loop.Deterministic Input Multiplexer: Navigate smoothly between granular TUI control maps and live shell interaction lines without interface locks.Non-Blocking Execution Model: Network dropouts or high-density byte arrays from one terminal node will not bottleneck adjacent connections.🛠️ Session ManagementCustom Alias Mapping: Rename raw random UUID descriptors to meaningful environmental labels (e.g., web-prod-01, dc-01).Isolated Analytical Logging: Every event—including connect sequences, timestamps, transmitted input strings, and disconnect loops—is cleanly documented within individual text frames on disk.Localized Session Notes Ledger: Pin real-time field annotations (vulnerabilities discovered, configuration states, credentials validated) directly onto an individual active tunnel context.📊 Feature Comparison MatrixManagement CapabilityTraditional Soket Listeners (nc)Multiplexed Managers (screen / tmux)HackHub Framework CoreSimultaneous Ports❌ (1 Port per instance)❌ (Requires manually bound panes)(Native Asynchronous Loop)Unified Status Dashboard❌❌(Real-Time Statistics)Isolated Session Logging❌ (Manual redirection required)⚠️ (Terse transcript captures)(Structured Event Loggers)Inline Protocol Commands❌❌(Escape Mode Interactivity)Session Tracking Notes❌❌(Per-Session RAM Ledger)🖥️ Supported EnvironmentsOperating SystemDistribution AlignmentFunctional TierLinux CoreKali Linux, Debian Mappings, Ubuntu LTSFull Native SupportWindows SubsystemMicrosoft Windows CMD Core⚠️ Experimental Tier⚙️ InstallationEnsure you have Python 3.9 or higher installed on your host system.Bash# Clone the remote asset repository
git clone [https://github.com/res4ad/hackhub.git](https://github.com/res4ad/hackhub.git)
cd hackhub

# Verify python deployment version alignment
python3 --version

# Run the framework pipeline directly (Utilizes standard standard libraries)
python3 listener.py --help
⚡ Quick Start & Usage Examples1. View Parameter Commands Help MenuBashpython3 listener.py --help
2. Bind Listener to a Default/Single Network PortBashpython3 listener.py -p 4444
3. Deploy Multi-Port Matrix BindingBashpython3 listener.py --port 1234,4444,8080
🕹️ Active Interface & Protocol DirectivesWhile engaged inside a live session interaction terminal, the operator can pass dynamic escape tokens to manipulate the underlying control matrix directly:📍 Inline Interactivity CommandsCommand DirectiveFunctional Impact Description:sessionsOutputs a quick structured inline listing of all currently active network pipes.:switch <id/name>Rotates input routing context immediately to the specified terminal target.:addnote <text>Appends a text annotation record directly to the current runtime tracking asset.:notesPrints a full timeline dump of all localized notes collected for this specific host.Ctrl + ADisengages from current terminal and brings forward the central Control Dashboard Menu.When inside the Central Console Dashboard Panel, navigate utilizing standardized macro keystrokes:ESC -> Instantly closes panel layouts and drops input focus straight back down to active shell lines.Ctrl + C -> Safely dismisses the menu display overlay without dropping connections or altering runtime state.Q -> Moves back exactly one menu hierarchy tier.🗂️ Analytics & Logging Framework StructureThe listener engine automatically provisions a persistent tracking structure inside the runtime workspace path:Plaintextlogs/
├── session_a1b2c3.log  <-- Contains granular network events, connect sequences & traffic logs
├── session_d4e5f6.log
└── system_audit.log    <-- Tracks general handler exceptions & framework initialization
Operators can inspect active transmission transcripts inside the Dashboard panel via Option [4] (Telemetry Log Viewer), or pass filtering flags (by string keyword / by specific session context) to locate targeted transaction anomalies.🗺️ Engineering Development RoadmapCompleted Milestones (v0.5)[x] Asynchronous multi-port listening pipeline engine loop architecture.[x] Contextual console interaction interface abstraction layers.[x] Real-time diagnostic statistics compute module dashboard matrix.[x] White-listed file payload transfer handlers with verification checksum validation.Upcoming Implementations (v1.0)[ ] TLS encapsulation layering option for secure inter-lab connection transport.[ ] Localized configuration template storage engine file parsing support.[ ] Tab-completion support for interactive inner-session filesystem navigation.[ ] Export module to parse session note databases into raw JSON reports.⚠️ Security Notice[!IMPORTANT]HackHub is designed exclusively for educational research, laboratory testing, and fully authorized internal validation exercises. Usage of this software for unauthorized access, tampering, or malicious interaction with data infrastructure is strictly prohibited. The authors and project contributors assume zero liability for downstream architectural damage or infrastructural misuse resulting from altered deployments of this codebase.🤝 ContributingContributions to improve stability, fix edge-case parsing exceptions, or build out robust tracking reporting functions are welcome. Please adhere to these guidelines:Fork the codebase repository (github.com/res4ad/hackhub).Form an independent branch detailing tracking changes (git checkout -b feature/StableFix).Commit adjustments with verbose informational summaries.Issue a detailed Pull Request back to the main repository pipeline.📄 LicenseThis framework architecture is distributed completely open-source under the strict legal terms of the MIT License.👥 Developer & AcknowledgmentsLead Developer: Reshad Rustemov (@res4ad) - Core architecture and asynchronous engine implementation.Python Standard Library Contributors: For providing robust asynchronous engine frameworks (asyncio).Open Source Testing Community: For continuously refining laboratory tooling paradigms and contributing architecture edge-case reports.
