# RepoScope

> Analyze any GitHub repository in seconds. No accounts. No subscriptions. Just Docker.

**RepoScope** is a lightweight, open-source codebase analyzer that generates objective reports on code quality, security, engineering activity, and best practices — all from a single `docker run` command.

[![Docker Image](https://img.shields.io/docker/v/yourname/reposcope?label=Docker%20Hub&logo=docker)](https://hub.docker.com/r/yourname/reposcope)
[![CI Status](https://img.shields.io/github/actions/workflow/status/yourname/reposcope/ci.yml?branch=main&logo=github)](https://github.com/yourname/reposcope/actions)
[![License: MIT](https://img.shields.io/github/license/yourname/reposcope)](LICENSE)

---

## Why RepoScope?

Evaluating a repository — whether for due diligence, a job application, a vendor audit, or open-source contribution — usually means clicking through GitHub tabs manually. RepoScope automates that into a structured, repeatable report with no setup friction.

- **Zero installation** — runs entirely in Docker
- **No external services** — uses only the free GitHub API and local open-source analyzers
- **Objective output** — JSON for pipelines, PDF for humans
- **Private repo support** — pass a GitHub personal access token and you're done

---

## What Gets Analyzed

| Category           | What RepoScope Checks                                                                                    |
| ------------------ | -------------------------------------------------------------------------------------------------------- |
| **Code Quality**   | Test directory presence, CI configuration (GitHub Actions, Travis CI, etc.), linting config files        |
| **Security**       | Dependency file detection, known vulnerability scanning via [`safety`](https://pypi.org/project/safety/) |
| **Activity**       | Total closed pull requests, average PR merge time (days)                                                 |
| **Best Practices** | Presence of `README`, `LICENSE`, `CONTRIBUTING`, and `CODE_OF_CONDUCT`                                   |

---

## Quick Start

build from source:

```bash
git clone https://github.com/Saad7890-web/RepoScope.git
cd reposcope
docker build -t reposcope .
```

### Generate a report

```bash
# PDF report (great for sharing)
docker run --rm reposcope analyze \
  --repo https://github.com/octocat/Hello-World \
  --format pdf > report.pdf

# JSON report (great for pipelines)
docker run --rm reposcope analyze \
  --repo https://github.com/octocat/Hello-World \
  --format json
```

### Save the PDF to your current directory

```bash
docker run --rm -v $(pwd):/out reposcope analyze \
  --repo https://github.com/angular/angular \
  --format pdf \
  --output /out/angular_report.pdf
```

---

## REST API

RepoScope also ships with an optional HTTP API powered by [FastAPI](https://fastapi.tiangolo.com/).

**Start the server:**

```bash
docker run -d -p 8000:8000 reposcope
```

**Submit an analysis:**

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/octocat/Hello-World", "format": "json"}'
```

The report is returned directly in the response body.

---

## Configuration

### Private repositories & rate limits

Set the `GITHUB_TOKEN` environment variable to authenticate with the GitHub API. This is required for private repositories and recommended to avoid rate limiting on public ones.

```bash
docker run --rm \
  -e GITHUB_TOKEN=your_personal_access_token \
  reposcope analyze \
  --repo https://github.com/your-org/private-repo \
  --format pdf > report.pdf
```

### Output formats

| Format | Use case                                                   |
| ------ | ---------------------------------------------------------- |
| `json` | CI pipelines, programmatic consumption, further processing |
| `pdf`  | Sharing with teams, investors, or reviewers                |

---

## Contributing

Contributions are welcome — bug fixes, new analyzers, or documentation improvements.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request

Run the test suite locally with Docker:

```bash
docker build -t reposcope-dev .
docker run reposcope-dev pytest
```

---

## Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — REST API layer
- **[WeasyPrint](https://weasyprint.org/)** — PDF generation
- **[Safety](https://pypi.org/project/safety/)** — dependency vulnerability scanning
- **[GitHub REST API](https://docs.github.com/en/rest)** — repository data

---

## License

Distributed under the [MIT License](LICENSE).

---

## Support

Found a bug or have a feature request? [Open an issue](https://github.com/yourname/reposcope/issues) on GitHub.
