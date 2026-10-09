# tristangabl.com

Tristan Gabl's CV in Typst, in two variants. Content lives in YAML, layout in `.typ`.

| Variant | Template | Content | Output |
|---|---|---|---|
| short (one page, two columns) | `typst/short.typ` | `typst/configuration_short.yml` | `short/cv_tristan_gabl.pdf` |
| default (detailed, multi-page) | `typst/default.typ` | `typst/configuration_default.yml` | `default/cv_tristan_gabl.pdf` |

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
`short/cv_tristan_gabl.pdf` and `default/cv_tristan_gabl.pdf`. `site/index.html` (embeds the default CV) and `site/CNAME` (custom domain `tristangabl.com`) are copied to the site root. Commits go directly to `main`.

## Writing CV bullets

- Only claim what the source (repos, reports) supports; flag unverifiable claims (e.g. comparisons or metrics without saved results) instead of writing them.
- Prefer concrete methods and numbers over generic phrases ("good coding practices").
- Skills and interests are kept identical across both configuration files.
