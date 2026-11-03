"""Generates README.md (profile page). Usage: python scripts/build_readme.py"""
from pathlib import Path

LINKEDIN = 'https://www.linkedin.com/in/bruno-vin%C3%ADcius-isaac-costa-a90758156/'
SITE = 'https://portfolio.brunoisaac.dev'
GITHUB = 'https://github.com/BrunoICosta'
RAW = 'https://raw.githubusercontent.com/BrunoICosta'

# repo, name pt, name en, stack, description pt, description en
PROJECTS = [
    ('angular-ecommerce-admin', 'Painel Admin de E-commerce', 'E-commerce Admin', 'Angular 20 · Material · Signals',
     'Tabelas com paginação, ordenação e filtros, interceptors HTTP e guards por perfil.',
     'Material tables with pagination, sorting and filters, HTTP interceptors and role-based guards.'),
    ('next-ecommerce-store', 'Loja Virtual com Next.js', 'Next.js E-commerce Store', 'Next.js 16 · React 19 · Zustand',
     'App Router com páginas estáticas, carrinho persistente e checkout completo, bilíngue e com SEO.',
     'App Router with static pages, persistent cart and full checkout, bilingual with SEO.'),
    ('angular-kanban-board', 'Quadro Kanban', 'Kanban Board', 'Angular 20 · NgRx · CDK',
     'Arrastar e soltar com atualização otimista e rollback, estado com Store, Effects e Entity.',
     'Drag and drop with optimistic updates and rollback, state with Store, Effects and Entity.'),
    ('react-realtime-chat', 'Chat em Tempo Real', 'Realtime Chat', 'React 19 · Socket.io · Node',
     'Monorepo com contratos tipados, JWT, presença e modo demo que roda direto no navegador.',
     'Monorepo with typed contracts, JWT, presence and a demo mode that runs in the browser.'),
    ('angular-tv-explorer', 'Explorador de Séries', 'TV Explorer', 'Angular 20 · RxJS · Signals',
     'Busca com debounce, rolagem infinita, detalhes, elenco e agenda do dia.',
     "Debounced search, infinite scroll, details, cast and today's schedule."),
    ('angular-finance-tracker', 'Controle Financeiro', 'Finance Tracker', 'Angular 20 · Material · Chart.js',
     'Lançamentos, orçamento mensal, gráficos e máscara de valores por idioma.',
     'Transactions, monthly budget, charts and a locale-aware money mask.'),
    ('angular-appointment-scheduler', 'Agenda de Atendimentos', 'Appointment Scheduler', 'Angular 20 · FullCalendar · Transloco',
     'Calendário com validadores customizados e visão adaptada ao celular.',
     'Calendar with custom validators and a mobile-friendly view.'),
    ('react-recipe-finder', 'Receitário', 'Recipe Finder', 'React 19 · React Hook Form · Zod',
     'Receitas do TheMealDB com tradução automática e receitas próprias validadas.',
     'TheMealDB recipes with automatic translation and validated custom recipes.'),
    ('react-weather-dashboard', 'Painel do Clima', 'Weather Dashboard', 'React 19 · TanStack Query · Recharts',
     'Busca de cidades, previsão horária e semanal e geolocalização.',
     'City search, hourly and weekly forecast and geolocation.'),
    ('react-habit-tracker', 'Rastreador de Hábitos', 'Habit Tracker', 'React 19 · PWA · Motion',
     'Funciona offline, com sequências, mapa de calor anual e animações.',
     'Works offline, with streaks, a yearly heatmap and animations.'),
    ('react-notes-workspace', 'Espaço de Notas', 'Notes Workspace', 'React 19 · dnd-kit · Zustand',
     'Páginas aninhadas, blocos reordenáveis e menu de comandos com "/".',
     'Nested pages, reorderable blocks and a "/" command menu.'),
]

ICONS = ('https://skillicons.dev/icons?i=angular,react,nextjs,ts,js,html,css,sass,tailwind,'
         'nodejs,jest,vitest,git,githubactions,cloudflare,vscode&perline=8')
SNAKE = f'{RAW}/BrunoICosta/output'


