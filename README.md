# YTU-DEPTRON

[![SAC to drive Carla and cabin display SDV for Eclipse SDV Hackathon Chapter Three](https://img.youtube.com/vi/FyUjJ6R4yQk/0.jpg)](https://www.youtube.com/watch?v=FyUjJ6R4yQk)

# 1. Your Team at a Glance

YTU-Deptron / Not Just Robotics It's Deptron

<img width="1080" height="1080" alt="image" src="https://github.com/user-attachments/assets/d52621d2-04f0-4aef-88a6-4312e925cec4" />


## Team Members  
| Name | GitHub Handle | Role(s) |
|-------|---------------|---------|
| Meryem Koc | [codermery](https://github.com/codermery) | hacker |
| Ugur Aydin | [uguray75](https://github.com/uguray75) | GUI |
| Rıchard Meınsen | [hackathon-develop](https://github.com/hackathon-develop)  | hacker |
| Murat Murat | [muratmurat34](https://github.com/muratmurat34) | GUI |
| Juan Pizarro | [jpizarrom](https://github.com/jpizarrom) | hacker |

## Challenge  
Lab Challenge

## Core Idea  
**“Control Everything at Once”** – an integrated feature controller that unifies different ADAS modules (cruise control, lane monitoring, and emergency response) into a single orchestrated system using the SDV Lab ecosystem.

Instead of building one isolated feature, our prototype will demonstrate how multiple features can interact through a shared communication backbone (uProtocol, MQTT, or Zenoh), orchestrated by Ankaios, and tested in the CARLA simulator with a connected Android GUI cluster.

We want to showcase how different ADAS components can run in parallel, exchange signals, and still be managed and visualized coherently by developers and drivers alike.

---

# 2. How Do You Work

## Development Process  

We adopt a hybrid exploratory and structured approach:

**Exploration & Rapid Prototyping:** Each hacker experiments with small proof-of-concepts (e.g., Python PID controller, Rust + uProtocol integration, Android visualization).

**Integration Phase:** Components are containerized with Podman and orchestrated using Ankaios for deployment consistency.

**Simulation & Testing:** Features are validated in the CARLA simulator, then visualized through an PyQt.

This ensures both speed during the hackathon and technical robustness for demonstration.

### Planning & Tracking  

GitHub will be used to host source code, track issues, and manage pull requests.

We plan short sync meetings to align priorities and assign tasks.

Milestones are tied to key features (first data exchange, first GUI visualization, full orchestration).

### Quality Assurance  

**Code Reviews:** At least one teammate reviews each merge request.

**Containerized Testing:** Each workload will be tested in isolation before cluster integration.

**Simulation Runs:** Frequent CARLA scenario testing to validate correctness under different traffic and environment conditions.

**Debugging Tools:** Using ank logs and CARLA debug sensors to trace data flow.

## Communication  

We use translation tools like DeepL to bridge communication gaps across different native languages.

## Decision Making  

Decisions are collaborative: proposals are discussed briefly, then agreed by majority.
