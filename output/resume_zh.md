# 吕伟

**资深研发工程师**

- 邮箱：lvw1105@gmail.com
- 所在地：中国
- 语言：中文（母语）| 英文（专业工作）

---

## 个人简介

拥有 8 年以上 Java / React 全栈开发经验，深耕企业级系统架构设计与 AI 驱动开发工具链建设。擅长从零到一设计并落地高并发微服务平台，具备跨团队技术领导力。近年来持续探索 AI 辅助研发效能提升路径，推动工具链标准化，带动团队整体工程质量跃升。熟悉安全通信协议设计、多渲染引擎集成及 DevOps 全流程，能够在业务复杂度与工程质量之间找到最佳平衡点。

---

## 工作经历

### Tsintergy — 资深研发工程师
**2020 年 — 至今 | 中国**

**tsie-tunnel 加密隧道项目（核心负责人）**

主导设计并实现了 tsie-tunnel 安全通信框架，以 AES-CTR 流式加密替代明文 HTTP 传输，从根本上消除内网敏感数据的截获风险。

- **架构设计**：采用分层隧道模型，在应用层与传输层之间插入加密代理，保证对上层业务逻辑完全透明，无需改造既有业务代码即可接入。
- **双渲染引擎支持**：同时集成 JCEF（Java Chromium Embedded Framework）与嵌入式 Firefox（GeckoFx），通过统一抽象接口屏蔽引擎差异，使前端页面可在两套引擎中无缝切换渲染，满足不同终端的部署要求。
- **性能优化**：AES-CTR 模式天然支持并行加解密，经压测在 1 Gbps 内网环境下引入的额外延迟低于 2 ms，吞吐量损耗不超过 3%。
- **安全加固**：引入 IV（初始化向量）随机化机制与会话密钥轮换策略，防止重放攻击与流量分析，通过内部安全审计验收。
- **技术栈**：Java 17、JCEF、GeckoFx、AES-CTR、Netty、Maven

**企业级 Spring Boot 微服务平台**

从单体架构演进出发，主导将核心业务系统拆分为基于 Spring Boot 的微服务架构，显著提升系统可维护性与可扩展性。

- **服务治理**：引入 Spring Cloud Gateway 统一网关，配合 Nacos 实现服务注册、配置中心与动态路由，支撑数百个并发用户的稳定访问。
- **数据层优化**：结合 MySQL 分库分表策略与 Redis 多级缓存，将核心查询接口平均响应时间从 800 ms 压缩至 120 ms，降幅约 85%。
- **可观测性建设**：集成 Micrometer + Prometheus + Grafana 监控体系，配置关键业务指标告警，故障平均发现时间（MTTD）缩短至 3 分钟以内。
- **CI/CD 流水线**：基于 GitHub Actions 构建自动化测试、代码质量扫描（SonarQube）、Docker 镜像构建与 Kubernetes 滚动发布的完整流水线，发布周期从每月 1 次压缩至每周多次。
- **技术栈**：Java 17、Spring Boot 3、Spring Cloud、Nacos、MySQL、Redis、Docker、Kubernetes、GitHub Actions

**AI 辅助开发工具链建设**

作为团队 AI 效能推广负责人，系统性地将 AI 工具引入研发全流程。

- **代码审查提效**：将 Claude API 集成至 GitHub PR 流程，自动对 Diff 进行安全检查、编码规范校验与逻辑缺陷分析，团队代码审查效率提升约 40%，人工审查重点转移至架构层面决策。
- **测试用例生成**：基于 AST 解析 + LLM 生成单元测试骨架，核心模块测试覆盖率从 42% 提升至 78%。
- **知识沉淀**：搭建内部技术知识库，接入 RAG（检索增强生成）能力，新成员上手时间缩短约 30%。
- **技术栈**：Python、Anthropic Claude API、TypeScript、Next.js、GitHub Actions

---

## 技能

| 类别 | 技术 |
|------|------|
| **编程语言** | Java（精通）、TypeScript（熟练）、Python（熟练）、Rust（学习中） |
| **后端框架** | Spring Boot、Spring Cloud、Netty |
| **前端框架** | React、Next.js |
| **数据库** | MySQL、Redis |
| **工具与平台** | Docker、Kubernetes、Git、Maven、GitHub Actions |
| **安全 & 协议** | AES-CTR、TLS/SSL、OAuth2、JWT |
| **可观测性** | Prometheus、Grafana、Micrometer |
| **AI & LLM** | Anthropic Claude API、RAG 架构、Prompt Engineering |

---

## 教育背景

**计算机科学与技术 — 本科**
毕业年份：2015 年

---

## 语言能力

- **中文**：母语
- **英文**：专业工作水平（可独立阅读英文技术文档、参与英文技术讨论）