def cell(project, lang):
    repo, name_pt, name_en, stack, desc_pt, desc_en = project
    name, desc = (name_pt, desc_pt) if lang == 'pt' else (name_en, desc_en)
    code = 'Código' if lang == 'pt' else 'Code'
    return (
        '<td width="50%" valign="top">\n'
        f'<a href="{SITE}/{repo}/"><img src="{RAW}/{repo}/main/docs/screenshot.png" alt="{name}" width="100%"></a>\n'
        f'<h4>{name}</h4>\n<sub><code>{stack}</code></sub><br>\n{desc}<br>\n'
        f'<a href="{SITE}/{repo}/"><b>Demo</b></a> · <a href="{GITHUB}/{repo}">{code}</a>\n'
        '</td>'
    )


def table(items, lang):
    rows = []
    for i in range(0, len(items), 2):
        cells = [cell(p, lang) for p in items[i:i + 2]]
        if len(cells) == 1:
            cells.append('<td width="50%"></td>')
        rows.append('<tr>\n' + '\n'.join(cells) + '\n</tr>')
    return '<table>\n' + '\n'.join(rows) + '\n</table>'


def badges(lang):
    pt = lang == 'pt'
    cv = f"{SITE}/cv/Bruno-Costa-{'Curriculo' if pt else 'Resume'}.pdf"
    mail = 'contato@brunoisaac.dev' if pt else 'hello@brunoisaac.dev'
    shield = 'https://img.shields.io/badge'
    style = 'style=for-the-badge&logoColor=white'
    return ' '.join([
        f'<a href="{SITE}/"><img src="{shield}/{"Portf%C3%B3lio" if pt else "Portfolio"}-7c3aed?{style}&logo=googlechrome" alt="Portfolio"></a>',
        f'<a href="{LINKEDIN}"><img src="{shield}/LinkedIn-0A66C2?{style}&logo=linkedin" alt="LinkedIn"></a>',
        f'<a href="mailto:{mail}"><img src="{shield}/{"E--mail" if pt else "Email"}-0891b2?{style}&logo=maildotru" alt="{mail}"></a>',
        f'<a href="{cv}"><img src="{shield}/{"Curr%C3%ADculo" if pt else "Resume"}-db2777?{style}&logo=readthedocs" alt="CV"></a>',
    ])


def header(lang):
    alt = ('Bruno Vinicius Isaac Costa, desenvolvedor front-end' if lang == 'pt'
           else 'Bruno Vinicius Isaac Costa, front-end developer')
    return (
        '<picture>\n'
        f'  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-{lang}-dark.svg">\n'
        f'  <img src="./assets/header-{lang}-light.svg" alt="{alt}" width="100%">\n'
        '</picture>'
    )


def snake(alt):
    return (
        '<picture>\n'
        f'  <source media="(prefers-color-scheme: dark)" srcset="{SNAKE}/github-snake-dark.svg">\n'
        f'  <img src="{SNAKE}/github-snake.svg" alt="{alt}" width="100%">\n'
        '</picture>'
    )


