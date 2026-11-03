// Generates the animated profile header (assets/header-{dark,light}.svg).
// Usage: node scripts/build-header.mjs
import { writeFileSync } from 'node:fs'

const W = 1200
const H = 300
const CHAR = 14.4 // monospace advance at 24px (textLength keeps it exact)
const SLOT = 4 // seconds each typed line stays on screen

const lines = {
  pt: [
    'Desenvolvedor Front-end',
    'Angular · React · TypeScript',
    'Referência técnica no setor financeiro',
    '6+ anos criando interfaces rápidas e acessíveis',
  ],
  en: [
    'Front-end Developer',
    'Angular · React · TypeScript',
    'Technical lead in the financial sector',
    '6+ years building fast, accessible interfaces',
  ],
}

const themes = {
  dark: {
    bg1: '#0b0d14',
    bg2: '#151a2b',
    grid: '#ffffff',
    gridOpacity: 0.04,
    muted: '#9aa3b5',
    text: '#e7e9ee',
    card: '#11141f',
    cardBorder: '#262c40',
    code: '#c9d1e3',
  },
  light: {
    bg1: '#ffffff',
    bg2: '#eef1f8',
    grid: '#1b2236',
    gridOpacity: 0.05,
    muted: '#5b6478',
    text: '#151a2b',
    card: '#ffffff',
    cardBorder: '#dde2ee',
    code: '#2a3148',
  },
}

const escape = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

function typing(texts) {
  const total = SLOT * texts.length
  const nodes = []
  texts.forEach((text, i) => {
    const width = Math.round(text.length * CHAR)
    const s = i * SLOT
    // Points in seconds: hidden, typed, hold, erased, hidden until the cycle ends.
    const points = [
      [0, 0],
      [s, 0],
      [s + 1.6, width],
      [s + 3.2, width],
      [s + 3.8, 0],
      [total, 0],
    ].filter(([t], idx, all) => idx === 0 || t > all[idx - 1][0])
    const keyTimes = points.map(([t]) => (t / total).toFixed(4)).join(';')
    const widths = points.map(([, w]) => w).join(';')
    const shifts = points.map(([, w]) => `${w} 0`).join(';')
    const on = (s / total).toFixed(4)
    const off = ((s + 3.8) / total).toFixed(4)
    const visible = s === 0 ? { values: '1;0', keyTimes: `0;${off}` } : { values: '0;1;0', keyTimes: `0;${on};${off}` }
    nodes.push(`
      <clipPath id="clip${i}"><rect x="0" y="-30" width="0" height="40">
        <animate attributeName="width" values="${widths}" keyTimes="${keyTimes}" dur="${total}s" repeatCount="indefinite"/>
      </rect></clipPath>
      <text clip-path="url(#clip${i})" class="mono" textLength="${width}" lengthAdjust="spacingAndGlyphs">${escape(text)}</text>
      <g opacity="0">
        <animate attributeName="opacity" values="${visible.values}" keyTimes="${visible.keyTimes}" calcMode="discrete" dur="${total}s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" type="translate" values="${shifts}" keyTimes="${keyTimes}" dur="${total}s" repeatCount="indefinite"/>
        <rect x="4" y="-22" width="12" height="28" rx="2" fill="#a78bfa">
          <animate attributeName="opacity" values="1;0;1" keyTimes="0;0.5;1" calcMode="discrete" dur="1s" repeatCount="indefinite"/>
        </rect>
      </g>`)
  })
  return { css: '', nodes: nodes.join('') }
}

