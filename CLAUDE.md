# tristangabl.com

Tristan Gabl's CV in Typst, in two variants. Content lives in YAML, layout in `.typ`.

| Variant | Template | Content | Output |
|---|---|---|---|
| short (one page, two columns) | `typst/short.typ` | `typst/configuration_short.yml` | `short/cv_tristan_gabl.pdf` |
| default (detailed, multi-page) | `typst/default.typ` | `typst/configuration_default.yml` | `default/cv_tristan_gabl.pdf` |
| HTML (site main page) | `site/build_html.py` | `typst/configuration_default.yml` | `index.html` (CI only) |

Shared font sizes: `typst/settings.yml`. Headshot: `typst/images/headshot.jpeg`.

## Build

Always rebuild the affected PDF after any content or layout edit (run from `typst/`):

```sh
typst compile short.typ ../short/cv_tristan_gabl.pdf
typst compile default.typ ../default/cv_tristan_gabl.pdf
```

- The short CV must stay one page: check with `pdfinfo ../short/cv_tristan_gabl.pdf | grep Pages`.
- "unknown font family: poppins" is expected locally (Poppins not installed); CI installs it from `fonts/`.

## Deploy

`.github/workflows` builds both variants on push and deploys to GitHub Pages (`gh-pages`) as
`short/cv_tristan_gabl.pdf` and `default/cv_tristan_gabl.pdf`. CI also runs `python3 site/build_html.py cv`, which renders the default YAML as `index.html` (the site's main page, Tristan's choice "for now") plus the headshot. `site/pdf.html` (PDF.js view of the default PDF) and `site/CNAME` (custom domain `tristangabl.com`) are copied to the site root.
- When a YAML field is added or renamed, update `site/build_html.py` too, so the HTML CV keeps matching the PDF. Test locally: `python3 site/build_html.py <scratch dir>`. Commits go directly to `main`.

## Writing CV bullets

- Only claim what the source (repos, reports) supports; flag unverifiable claims (e.g. comparisons or metrics without saved results) instead of writing them.
- Prefer concrete methods and numbers over generic phrases ("good coding practices").
- Skills and interests are kept identical across both configuration files.

