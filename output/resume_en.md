# Wei Lv (吕伟)

**Senior Software Engineer**

- Email: lvw1105@gmail.com
- Location: China
- Languages: Chinese (Native) | English (Professional Working)

---

## Professional Summary

Senior full-stack engineer with 8+ years of hands-on experience designing and delivering enterprise-grade systems across the Java and React ecosystems. Proven track record of leading zero-to-one architecture initiatives — from encrypted communication tunnels to high-throughput microservice platforms — while maintaining a strong focus on engineering quality, observability, and developer productivity.

A strong advocate for AI-augmented development, having systematically integrated large language models into code review, test generation, and knowledge management workflows, achieving measurable efficiency gains across the engineering team. Currently deepening expertise in systems programming with Rust to expand low-level performance optimization capabilities.

---

## Work Experience

### Tsintergy — Senior Software Engineer
**2020 – Present | China**

**tsie-tunnel: Encrypted Communication Tunnel (Technical Lead)**

Led the end-to-end design and implementation of tsie-tunnel, a transparent AES-CTR encrypted tunnel that replaces plaintext HTTP communication for sensitive internal traffic. The solution required zero changes to existing application business logic.

- **Architecture**: Designed a layered proxy model inserted between the application and transport layers, abstracting encryption concerns behind a unified interface and enabling seamless adoption across existing services.
- **Dual Render-Engine Support**: Integrated both JCEF (Java Chromium Embedded Framework) and embedded Firefox (GeckoFx) with a common abstraction layer, allowing front-end pages to switch rendering engines at deployment time — supporting diverse client environments without code duplication.
- **Performance**: AES-CTR's native parallelism kept encryption overhead below 2 ms additional latency and under 3% throughput reduction at 1 Gbps on internal networks (verified under load testing).
- **Security Hardening**: Implemented randomized IV generation and session key rotation to defend against replay attacks and traffic analysis; passed internal security audit without findings.
- **Stack**: Java 17, JCEF, GeckoFx, AES-CTR, Netty, Maven

**Enterprise Spring Boot Microservices Platform**

Spearheaded the decomposition of a legacy monolith into a cloud-native microservices architecture, dramatically improving scalability, maintainability, and release velocity.

- **Service Governance**: Deployed Spring Cloud Gateway as the unified API gateway with Nacos for service discovery, configuration management, and dynamic routing — supporting hundreds of concurrent users under peak load.
- **Data Layer Optimization**: Combined MySQL sharding with multi-layer Redis caching, reducing average response time for core query APIs from ~800 ms to ~120 ms (85% improvement).
- **Observability**: Built a Micrometer + Prometheus + Grafana monitoring stack with business-critical alerting rules, reducing Mean Time to Detect (MTTD) for incidents to under 3 minutes.
- **CI/CD Pipeline**: Automated the full delivery pipeline with GitHub Actions — unit tests, SonarQube code quality gates, Docker image builds, and Kubernetes rolling deployments — compressing release cadence from monthly to multiple times per week.
- **Stack**: Java 17, Spring Boot 3, Spring Cloud, Nacos, MySQL, Redis, Docker, Kubernetes, GitHub Actions

**AI-Augmented Development Toolchain**

Served as the internal champion for AI-assisted engineering, systematically embedding LLM capabilities across the development lifecycle.

- **Code Review Acceleration**: Integrated the Claude API into the GitHub PR workflow to automatically analyze diffs for security issues, coding standards violations, and logic defects — boosting team code review throughput by approximately 40% and shifting human review focus to higher-level architectural decisions.
- **Test Generation**: Combined AST-based code parsing with LLM-generated unit test scaffolding, lifting core module test coverage from 42% to 78%.
- **Internal Knowledge Base**: Built a RAG-powered (Retrieval-Augmented Generation) internal knowledge system, reducing new engineer onboarding time by roughly 30%.
- **Stack**: Python, Anthropic Claude API, TypeScript, Next.js, GitHub Actions

---

## Skills

| Category | Technologies |
|----------|-------------|
| **Languages** | Java (Expert), TypeScript (Proficient), Python (Proficient), Rust (Learning) |
| **Backend** | Spring Boot, Spring Cloud, Netty |
| **Frontend** | React, Next.js |
| **Databases** | MySQL, Redis |
| **DevOps & Tooling** | Docker, Kubernetes, Git, Maven, GitHub Actions |
| **Security & Protocols** | AES-CTR, TLS/SSL, OAuth2, JWT |
| **Observability** | Prometheus, Grafana, Micrometer |
| **AI & LLM** | Anthropic Claude API, RAG Architecture, Prompt Engineering |

---

## Education

**Bachelor of Science — Computer Science and Technology**
Graduation Year: 2015

---

## Languages

- **Chinese**: Native
- **English**: Professional working proficiency (independent reading of technical documentation; participation in technical discussions)
