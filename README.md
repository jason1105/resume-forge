# resume-forge

Auto-generates multiple resume versions from a single YAML source of truth, published to GitHub Pages.

## How it works

1. Edit `data/resume.yml` — the single source of truth for all resume content.
2. Push to `main`. GitHub Actions detects the change, calls the Anthropic API to generate four Markdown variants, commits them to `output/`, and deploys the Pages site.
3. Your resume portfolio is live at `https://<your-username>.github.io/resume-forge/`.

## File structure

```
resume-forge/
├── data/
│   └── resume.yml              # Edit this — single source of truth
├── scripts/
│   └── build_resumes.py        # Calls Claude API, writes output/
├── output/
│   ├── resume_zh.md            # Full Chinese resume (auto-generated)
│   ├── resume_en.md            # Full English resume (auto-generated)
│   ├── resume_onepage_zh.md    # One-page Chinese (auto-generated)
│   └── resume_onepage_en.md    # One-page English (auto-generated)
├── .github/
│   └── workflows/
│       └── build-resume.yml    # CI/CD pipeline
├── index.html                  # Resume portfolio viewer (GitHub Pages)
└── README.md
```

## Setup

### 1. Create the repository

```bash
gh repo create resume-forge --public
cd resume-forge
git remote add origin https://github.com/<your-username>/resume-forge.git
```

### 2. Add the Anthropic API key secret

In your GitHub repository: **Settings → Secrets and variables → Actions → New repository secret**

- Name: `ANTHROPIC_API_KEY`
- Value: your Anthropic API key (get one at https://console.anthropic.com)

### 3. Enable GitHub Pages

In your repository: **Settings → Pages**

- Source: **GitHub Actions**

### 4. Push and let the workflow run

```bash
git add .
git commit -m "feat: initial resume-forge setup"
git push -u origin main
```

The workflow triggers automatically because `data/resume.yml` changed. Watch it run under the **Actions** tab.

## Running locally

```bash
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/build_resumes.py
```

Then open `index.html` via a local web server (required for the `fetch()` calls to work):

```bash
python -m http.server 8080
# Open http://localhost:8080
```

## Customizing

- **Content**: edit `data/resume.yml`.
- **Prompts**: tweak the `PROMPT_*` strings in `scripts/build_resumes.py` to adjust tone, length, or format.
- **Model**: change the `MODEL` constant in `build_resumes.py`. Currently uses `claude-haiku-4-5-20251001` for speed and cost efficiency.
- **Styling**: all design is contained in `index.html` — edit the `<style>` block to change fonts, colors, or layout.

## Triggering a rebuild without changing resume.yml

Use the **workflow_dispatch** trigger via the GitHub UI or CLI:

```bash
gh workflow run build-resume.yml
```
