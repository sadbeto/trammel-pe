"""
Trammel PE — Core prompt generation engine.

Pure Python reimplementation of the Trammel PE HTML tool's buildPrompt() logic.
No browser, no dependencies — just structured prompts.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
import json
import re

# ── Language maps ──────────────────────────────────────────────────────────

LANG = {
    "en": {
        "pObjective": "Objective",
        "pRole": "Role & Tone",
        "pSuccess": "Success Criteria",
        "pScope": "Scope",
        "pInScope": "In Scope",
        "pOutScope": "Out of Scope",
        "pDepth": "Depth",
        "pTools": "Tools",
        "pToolsDesc": "Use the following tools to complete this task:",
        "pDecomposition": "Task Decomposition",
        "pDecompDesc": "Break the objective into focused sub-tasks. Execute each with concentrated data.",
        "pSubtask": "Sub-task",
        "pDataFocus": "Data focus",
        "pContext": "Context & Data",
        "pBackground": "Background",
        "pInputData": "Input Data",
        "pAudience": "Target Audience",
        "pFormat": "Output Format",
        "pFormatLabel": "Format",
        "pLength": "Length",
        "pCustomFormat": "Custom format instructions:",
        "pConstraints": "Constraints",
        "pMust": "MUST DO",
        "pMustNot": "MUST NOT",
        "pEdgeCases": "Edge Cases",
        "pSelfLearn": "Self-Learning Loop",
        "pStrategy": "Strategy",
        "pMaxIter": "Max iterations",
        "pFocus": "Focus:",
        # Depth labels
        "s2DepthQuick": "Quick overview",
        "s2DepthStd": "Standard analysis",
        "s2DepthDeep": "Deep dive",
        "s2DepthExp": "Expert-level analysis",
        # Tone labels
        "s5TonePro": "Professional",
        "s5ToneConcise": "Concise",
        "s5ToneAcademic": "Academic",
        "s5ToneCreative": "Creative",
        "s5ToneConv": "Conversational",
        "s5ToneTech": "Technical",
        "s5ToneExec": "Executive",
        # Format labels
        "s6FmtMd": "Markdown",
        "s6FmtJson": "JSON",
        "s6FmtTable": "Table",
        "s6FmtBullets": "Bullet list",
        "s6FmtNarrative": "Narrative",
        "s6FmtCode": "Code",
        "s6FmtMixed": "Mixed (Markdown + code + tables)",
        # Length labels
        "lenBrief": "Brief (<500 words)",
        "lenModerate": "Moderate (500-1500 words)",
        "lenComprehensive": "Comprehensive (1500-3000 words)",
        "lenUnlimited": "No length limit",
        # Iteration labels
        "s9IterReflect": "Reflect on output quality",
        "s9IterValidate": "Validate against success criteria",
        "s9IterResearch": "Research and fill gaps",
        "s9IterAll": "All strategies (reflect + validate + research)",
        # Tool labels
        "tWebSearch": "Web Search",
        "tCodeExec": "Code Execution",
        "tFileRW": "File Read/Write",
        "tApiCalls": "API Calls",
        "tDataAnalysis": "Data Analysis",
        "tBrowser": "Browser Automation",
        "tDatabase": "Database",
        "tShell": "Shell/Terminal",
        "tImageGen": "Image Generation",
        "tDocProcess": "Document Processing",
        "tScheduling": "Scheduling/Cron",
        "tMemory": "Memory/Vector DB",
        # Self-learning loop steps
        "loopStep1": "Reflect on your initial output. Identify weaknesses, gaps, or ambiguities.",
        "loopStep2a": "Research additional information to fill identified gaps.",
        "loopStep2b": "Validate your output against the success criteria.",
        "loopStep3": "Revise and improve the output based on findings from steps 1-2.",
        "loopStep4": "Repeat up to {n} iterations, or stop when output meets all success criteria.",
        "youAre": "You are",
        "tone": "Tone",
    },
    "es": {
        "pObjective": "Objetivo",
        "pRole": "Rol y Tono",
        "pSuccess": "Criterios de Éxito",
        "pScope": "Alcance",
        "pInScope": "Dentro del Alcance",
        "pOutScope": "Fuera del Alcance",
        "pDepth": "Profundidad",
        "pTools": "Herramientas",
        "pToolsDesc": "Usa las siguientes herramientas para completar esta tarea:",
        "pDecomposition": "Descomposición de Tareas",
        "pDecompDesc": "Descompón el objetivo en subtareas enfocadas. Ejecuta cada una con datos concentrados.",
        "pSubtask": "Subtarea",
        "pDataFocus": "Datos de enfoque",
        "pContext": "Contexto y Datos",
        "pBackground": "Antecedentes",
        "pInputData": "Datos de Entrada",
        "pAudience": "Audiencia Objetivo",
        "pFormat": "Formato de Salida",
        "pFormatLabel": "Formato",
        "pLength": "Longitud",
        "pCustomFormat": "Instrucciones de formato personalizado:",
        "pConstraints": "Restricciones",
        "pMust": "DEBE HACER",
        "pMustNot": "NO DEBE HACER",
        "pEdgeCases": "Casos Límite",
        "pSelfLearn": "Bucle de Auto-Aprendizaje",
        "pStrategy": "Estrategia",
        "pMaxIter": "Iteraciones máximas",
        "pFocus": "Enfoque:",
        "s2DepthQuick": "Vista rápida",
        "s2DepthStd": "Análisis estándar",
        "s2DepthDeep": "Análisis profundo",
        "s2DepthExp": "Análisis experto",
        "s5TonePro": "Profesional",
        "s5ToneConcise": "Conciso",
        "s5ToneAcademic": "Académico",
        "s5ToneCreative": "Creativo",
        "s5ToneConv": "Conversacional",
        "s5ToneTech": "Técnico",
        "s5ToneExec": "Ejecutivo",
        "s6FmtMd": "Markdown",
        "s6FmtJson": "JSON",
        "s6FmtTable": "Tabla",
        "s6FmtBullets": "Lista de viñetas",
        "s6FmtNarrative": "Narrativo",
        "s6FmtCode": "Código",
        "s6FmtMixed": "Mixto (Markdown + código + tablas)",
        "lenBrief": "Breve (<500 palabras)",
        "lenModerate": "Moderado (500-1500 palabras)",
        "lenComprehensive": "Comprensivo (1500-3000 palabras)",
        "lenUnlimited": "Sin límite de longitud",
        "s9IterReflect": "Reflexionar sobre la calidad de la salida",
        "s9IterValidate": "Validar contra los criterios de éxito",
        "s9IterResearch": "Investigar y llenar vacíos",
        "s9IterAll": "Todas las estrategias (reflexionar + validar + investigar)",
        "tWebSearch": "Búsqueda Web",
        "tCodeExec": "Ejecución de Código",
        "tFileRW": "Lectura/Escritura de Archivos",
        "tApiCalls": "Llamadas API",
        "tDataAnalysis": "Análisis de Datos",
        "tBrowser": "Automatización de Navegador",
        "tDatabase": "Base de Datos",
        "tShell": "Shell/Terminal",
        "tImageGen": "Generación de Imágenes",
        "tDocProcess": "Procesamiento de Documentos",
        "tScheduling": "Programación/Cron",
        "tMemory": "Memoria/Vector DB",
        "loopStep1": "Reflexiona sobre tu salida inicial. Identifica debilidades, vacíos o ambigüedades.",
        "loopStep2a": "Investiga información adicional para llenar los vacíos identificados.",
        "loopStep2b": "Valida tu salida contra los criterios de éxito.",
        "loopStep3": "Revisa y mejora la salida basándote en los hallazgos de los pasos 1-2.",
        "loopStep4": "Repite hasta {n} iteraciones, o detente cuando la salida cumpla todos los criterios de éxito.",
        "youAre": "Eres",
        "tone": "Tono",
    },
    "pt": {
        "pObjective": "Objetivo",
        "pRole": "Papel e Tom",
        "pSuccess": "Critérios de Sucesso",
        "pScope": "Escopo",
        "pInScope": "Dentro do Escopo",
        "pOutScope": "Fora do Escopo",
        "pDepth": "Profundidade",
        "pTools": "Ferramentas",
        "pToolsDesc": "Use as seguintes ferramentas para completar esta tarefa:",
        "pDecomposition": "Decomposição de Tarefas",
        "pDecompDesc": "Decomponha o objetivo em subtarefas focadas. Execute cada uma com dados concentrados.",
        "pSubtask": "Subtarefa",
        "pDataFocus": "Foco de dados",
        "pContext": "Contexto e Dados",
        "pBackground": "Contexto",
        "pInputData": "Dados de Entrada",
        "pAudience": "Público-Alvo",
        "pFormat": "Formato de Saída",
        "pFormatLabel": "Formato",
        "pLength": "Comprimento",
        "pCustomFormat": "Instruções de formato personalizado:",
        "pConstraints": "Restrições",
        "pMust": "DEVE FAZER",
        "pMustNot": "NÃO DEVE FAZER",
        "pEdgeCases": "Casos Limite",
        "pSelfLearn": "Loop de Auto-Aprendizado",
        "pStrategy": "Estratégia",
        "pMaxIter": "Iterações máximas",
        "pFocus": "Foco:",
        "s2DepthQuick": "Visão rápida",
        "s2DepthStd": "Análise padrão",
        "s2DepthDeep": "Análise profunda",
        "s2DepthExp": "Análise especializada",
        "s5TonePro": "Profissional",
        "s5ToneConcise": "Conciso",
        "s5ToneAcademic": "Acadêmico",
        "s5ToneCreative": "Criativo",
        "s5ToneConv": "Conversacional",
        "s5ToneTech": "Técnico",
        "s5ToneExec": "Executivo",
        "s6FmtMd": "Markdown",
        "s6FmtJson": "JSON",
        "s6FmtTable": "Tabela",
        "s6FmtBullets": "Lista de marcadores",
        "s6FmtNarrative": "Narrativo",
        "s6FmtCode": "Código",
        "s6FmtMixed": "Misto (Markdown + código + tabelas)",
        "lenBrief": "Breve (<500 palavras)",
        "lenModerate": "Moderado (500-1500 palavras)",
        "lenComprehensive": "Abrangente (1500-3000 palavras)",
        "lenUnlimited": "Sem limite de comprimento",
        "s9IterReflect": "Refletir sobre a qualidade da saída",
        "s9IterValidate": "Validar contra os critérios de sucesso",
        "s9IterResearch": "Pesquisar e preencher lacunas",
        "s9IterAll": "Todas as estratégias (refletir + validar + pesquisar)",
        "tWebSearch": "Pesquisa Web",
        "tCodeExec": "Execução de Código",
        "tFileRW": "Leitura/Escrita de Arquivos",
        "tApiCalls": "Chamadas API",
        "tDataAnalysis": "Análise de Dados",
        "tDataba": "Banco de Dados",
        "tShell": "Shell/Terminal",
        "tImageGen": "Geração de Imagens",
        "tDocProcess": "Processamento de Documentos",
        "tScheduling": "Agendamento/Cron",
        "tMemory": "Memória/Vector DB",
        "loopStep1": "Refleta sobre sua saída inicial. Identifique fraquezas, lacunas ou ambiguidades.",
        "loopStep2a": "Pesquise informações adicionais para preencher as lacunas identificadas.",
        "loopStep2b": "Valide sua saída contra os critérios de sucesso.",
        "loopStep3": "Revise e melhore a saída com base nas descobertas dos passos 1-2.",
        "loopStep4": "Repita até {n} iterações, ou pare quando a saída atender a todos os critérios de sucesso.",
        "youAre": "Você é",
        "tone": "Tom",
    },
}


# ── Built-in templates ─────────────────────────────────────────────────────

TEMPLATES = {
    "competitive": {
        "objective": "Analyze the competitive landscape for a SaaS startup offering AI-powered customer support automation in Latin America",
        "domain": "Marketing & Growth",
        "success_criteria": "A prioritized list of 5-7 competitors with revenue estimates, funding stage, key differentiators, and a positioning map",
        "in_scope": "LATAM market, companies >$1M ARR, AI/ML products, direct and indirect competitors",
        "out_scope": "Companies with no AI, markets outside LATAM, <$500K ARR",
        "depth": "deep",
        "tone": "professional",
        "format_type": "mixed",
        "length_target": "comprehensive",
        "role": "Senior competitive intelligence analyst with 10+ years in LATAM SaaS markets",
        "must_do": "Include revenue estimates with confidence levels. Cite sources. Provide a positioning matrix.",
        "tools": ["web_search", "data_analysis"],
        "subtasks": [
            {"name": "Identify Competitors", "desc": "Find all relevant competitors in the space", "data": "Competitor sites, G2/Capterra, funding databases"},
            {"name": "Analyze Positioning", "desc": "Map each competitor: price, features, segment", "data": "Pricing pages, feature tables, reviews"},
        ],
    },
    "data-analysis": {
        "objective": "Explore a sales dataset to identify revenue drivers and deliver actionable insights with visualizations",
        "domain": "Data Science & Analytics",
        "success_criteria": "Top 3-5 revenue drivers identified with statistical support, plus 3+ charts and a prioritized recommendation list",
        "in_scope": "Provided dataset only, descriptive + correlation analysis, segment breakdowns",
        "out_scope": "External data sources, causal claims without experiment, predictive modeling unless asked",
        "depth": "standard",
        "tone": "technical",
        "format_type": "mixed",
        "length_target": "moderate",
        "role": "Senior data analyst fluent in Python/pandas and statistical reasoning",
        "must_do": "State assumptions. Quantify findings. Flag data quality issues. Charts must have labeled axes.",
        "tools": ["code_execution", "data_analysis", "file_read_write"],
        "subtasks": [
            {"name": "Profile & Clean", "desc": "Inspect schema, types, missing values, outliers", "data": "Column dtypes, null counts, distributions"},
            {"name": "Find Drivers", "desc": "Correlation + segment analysis vs revenue", "data": "Correlation matrix, groupby aggregates"},
        ],
    },
    "content-writing": {
        "objective": "Write an SEO-optimized long-form blog post that ranks for a target keyword and converts readers",
        "domain": "Creative & Content",
        "success_criteria": "A 1500+ word post with H2/H3 structure, target keyword in title/intro/headers, meta description, and a clear CTA",
        "in_scope": "One primary keyword + 3-5 secondary, internal linking suggestions, reader-first tone",
        "out_scope": "Keyword stuffing, fabricated stats, plagiarized content",
        "depth": "standard",
        "tone": "conversational",
        "format_type": "markdown",
        "length_target": "comprehensive",
        "role": "Senior content strategist and SEO copywriter",
        "must_do": "Keyword in first 100 words. Scannable structure. Original examples. End with a CTA.",
        "tools": ["web_search"],
        "subtasks": [
            {"name": "Outline", "desc": "Build an H2/H3 outline around search intent", "data": "SERP analysis, related questions"},
            {"name": "Draft & Optimize", "desc": "Write the post and weave keywords naturally", "data": "Keyword list, brand voice notes"},
        ],
    },
    "api-design": {
        "objective": "Design a REST API for a multi-tenant task management app with auth, schemas, and error handling",
        "domain": "Software Engineering",
        "success_criteria": "OpenAPI-style endpoint list, request/response schemas, auth flow, status codes, and pagination strategy",
        "in_scope": "CRUD for tasks/projects/users, JWT auth, RBAC, rate limiting, versioning",
        "out_scope": "Frontend, deployment infra, billing system",
        "depth": "deep",
        "tone": "technical",
        "format_type": "mixed",
        "length_target": "comprehensive",
        "role": "Senior backend architect specializing in API design and security",
        "must_do": "Use consistent naming. Define error envelope. Specify auth on every endpoint. Include rate limit headers.",
        "tools": ["code_execution", "file_read_write"],
        "subtasks": [
            {"name": "Resource Model", "desc": "Define entities, relationships, and schemas", "data": "Entity fields, constraints, tenant isolation"},
            {"name": "Endpoints & Auth", "desc": "Map routes, methods, auth scopes, and errors", "data": "Route table, JWT claims, status codes"},
        ],
    },
    "code-review": {
        "objective": "Review a pull request for bugs, security issues, performance, and maintainability",
        "domain": "Software Engineering",
        "success_criteria": "Categorized findings (blocker/major/minor/nit) with file:line refs and concrete fix suggestions",
        "in_scope": "Logic, security, performance, readability, test coverage of the diff",
        "out_scope": "Unrelated files, style nitpicks already enforced by linters, architecture rewrites",
        "depth": "deep",
        "tone": "concise",
        "format_type": "mixed",
        "length_target": "moderate",
        "role": "Senior engineer doing a rigorous but constructive code review",
        "must_do": "Reference file:line. Explain why, not just what. Suggest a fix. Separate blockers from nits.",
        "tools": ["code_execution", "file_read_write"],
        "subtasks": [
            {"name": "Correctness & Security", "desc": "Hunt logic bugs, injection, auth gaps, unsafe input", "data": "Diff hunks, data flow, trust boundaries"},
            {"name": "Maintainability", "desc": "Assess naming, structure, tests, and docs", "data": "Complexity, duplication, test coverage"},
        ],
    },
    "security-audit": {
        "objective": "Audit a web application for common vulnerabilities and recommend prioritized remediations",
        "domain": "Cybersecurity",
        "success_criteria": "Findings mapped to OWASP Top 10 with severity (CVSS-ish), evidence, and a prioritized fix plan",
        "in_scope": "Authn/authz, injection, XSS, CSRF, secrets handling, dependency risks, access control",
        "out_scope": "Active exploitation, DoS testing, social engineering, physical security",
        "depth": "expert",
        "tone": "professional",
        "format_type": "mixed",
        "length_target": "comprehensive",
        "role": "Application security engineer focused on defensive review (not active exploitation)",
        "must_do": "Map to OWASP. Rate severity. Provide evidence. Recommend least-privilege fixes. No live exploitation.",
        "edge_cases": "Defensive analysis only — do not run exploits against live systems",
        "tools": ["code_execution", "file_read_write", "web_search"],
        "subtasks": [
            {"name": "Surface Mapping", "desc": "Map inputs, auth flows, and trust boundaries", "data": "Routes, params, session handling, dependencies"},
            {"name": "Findings & Fixes", "desc": "Document vulns by severity with remediations", "data": "OWASP categories, code refs, fix steps"},
        ],
    },
}


# ── Data model ─────────────────────────────────────────────────────────────

# Quality Scoring v2 heuristics — keep in sync with computeQuality() in index.html
_QS_ACTION_VERBS = re.compile(
    r"^(analyze|analiza|analise|build|construye|construa|write|escribe|escreva"
    r"|create|crea|crie|design|dise|projete|review|revisa|revise|audit|audita|audite"
    r"|summarize|resume|resuma|generate|genera|gere|develop|desarrolla|desenvolva"
    r"|implement|implementa|implemente|evaluate|eval|avalie|compare|compara"
    r"|research|investiga|pesquise|plan|planifica|planeje|debug|depura|depure"
    r"|refactor|refactoriza|refatore|test|prueba|teste|document|documenta|documente"
    r"|translate|traduce|traduza|optimize|optimiza|otimize|identify|identifica|identifique"
    r"|extract|extrae|extraia|draft|redacta|rascunhe|fix|arregla|corrige|corrija"
    r"|map|mapea|mapeie|define|definir?)", re.IGNORECASE)
_QS_VAGUE_WORDS = re.compile(
    r"\b(etc\.?|stuff|things?|whatever|something|cosas?|algo|cualquier cosa"
    r"|coisas?|alguma? coisa|qualquer coisa)\b", re.IGNORECASE)
_QS_MEASURABLE = re.compile(
    r"\d+|\b(all|each|every|per|at least|at most|todos?|todas?|cada|al menos"
    r"|como m[íi]nimo|m[áa]ximo|cada um|pelo menos|no m[áa]ximo)\b", re.IGNORECASE)


@dataclass
class PromptData:
    """Structured input for Trammel PE prompt generation."""
    objective: str = ""
    domain: str = ""
    success_criteria: str = ""
    in_scope: str = ""
    out_scope: str = ""
    depth: str = "standard"          # quick | standard | deep | expert
    role: str = ""
    tone: str = "professional"        # professional | concise | academic | creative | conversational | technical | executive
    tools: list = field(default_factory=list)
    subtasks: list = field(default_factory=list)  # [{name, desc, data}]
    format_type: str = "markdown"     # markdown | json | table | bulletlist | narrative | code | mixed
    length_target: str = "moderate"   # brief | moderate | comprehensive | unlimited
    background: str = ""
    input_data: str = ""
    audience: str = ""
    constraints: str = ""
    must_do: str = ""
    edge_cases: str = ""
    self_learn: bool = False
    iteration_strategy: str = "reflect"  # reflect | validate | research_more | all
    max_iterations: int = 3
    improvement_focus: str = ""
    lang: str = "en"                  # en | es | pt

    # Allow tools as comma-separated string or list
    def __post_init__(self):
        if isinstance(self.tools, str):
            self.tools = [t.strip() for t in self.tools.split(",") if t.strip()]
        # Normalize subtask dicts
        normalized = []
        for st in self.subtasks:
            if isinstance(st, dict):
                normalized.append(st)
            elif isinstance(st, str):
                normalized.append({"name": st, "desc": "", "data": ""})
        self.subtasks = normalized

    def quality(self) -> dict:
        """Quality Scoring v2 — mirrors computeQuality() in index.html.

        Returns {completeness, specificity, tips} where tips are i18n keys
        (qTipVerb, qTipMeasure, qTipVague, qTipScope, qTipSubtasks).
        """
        fields = [self.objective, self.success_criteria, self.in_scope,
                  self.out_scope, self.role, self.background,
                  self.constraints, self.must_do]
        filled = sum(1 for f in fields if f and len(f.strip()) > 10)
        completeness = round((filled / len(fields)) * 100)

        spec_fields = [self.success_criteria, self.in_scope, self.out_scope,
                       self.constraints, self.must_do, self.edge_cases]
        spec_filled = sum(1 for f in spec_fields if f and len(f.strip()) > 20)
        spec = (spec_filled / len(spec_fields)) * 60  # base: 60 pts

        tips = []

        # Signal 1: objective starts with an action verb (+10)
        if self.objective and _QS_ACTION_VERBS.match(self.objective.strip()):
            spec += 10
        elif self.objective and len(self.objective.strip()) > 10:
            tips.append("qTipVerb")

        # Signal 2: success criteria is measurable (+10)
        if self.success_criteria and _QS_MEASURABLE.search(self.success_criteria):
            spec += 10
        elif self.success_criteria and len(self.success_criteria.strip()) > 10:
            tips.append("qTipMeasure")

        # Signal 3: no vague filler words (+5)
        if not _QS_VAGUE_WORDS.search((self.objective or "") + " " + (self.success_criteria or "")):
            spec += 5
        else:
            tips.append("qTipVague")

        # Signal 4: scope balance (+10)
        in_ok = self.in_scope and len(self.in_scope.strip()) > 10
        out_ok = self.out_scope and len(self.out_scope.strip()) > 10
        if in_ok and out_ok:
            spec += 10
        elif (self.in_scope and self.in_scope.strip()) or (self.out_scope and self.out_scope.strip()):
            tips.append("qTipScope")

        # Signal 5: at least one real subtask (+5)
        if any(st.get("name") and st.get("desc") for st in self.subtasks):
            spec += 5
        elif completeness >= 40:
            tips.append("qTipSubtasks")

        return {
            "completeness": completeness,
            "specificity": min(100, round(spec)),
            "tips": tips[:3],
        }


# ── Tool name resolver ─────────────────────────────────────────────────────

TOOL_NAMES = {
    "web_search": {"en": "Web Search", "es": "Búsqueda Web", "pt": "Pesquisa Web"},
    "code_execution": {"en": "Code Execution", "es": "Ejecución de Código", "pt": "Execução de Código"},
    "file_read_write": {"en": "File Read/Write", "es": "Lectura/Escritura de Archivos", "pt": "Leitura/Escrita de Arquivos"},
    "api_calls": {"en": "API Calls", "es": "Llamadas API", "pt": "Chamadas API"},
    "data_analysis": {"en": "Data Analysis", "es": "Análisis de Datos", "pt": "Análise de Dados"},
    "browser_automation": {"en": "Browser Automation", "es": "Automatización de Navegador", "pt": "Automação de Navegador"},
    "database": {"en": "Database", "es": "Base de Datos", "pt": "Banco de Dados"},
    "shell_terminal": {"en": "Shell/Terminal", "es": "Shell/Terminal", "pt": "Shell/Terminal"},
    "image_generation": {"en": "Image Generation", "es": "Generación de Imágenes", "pt": "Geração de Imagens"},
    "document_processing": {"en": "Document Processing", "es": "Procesamiento de Documentos", "pt": "Processamento de Documentos"},
    "scheduling_cron": {"en": "Scheduling/Cron", "es": "Programación/Cron", "pt": "Agendamento/Cron"},
    "memory_vector_db": {"en": "Memory/Vector DB", "es": "Memoria/Vector DB", "pt": "Memória/Vector DB"},
}


def tool_name(tool_id: str, lang: str = "en") -> str:
    """Resolve a tool ID to its localized name."""
    if tool_id in TOOL_NAMES:
        return TOOL_NAMES[tool_id].get(lang, TOOL_NAMES[tool_id]["en"])
    return tool_id


# ── Depth/tone/format/length labels ───────────────────────────────────────

DEPTH_LABELS = {
    "quick": {"en": "Quick overview", "es": "Vista rápida", "pt": "Visão rápida"},
    "standard": {"en": "Standard analysis", "es": "Análisis estándar", "pt": "Análise padrão"},
    "deep": {"en": "Deep dive", "es": "Análisis profundo", "pt": "Análise profunda"},
    "expert": {"en": "Expert-level analysis", "es": "Análisis experto", "pt": "Análise especializada"},
}

TONE_LABELS = {
    "professional": {"en": "Professional", "es": "Profesional", "pt": "Profissional"},
    "concise": {"en": "Concise", "es": "Conciso", "pt": "Conciso"},
    "academic": {"en": "Academic", "es": "Académico", "pt": "Acadêmico"},
    "creative": {"en": "Creative", "es": "Creativo", "pt": "Criativo"},
    "conversational": {"en": "Conversational", "es": "Conversacional", "pt": "Conversacional"},
    "technical": {"en": "Technical", "es": "Técnico", "pt": "Técnico"},
    "executive": {"en": "Executive", "es": "Ejecutivo", "pt": "Executivo"},
}

FORMAT_LABELS = {
    "markdown": {"en": "Markdown", "es": "Markdown", "pt": "Markdown"},
    "json": {"en": "JSON", "es": "JSON", "pt": "JSON"},
    "table": {"en": "Table", "es": "Tabla", "pt": "Tabela"},
    "bulletlist": {"en": "Bullet list", "es": "Lista de viñetas", "pt": "Lista de marcadores"},
    "narrative": {"en": "Narrative", "es": "Narrativo", "pt": "Narrativo"},
    "code": {"en": "Code", "es": "Código", "pt": "Código"},
    "mixed": {"en": "Mixed (Markdown + code + tables)", "es": "Mixto (Markdown + código + tablas)", "pt": "Misto (Markdown + código + tabelas)"},
}

LENGTH_LABELS = {
    "brief": {"en": "Brief (<500 words)", "es": "Breve (<500 palabras)", "pt": "Breve (<500 palavras)"},
    "moderate": {"en": "Moderate (500-1500 words)", "es": "Moderado (500-1500 palabras)", "pt": "Moderado (500-1500 palavras)"},
    "comprehensive": {"en": "Comprehensive (1500-3000 words)", "es": "Comprensivo (1500-3000 palabras)", "pt": "Abrangente (1500-3000 palavras)"},
    "unlimited": {"en": "No length limit", "es": "Sin límite", "pt": "Sem limite"},
}

ITER_LABELS = {
    "reflect": {"en": "Reflect on output quality", "es": "Reflexionar sobre la calidad de la salida", "pt": "Refletir sobre a qualidade da saída"},
    "validate": {"en": "Validate against success criteria", "es": "Validar contra los criterios de éxito", "pt": "Validar contra os critérios de sucesso"},
    "research_more": {"en": "Research and fill gaps", "es": "Investigar y llenar vacíos", "pt": "Pesquisar e preencher lacunas"},
    "all": {"en": "All strategies (reflect + validate + research)", "es": "Todas las estrategias (reflexionar + validar + investigar)", "pt": "Todas as estratégias (refletir + validar + pesquisar)"},
}


def _t(key: str, lang: str = "en") -> str:
    """Translate a key to the given language."""
    return LANG.get(lang, LANG["en"]).get(key, LANG["en"].get(key, key))


# ── Main engine ────────────────────────────────────────────────────────────

class TrammelPE:
    """Trammel PE prompt generator."""

    def __init__(self, lang: str = "en"):
        self.lang = lang

    def generate_markdown(self, data: PromptData) -> str:
        """Generate a structured prompt in Markdown format."""
        lang = data.lang or self.lang
        d = data
        if not d.objective:
            raise ValueError("objective is required")

        lines = []

        # 1. Objective
        lines.append(f"# 🎯 {_t('pObjective', lang)}")
        lines.append(d.objective)
        if d.domain:
            lines.append(f"\n{_t('pDepth', lang)}: {DEPTH_LABELS.get(d.domain, {}).get(lang, d.domain)}" if d.domain in DEPTH_LABELS else f"\n**{_t('pObjective', lang)} {_t('pDepth', lang).lower()}**: {d.domain}")

        # 2. Role & Tone
        lines.append(f"\n# 🎭 {_t('pRole', lang)}")
        if d.role:
            lines.append(f"{_t('youAre', lang)} {d.role}.")
        lines.append(f"{_t('tone', lang)}: {TONE_LABELS.get(d.tone, {}).get(lang, d.tone)}")

        # 3. Success Criteria
        if d.success_criteria:
            lines.append(f"\n# ✅ {_t('pSuccess', lang)}")
            lines.append(d.success_criteria)

        # 4. Scope
        lines.append(f"\n# 🔭 {_t('pScope', lang)}")
        if d.in_scope:
            lines.append(f"\n## {_t('pInScope', lang)}")
            lines.append(d.in_scope)
        if d.out_scope:
            lines.append(f"\n## {_t('pOutScope', lang)}")
            lines.append(d.out_scope)
        lines.append(f"\n{_t('pDepth', lang)}: {DEPTH_LABELS.get(d.depth, {}).get(lang, d.depth)}")

        # 5. Tools
        if d.tools:
            lines.append(f"\n# 🛠️ {_t('pTools', lang)}")
            lines.append(_t('pToolsDesc', lang))
            for t in d.tools:
                lines.append(f"- {tool_name(t, lang)}")

        # 6. Task Decomposition
        if d.subtasks:
            lines.append(f"\n# 🧩 {_t('pDecomposition', lang)}")
            lines.append(_t('pDecompDesc', lang))
            for i, st in enumerate(d.subtasks, 1):
                name = st.get("name", f"Step {i}") if isinstance(st, dict) else st
                desc = st.get("desc", "") if isinstance(st, dict) else ""
                data_focus = st.get("data", "") if isinstance(st, dict) else ""
                lines.append(f"\n## {_t('pSubtask', lang)} {i}: {name}")
                if desc:
                    lines.append(desc)
                if data_focus:
                    lines.append(f"\n{_t('pDataFocus', lang)}: {data_focus}")

        # 7. Context & Data
        if d.background or d.input_data or d.audience:
            lines.append(f"\n# 📚 {_t('pContext', lang)}")
            if d.background:
                lines.append(f"\n## {_t('pBackground', lang)}")
                lines.append(d.background)
            if d.input_data:
                lines.append(f"\n## {_t('pInputData', lang)}")
                lines.append(d.input_data)
            if d.audience:
                lines.append(f"\n## {_t('pAudience', lang)}")
                lines.append(d.audience)

        # 8. Output Format
        lines.append(f"\n# 📋 {_t('pFormat', lang)}")
        lines.append(f"{_t('pFormatLabel', lang)}: {FORMAT_LABELS.get(d.format_type, {}).get(lang, d.format_type)}")
        lines.append(f"{_t('pLength', lang)}: {LENGTH_LABELS.get(d.length_target, {}).get(lang, d.length_target)}")
        if d.format_type == "mixed" or (hasattr(d, '_custom_format') and d._custom_format):
            pass  # mixed is self-explanatory
        # Custom format handled via must_do/constraints if needed

        # 9. Constraints
        if d.must_do or d.constraints or d.edge_cases:
            lines.append(f"\n# 🚧 {_t('pConstraints', lang)}")
            if d.must_do:
                lines.append(f"\n## {_t('pMust', lang)}")
                lines.append(d.must_do)
            if d.constraints:
                lines.append(f"\n## {_t('pMustNot', lang)}")
                lines.append(d.constraints)
            if d.edge_cases:
                lines.append(f"\n## {_t('pEdgeCases', lang)}")
                lines.append(d.edge_cases)

        # 10. Self-Learning Loop
        if d.self_learn:
            lines.append(f"\n# 🔄 {_t('pSelfLearn', lang)}")
            lines.append(f"{_t('pStrategy', lang)}: {ITER_LABELS.get(d.iteration_strategy, {}).get(lang, d.iteration_strategy)}")
            lines.append(f"{_t('pMaxIter', lang)}: {d.max_iterations}")
            if d.improvement_focus:
                lines.append(f"\n{_t('pFocus', lang)} {d.improvement_focus}")
            lines.append(f"\n{lang == 'es' and 'Después de completar la salida inicial:' or lang == 'pt' and 'Após completar a saída inicial:' or 'After completing your initial output:'}")
            lines.append(f"1. {_t('loopStep1', lang)}")
            step2_key = "loopStep2a" if d.iteration_strategy in ("research_more", "all") else "loopStep2b"
            lines.append(f"2. {_t(step2_key, lang)}")
            lines.append(f"3. {_t('loopStep3', lang)}")
            lines.append(f"4. {_t('loopStep4', lang).replace('{n}', str(d.max_iterations))}")

        return "\n".join(lines)

    def generate_json(self, data: PromptData) -> dict:
        """Generate a structured prompt as a JSON object."""
        d = data
        obj = {
            "objective": d.objective or "",
            "domain": d.domain or "",
            "success_criteria": d.success_criteria or "",
            "scope": {
                "in_scope": d.in_scope or "",
                "out_of_scope": d.out_scope or "",
                "depth": d.depth or "standard",
            },
            "tools": [{"id": t, "name": tool_name(t, d.lang or self.lang)} for t in d.tools],
            "task_decomposition": [
                {
                    "step": i + 1,
                    "name": st.get("name", f"Step {i + 1}") if isinstance(st, dict) else st,
                    "description": st.get("desc", "") if isinstance(st, dict) else "",
                    "data_focus": st.get("data", "") if isinstance(st, dict) else "",
                }
                for i, st in enumerate(d.subtasks)
            ],
            "role": {
                "persona": d.role or "",
                "tone": d.tone or "professional",
            },
            "output": {
                "format": d.format_type or "markdown",
                "length": d.length_target or "moderate",
            },
            "context": {
                "background": d.background or "",
                "input_data": d.input_data or "",
                "audience": d.audience or "",
            },
            "constraints": {
                "must": d.must_do or "",
                "must_not": d.constraints or "",
                "edge_cases": d.edge_cases or "",
            },
        }
        if d.self_learn:
            obj["self_learning"] = {
                "enabled": True,
                "strategy": d.iteration_strategy,
                "max_iterations": d.max_iterations,
                "improvement_focus": d.improvement_focus or "",
            }
        return obj

    def save(self, data: PromptData, format: str = "markdown", path: str = None) -> str:
        """Generate and optionally save the prompt.

        Args:
            data: PromptData instance
            format: 'markdown' or 'json'
            path: Optional file path to save to

        Returns:
            The generated prompt string
        """
        if format == "json":
            content = json.dumps(self.generate_json(data), indent=2, ensure_ascii=False)
        else:
            content = self.generate_markdown(data)

        if path:
            from pathlib import Path
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")

        return content

    def from_template(self, template_id: str, overrides: dict = None) -> PromptData:
        """Create PromptData from a built-in template with optional overrides."""
        if template_id not in TEMPLATES:
            raise ValueError(f"Unknown template: {template_id}. Available: {', '.join(TEMPLATES.keys())}")
        tpl = TEMPLATES[template_id]
        # Map template keys to PromptData fields
        field_map = {
            "objective": "objective",
            "domain": "domain",
            "success_criteria": "success_criteria",
            "in_scope": "in_scope",
            "out_scope": "out_scope",
            "depth": "depth",
            "tone": "tone",
            "format_type": "format_type",
            "length_target": "length_target",
            "role": "role",
            "must_do": "must_do",
            "edge_cases": "edge_cases",
            "tools": "tools",
            "subtasks": "subtasks",
        }
        kwargs = {}
        for tpl_key, field_name in field_map.items():
            if tpl_key in tpl:
                kwargs[field_name] = tpl[tpl_key]
        if overrides:
            kwargs.update(overrides)
        return PromptData(**kwargs)

class PromptChain:
    """A sequence of prompts where each step's output feeds the next.

    Mirrors the Prompt Chains feature in index.html (buildChainMarkdown /
    buildChainJSON). Trammel generates the chain artifact; it never executes
    anything — the consuming agent runs the chain.
    """

    def __init__(self, name: str, steps: list, lang: str = "en"):
        """
        Args:
            name: Chain name.
            steps: List of PromptData instances (>= 2).
            lang: Language for generated prompts (en | es | pt).
        """
        if len(steps) < 2:
            raise ValueError("A chain needs at least 2 steps")
        for i, s in enumerate(steps):
            if not isinstance(s, PromptData):
                raise TypeError(f"steps[{i}] must be PromptData, got {type(s).__name__}")
        self.name = name
        self.steps = steps
        self.lang = lang
        self._engine = TrammelPE(lang=lang)

    def _step_name(self, data: "PromptData", i: int) -> str:
        return (data.objective or f"Step {i + 1}")[:60]

    def to_markdown(self) -> str:
        """Mega-prompt with stage gates — parity with buildChainMarkdown() in index.html."""
        n = len(self.steps)
        L = [
            f"# \U0001F517 Prompt Chain: {self.name}",
            "",
            f"> {n}-step chain generated by Trammel PE. Execute the steps IN ORDER.",
            "> Complete each step fully before starting the next. Wherever a step contains",
            "> the placeholder {{prev_output}}, substitute the complete output of the previous step.",
            "> Do not skip steps. Do not merge steps.",
        ]
        for i, data in enumerate(self.steps):
            L += ["", "---", "", f"## STEP {i + 1} of {n}: {self._step_name(data, i)}"]
            if i > 0:
                L += ["", f"**Input:** the full output of Step {i}. Use it as {{{{prev_output}}}} below."]
            L += ["", self._engine.generate_markdown(data), ""]
            if i < n - 1:
                L.append(
                    f"**Stage gate:** Step {i + 1} is complete only when its Success Criteria are met. "
                    f"Then proceed to Step {i + 2} using this step's output as {{{{prev_output}}}}."
                )
            else:
                L.append("**Stage gate:** This is the final step. Deliver its output as the chain result.")
        return "\n".join(L)

    def to_json(self) -> dict:
        """JSON chain spec — parity with buildChainJSON() in index.html."""
        return {
            "trammel_pe_chain": "1.0",
            "name": self.name,
            "execution": "sequential",
            "piping": "output of step N becomes {{prev_output}} in step N+1",
            "steps": [
                {
                    "step": i + 1,
                    "name": self._step_name(data, i),
                    "receives_prev_output": i > 0,
                    "data": self._engine.generate_json(data),
                    "prompt": self._engine.generate_markdown(data),
                }
                for i, data in enumerate(self.steps)
            ],
        }