README = f'''<div align="center">

{header("pt")}

{badges("pt")}

<sub><b>Português</b> · <a href="#english">English</a></sub>

</div>

## 👋 Sobre mim

Sou desenvolvedor front-end com **mais de 6 anos de experiência**, a maior parte no setor financeiro, em projetos para **Banco do Brasil, Bradesco e Banco Safra**. Hoje sou referência técnica em diversos sistemas no Safra, conduzindo o time com code review, documentação e apoio a desenvolvedores júnior, pleno e sênior.

- ⚡ Domino **Angular**, do AngularJS às versões modernas (standalone components e signals)
- ⚛️ Uso **React** e **Next.js** nos meus projetos, sempre com **TypeScript**
- 🚀 Já reduzi o carregamento de páginas de **10 s para 600 ms**
- ♿ Me preocupo com arquitetura, testes automatizados e acessibilidade
- 🌐 Todos os projetos abaixo são bilíngues (pt-BR e en), testados e com demo no ar

<table>
<tr>
<td align="center" width="33%"><h3>6+</h3><sub>anos de experiência</sub></td>
<td align="center" width="33%"><h3>3</h3><sub>grandes bancos atendidos</sub></td>
<td align="center" width="33%"><h3>10 s → 0,6 s</h3><sub>carregamento otimizado</sub></td>
</tr>
</table>

## 🧰 Stack

<p align="center">
  <img src="{ICONS}" alt="Angular, React, Next.js, TypeScript, JavaScript, HTML, CSS, Sass, Tailwind, Node.js, Jest, Vitest, Git, GitHub Actions, Cloudflare, VS Code">
</p>

<p align="center">
  <code>RxJS</code> <code>NgRx</code> <code>Signals</code> <code>Angular Material</code> <code>Zustand</code> <code>TanStack Query</code> <code>React Hook Form</code> <code>Zod</code> <code>Socket.io</code> <code>Transloco</code> <code>i18next</code> <code>Karma</code> <code>Jasmine</code>
</p>

## 🚀 Projetos em destaque

Todos publicados em **[portfolio.brunoisaac.dev]({SITE}/)**. Clique na imagem para abrir a demo.

{table(PROJECTS[:4], "pt")}

<details>
<summary><b>📂 Ver os outros 7 projetos</b></summary>
<br>

{table(PROJECTS[4:], "pt")}

</details>

## 💼 Por onde passei

<details open>
<summary><b>Analista de Sistemas · ACT Digital</b> · cliente Banco Safra · jul. 2021 até o momento</summary>

- Referência técnica em sistemas internos de maquininhas de cartão e domicílio bancário
- Aplicações em Angular e TypeScript, com testes em Jest e Karma
- Code review, documentação técnica e mentoria em times com Scrum e Kanban

</details>

<details>
<summary><b>Analista de Sistemas · Everis / NTT DATA</b> · cliente Bradesco · abr. 2021 a jul. 2021</summary>

- Funcionalidades do módulo de Open Finance do aplicativo Bradesco com Angular

</details>

<details>
<summary><b>Analista de Sistemas · Capgemini</b> · cliente Banco do Brasil · mar. 2020 a abr. 2021</summary>

- Migração de aplicações de AngularJS para Angular na plataforma interna do Banco do Brasil

</details>

<details>
<summary><b>Estágios em TI · Banco do Brasil e SEPLAG / CODHAB</b> · ago. 2018 a mar. 2020</summary>

- PostgreSQL, Java, AngularJS e VueJS, documentação técnica e intranet

</details>

<sub>🎓 Bacharelado em Sistemas de Informação (Faculdade Projeção) · 📜 Scrum Foundation (SFPC) · Kanban Foundation (KIKF)</sub>

## 🐍 Atividade

{snake("Cobrinha comendo as contribuições do GitHub")}

---

<h2 id="english">🌎 English</h2>

<details>
<summary><b>Open the English version</b></summary>
<br>

<div align="center">

{header("en")}

{badges("en")}

</div>

### 👋 About me

Front-end developer with **6+ years of experience**, mostly in the financial sector, on projects for **Banco do Brasil, Bradesco and Banco Safra**. Today I am the technical reference for several systems at Safra, leading the team through code review, documentation and mentoring.

- ⚡ Deep **Angular** expertise, from AngularJS to modern versions (standalone components and signals)
- ⚛️ I use **React** and **Next.js** in my own projects, always with **TypeScript**
- 🚀 Cut page load time from **10 s to 600 ms**
- ♿ I care about architecture, automated tests and accessibility
- 🌐 Every project below is bilingual (pt-BR and en), tested and live

### 🚀 Featured projects

All live at **[portfolio.brunoisaac.dev]({SITE}/)**.

{table(PROJECTS[:4], "en")}

<details>
<summary><b>📂 See the other 7 projects</b></summary>
<br>

{table(PROJECTS[4:], "en")}

</details>

### 💼 Experience

- **Systems Analyst · ACT Digital** (client Banco Safra) · Jul 2021 to present: technical reference, Angular, Jest, Karma, code review
- **Systems Analyst · Everis / NTT DATA** (client Bradesco) · Apr 2021 to Jul 2021: Open Finance module with Angular
- **Systems Analyst · Capgemini** (client Banco do Brasil) · Mar 2020 to Apr 2021: AngularJS to Angular migration
- **IT Intern · Banco do Brasil and SEPLAG / CODHAB** · Aug 2018 to Mar 2020

</details>

<br>

<div align="center">
<sub>Feito com ☕ em Brasília · <a href="{SITE}/">portfolio.brunoisaac.dev</a> · <a href="{LINKEDIN}">LinkedIn</a></sub>
</div>
'''

Path('README.md').write_text(README, encoding='utf-8', newline='\n')
print('README.md written')
