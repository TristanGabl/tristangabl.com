"""Render the default CV (typst/configuration_default.yml) as a web page.

Usage: python3 site/build_html.py <output_dir>
Writes <output_dir>/index.html and copies the headshot next to it.
"""

import shutil
import sys
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "typst" / "configuration_default.yml"


def e(text):
    return escape(str(text))


def link(name, url):
    return f'<a href="{e(url)}">{e(name)}</a>' if url else e(name)


def daterange(start, end):
    return e(start) if not end else f"{e(start)} – {e(end)}"


def bullets(points):
    if not points:
        return ""
    return "<ul>" + "".join(f"<li>{e(p)}</li>" for p in points) + "</ul>"


def entry(title_html, dates="", subtitle="", body=""):
    date_html = f'<span class="dates">{dates}</span>' if dates else ""
    sub_html = f'<div class="sub">{subtitle}</div>' if subtitle else ""
    return (
        '<article class="entry">'
        f'<div class="row"><h3>{title_html}</h3>{date_html}</div>'
        f"{sub_html}{body}</article>"
    )


def render(cfg):
    p = cfg["personal"]
    out = []

    # Education
    edu = [f'<p class="intro">{e(cfg["education_intro"])}</p>']
    for place in cfg["education"]:
        gpa = f'<span>GPA {e(place["gpa"])}</span>' if place.get("gpa") else ""
        body = f'<div class="row degree"><strong>{e(place["degree"])}</strong>{gpa}</div>'
        if place.get("coursework"):
            body += '<ul class="courses">' + "".join(
                f"<li>{e(c)}</li>" for c in place["coursework"]
            ) + "</ul>"
        body += bullets(place.get("points"))
        edu.append(entry(
            link(place["institution"], place.get("link")),
            daterange(place["from"], place["to"]),
            e(place["location"]),
            body,
        ))
    out.append(("Education", edu))

    # Experience: organizations first, then jobs (same order as the PDF)
    exp = []
    for org in cfg["organizations"]:
        exp.append(entry(
            f'{e(org["position"])}, {link(org["organization"], org.get("link"))}',
            daterange(org["from"], org["to"]),
            e(org["location"]),
            bullets(org.get("points")),
        ))
    for job in cfg["experience"]:
        exp.append(entry(
            f'{e(job["position"])} at {link(job["organization"], job.get("link"))}',
            daterange(job["from"], job["to"]),
            e(job["location"]),
            bullets(job.get("points")),
        ))
    out.append(("Experience", exp))

    # Projects
    proj = []
    for pr in cfg["projects"]:
        title = e(pr["name"])
        if pr.get("link"):
            title += f' <a class="tag" href="{e(pr["link"])}">github</a>'
        elif pr.get("link_note"):
            title += f' <span class="tag">{e(pr["link_note"])}</span>'
        sub = e(pr["course"]) + (f" — {e(pr['note'])}" if pr.get("note") else "")
        proj.append(entry(title, "", sub, bullets(pr.get("points"))))
    out.append(("Projects", proj))

    # Skills
    s = cfg["skills"]
    skills = [
        '<dl class="skills">'
        f'<dt>Languages</dt><dd>{" · ".join(e(x) for x in s["languages"])}</dd>'
        f'<dt>Technologies</dt><dd>{" · ".join(e(x) for x in s["technologies"])}</dd>'
        f'<dt>Interests</dt><dd>{" · ".join(e(x) for x in cfg["interests"])}</dd>'
        "</dl>"
    ]
    out.append(("Skills", skills))

    sections = "".join(
        f'<section><h2>{e(name)}</h2>{"".join(items)}</section>' for name, items in out
    )
    phone = p["phone"].replace(" ", "")
    headshot = Path(p["headshot"]).name

    return TEMPLATE.format(
        name=e(p["name"]),
        email=e(p["email"]),
        phone=e(p["phone"]),
        phone_link=e(phone),
        github=e(p["github"]),
        github_link=e(p["github_link"]),
        headshot=e(headshot),
        sections=sections,
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #ffffff; --fg: #1a1a1a; --muted: #5c5c5c; --rule: #1a1a1a;
    --accent: #1f5fa8; --tag-bg: #eeeeee;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #121212; --fg: #e8e8e8; --muted: #a0a0a0; --rule: #e8e8e8;
      --accent: #7fb2ec; --tag-bg: #2a2a2a;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg: #121212; --fg: #e8e8e8; --muted: #a0a0a0; --rule: #e8e8e8;
    --accent: #7fb2ec; --tag-bg: #2a2a2a;
  }}
  * {{ box-sizing: border-box; }}
  html {{ -webkit-text-size-adjust: 100%; }}
  body {{
    margin: 0; background: var(--bg); color: var(--fg);
    font: 17px/1.55 "Source Serif 4", Georgia, serif;
  }}
  main {{ max-width: 820px; margin: 0 auto; padding: 48px 16px 64px; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  header {{ display: flex; justify-content: space-between; align-items: center; gap: 24px; }}
  header h1 {{
    font: 500 2.1rem/1.1 Poppins, system-ui, sans-serif; letter-spacing: .02em;
    text-transform: uppercase; margin: 0 0 12px;
  }}
  .contact {{ font: 0.95rem/1.7 Poppins, system-ui, sans-serif; }}
  .contact a {{ color: var(--fg); }}
  .pdf {{
    display: inline-block; margin-top: 14px; padding: 6px 16px; border-radius: 6px;
    background: var(--accent); color: var(--bg); font: 500 0.9rem Poppins, system-ui, sans-serif;
  }}
  .pdf:hover {{ text-decoration: none; opacity: .88; }}
  header img {{ width: 112px; height: 136px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }}
  h2 {{
    display: flex; align-items: center; gap: 12px; margin: 40px 0 16px;
    font: 600 1.15rem Poppins, system-ui, sans-serif; text-transform: uppercase; letter-spacing: .03em;
  }}
  h2::after {{ content: ""; flex: 1; border-top: 1px solid var(--rule); }}
  .intro {{ font-style: italic; color: var(--muted); margin: 0 0 20px; }}
  .entry {{ margin-bottom: 24px; }}
  .row {{ display: flex; justify-content: space-between; align-items: baseline; gap: 16px; }}
  h3 {{ font-size: 1.05rem; font-weight: 600; margin: 0; }}
  .dates {{ font-style: italic; color: var(--muted); white-space: nowrap; font-size: .95rem; }}
  .sub {{ font-style: italic; color: var(--muted); font-size: .95rem; }}
  .degree {{ margin-top: 6px; }}
  .degree span {{ font-weight: 600; white-space: nowrap; }}
  ul {{ margin: 8px 0 0; padding-left: 20px; }}
  li {{ margin-bottom: 4px; }}
  .courses {{
    columns: 2; column-gap: 24px; list-style: none; padding-left: 16px; font-size: .95rem;
  }}
  .tag {{
    font: 500 .7rem Poppins, system-ui, sans-serif; background: var(--tag-bg);
    padding: 2px 7px; border-radius: 4px; vertical-align: 2px; margin-left: 4px;
  }}
  .skills {{ display: grid; grid-template-columns: max-content 1fr; gap: 6px 16px; margin: 0; }}
  .skills dt {{ font-weight: 600; }}
  .skills dd {{ margin: 0; }}
  @media (max-width: 560px) {{
    main {{ padding-top: 28px; }}
    header {{ flex-direction: column-reverse; align-items: flex-start; }}
    header h1 {{ font-size: 1.7rem; }}
    .row {{ flex-direction: column; gap: 0; }}
    .courses {{ columns: 1; }}
    .skills {{ grid-template-columns: 1fr; gap: 0; }}
    .skills dd {{ margin-bottom: 8px; }}
  }}
  @media print {{
    .pdf {{ display: none; }}
    main {{ padding: 0; }}
  }}
</style>
</head>
<body>
<main>
<header>
  <div>
    <h1>{name}</h1>
    <div class="contact">
      <a href="mailto:{email}">{email}</a><br>
      <a href="tel:{phone_link}">{phone}</a><br>
      <a href="{github_link}">{github}</a>
    </div>
    <a class="pdf" href="default/cv_tristan_gabl.pdf">PDF</a>
  </div>
  <img src="{headshot}" alt="{name}">
</header>
{sections}
</main>
</body>
</html>
"""


def main():
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "cv")
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = yaml.safe_load(CONFIG.read_text())
    (out_dir / "index.html").write_text(render(cfg))
    headshot = ROOT / "typst" / cfg["personal"]["headshot"]
    shutil.copy(headshot, out_dir / headshot.name)


if __name__ == "__main__":
    main()