function svg(theme, lang) {
  const c = themes[theme]
  const { css, nodes } = typing(lines[lang])
  const greeting = lang === 'pt' ? 'Olá, eu sou' : "Hi, I'm"
  const title = lang === 'pt' ? 'Bruno Vinicius Isaac Costa, desenvolvedor front-end' : 'Bruno Vinicius Isaac Costa, front-end developer'
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="title">
  <title id="title">${title}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg2}"/>
    </linearGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#a78bfa"><animate attributeName="stop-color" values="#a78bfa;#22d3ee;#f472b6;#a78bfa" dur="10s" repeatCount="indefinite"/></stop>
      <stop offset="1" stop-color="#22d3ee"><animate attributeName="stop-color" values="#22d3ee;#f472b6;#a78bfa;#22d3ee" dur="10s" repeatCount="indefinite"/></stop>
    </linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="${c.grid}" stroke-opacity="${c.gridOpacity}"/>
    </pattern>
    <radialGradient id="glowA"><stop offset="0" stop-color="#7c3aed" stop-opacity="0.35"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
    <radialGradient id="glowB"><stop offset="0" stop-color="#06b6d4" stop-opacity="0.28"/><stop offset="1" stop-color="#06b6d4" stop-opacity="0"/></radialGradient>
    <clipPath id="frame"><rect width="${W}" height="${H}" rx="20"/></clipPath>
  </defs>
  <style>
    .sans { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Ubuntu, 'Helvetica Neue', Arial, sans-serif; }
    .mono { font-family: Consolas, 'SFMono-Regular', Menlo, 'Courier New', monospace; font-size: 24px; fill: ${c.text}; }
    .pulse { animation: pulse 8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
    @keyframes pulse { 50% { transform: scale(1.15); opacity: 0.7; } }
    .dot { animation: dot 2s ease-in-out infinite; }
    @keyframes dot { 50% { opacity: 0.35; } }
    .code { font-family: Consolas, 'SFMono-Regular', Menlo, monospace; font-size: 17px; fill: ${c.code}; }
    .k { fill: #c084fc; } .s { fill: #34d399; } .p { fill: #f472b6; }
    @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }${css}
  </style>
  <g clip-path="url(#frame)">
    <rect width="${W}" height="${H}" fill="url(#bg)"/>
    <rect width="${W}" height="${H}" fill="url(#grid)"/>
    <circle class="pulse" cx="140" cy="40" r="220" fill="url(#glowA)"/>
    <circle class="pulse" cx="1080" cy="280" r="240" fill="url(#glowB)" style="animation-delay:-4s"/>
  </g>
  <rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="20" fill="none" stroke="${c.cardBorder}"/>

  <g transform="translate(64 64)">
    <rect x="0" y="0" width="${lang === 'pt' ? 236 : 262}" height="30" rx="15" fill="${c.card}" stroke="${c.cardBorder}"/>
    <circle class="dot" cx="18" cy="15" r="5" fill="#22c55e"/>
    <text x="32" y="20" class="sans" font-size="14" fill="${c.muted}">${lang === 'pt' ? 'Aberto a novas oportunidades' : 'Open to new opportunities'}</text>
  </g>
  <text x="64" y="132" class="sans" font-size="22" font-weight="600" fill="${c.muted}">${greeting}</text>
  <text x="64" y="184" class="sans" font-size="46" font-weight="800" fill="url(#name)" letter-spacing="-1">Bruno Vinicius Isaac Costa</text>
  <g transform="translate(64 240)">
    <text x="0" y="0" class="mono" fill="#a78bfa" style="fill:#a78bfa">&gt;</text>
    <g transform="translate(26 0)">${nodes}
    </g>
  </g>

  <g transform="translate(800 70)"><g>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" keyTimes="0;0.5;1" dur="6s" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" repeatCount="indefinite"/>
    <rect width="340" height="170" rx="14" fill="${c.card}" stroke="${c.cardBorder}"/>
    <circle cx="22" cy="20" r="5" fill="#f87171"/><circle cx="40" cy="20" r="5" fill="#fbbf24"/><circle cx="58" cy="20" r="5" fill="#34d399"/>
    <text x="316" y="25" text-anchor="end" class="code" font-size="13" fill="${c.muted}" style="fill:${c.muted}">bruno.ts</text>
    <text x="22" y="66" class="code"><tspan class="k">const</tspan> dev = {</text>
    <text x="22" y="92" class="code" xml:space="preserve">  role: <tspan class="s">'Front-end'</tspan>,</text>
    <text x="22" y="118" class="code" xml:space="preserve">  stack: [<tspan class="s">'Angular'</tspan>, <tspan class="s">'React'</tspan>],</text>
    <text x="22" y="144" class="code">} <tspan class="k">satisfies</tspan> <tspan class="p">Developer</tspan></text>
  </g></g>
</svg>
`
}

for (const theme of Object.keys(themes)) {
  for (const lang of Object.keys(lines)) {
    const file = `assets/header-${lang}-${theme}.svg`
    writeFileSync(file, svg(theme, lang))
    console.log('wrote', file)
  }
}
