from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = [
    ROOT / "templates" / "base_app.html",
    *sorted((ROOT / "templates" / "dashboard").rglob("*.html")),
    *sorted((ROOT / "templates" / "payments").rglob("*.html")),
]
OUTPUT = ROOT / "static" / "css" / "tailwind-lite.css"
STATICFILES_DIR = ROOT / "staticfiles" / "css"
MANIFEST = ROOT / "staticfiles" / "staticfiles.json"


IGNORE = {
    "active",
    "badge",
    "badge--danger",
    "badge--info",
    "badge--neutral",
    "badge--orange",
    "badge--success",
    "badge--warning",
    "btn",
    "btn--danger",
    "btn--ghost",
    "btn--primary",
    "btn--secondary",
    "btn--sm",
    "btn--xs",
    "card",
    "card-body",
    "card-header",
    "card-title",
    "crm-table",
    "elif",
    "empty-state",
    "empty-state-desc",
    "empty-state-icon",
    "empty-state-title",
    "f.statut",
    "facture-page",
    "facture.statut",
    "filter-bar",
    "flash-msg",
    "form-error",
    "form-hint",
    "form-input",
    "form-label",
    "form-section-title",
    "form-select",
    "info-grid",
    "info-item",
    "info-label",
    "info-value",
    "kanban-card",
    "kanban-col",
    "kpi--danger",
    "kpi--purple",
    "kpi--success",
    "kpi-card",
    "kpi-label",
    "kpi-secondary",
    "kpi-value",
    "ligne-hors-taxe",
    "ligne-pu",
    "ligne-qty",
    "ligne-row",
    "ligne-total",
    "page-header",
    "page-link",
    "page-subtitle",
    "page-title",
    "pagination",
    "preview_pdf",
    "recurrence-field",
    "section-card",
    "section-divider",
    "sidebar-link",
    "sidebar-nav",
    "sr-only",
    "step-pill",
    "sticky-summary",
    "text-money",
    "view-toggle",
}


COLORS = {
    "white": "#ffffff",
    "black": "#000000",
    "ink": "#0f172a",
    "slate-50": "#f8fafc",
    "slate-100": "#f1f5f9",
    "slate-200": "#e2e8f0",
    "slate-300": "#cbd5e1",
    "slate-400": "#94a3b8",
    "slate-500": "#64748b",
    "slate-600": "#475569",
    "slate-700": "#334155",
    "slate-800": "#1e293b",
    "slate-900": "#0f172a",
    "blue-100": "#dbeafe",
    "blue-200": "#bfdbfe",
    "blue-400": "#60a5fa",
    "blue-500": "#3b82f6",
    "blue-600": "#2563eb",
    "blue-700": "#1d4ed8",
    "blue-800": "#1e40af",
    "blue-900": "#1e3a8a",
    "brand-50": "#eff6ff",
    "brand-100": "#dbeafe",
    "brand-200": "#bfdbfe",
    "brand-300": "#93c5fd",
    "brand-400": "#60a5fa",
    "brand-600": "#2563eb",
    "brand-700": "#1d4ed8",
    "brand-800": "#1e40af",
    "emerald-50": "#ecfdf5",
    "emerald-100": "#d1fae5",
    "emerald-200": "#a7f3d0",
    "emerald-300": "#6ee7b7",
    "emerald-400": "#34d399",
    "emerald-500": "#10b981",
    "emerald-600": "#059669",
    "emerald-700": "#047857",
    "emerald-800": "#065f46",
    "indigo-50": "#eef2ff",
    "indigo-100": "#e0e7ff",
    "indigo-200": "#c7d2fe",
    "indigo-500": "#6366f1",
    "indigo-600": "#4f46e5",
    "indigo-700": "#4338ca",
    "indigo-900": "#312e81",
    "amber-100": "#fef3c7",
    "amber-200": "#fde68a",
    "amber-400": "#fbbf24",
    "amber-500": "#f59e0b",
    "amber-700": "#b45309",
    "rose-50": "#fff1f2",
    "rose-200": "#fecdd3",
    "rose-300": "#fda4af",
    "rose-500": "#f43f5e",
    "rose-600": "#e11d48",
    "rose-700": "#be123c",
    "rose-800": "#9f1239",
    "orange-500": "#f97316",
}

SPACING = {
    "0": "0px",
    "0.5": "0.125rem",
    "1": "0.25rem",
    "1.5": "0.375rem",
    "2": "0.5rem",
    "2.5": "0.625rem",
    "3": "0.75rem",
    "3.5": "0.875rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "7": "1.75rem",
    "8": "2rem",
    "9": "2.25rem",
    "10": "2.5rem",
    "11": "2.75rem",
    "12": "3rem",
    "32": "8rem",
    "52": "13rem",
    "64": "16rem",
    "72": "18rem",
}

MAX_WIDTH = {
    "2xl": "42rem",
    "6xl": "72rem",
}

TEXT_SIZES = {
    "xs": "0.75rem",
    "sm": "0.875rem",
    "base": "1rem",
    "lg": "1.125rem",
    "xl": "1.25rem",
    "2xl": "1.5rem",
    "3xl": "1.875rem",
}

BREAKPOINTS = {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
}

RADIUS = {
    "rounded": "0.25rem",
    "rounded-md": "0.375rem",
    "rounded-lg": "0.5rem",
    "rounded-xl": "0.75rem",
    "rounded-2xl": "1rem",
    "rounded-3xl": "1.5rem",
    "rounded-full": "9999px",
    "rounded-none": "0px",
}


def split_variants(token: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    bracket_depth = 0
    for char in token:
        if char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth -= 1
        if char == ":" and bracket_depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    parts.append("".join(current))
    return parts


def escape_selector(token: str) -> str:
    return "." + re.sub(r"([^a-zA-Z0-9_-])", lambda m: "\\" + m.group(1), token)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def alpha_to_float(value: str) -> float:
    if value.startswith("[") and value.endswith("]"):
        return float(value[1:-1])
    return float(value) / 100.0


def resolve_color(token: str) -> str | None:
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1]
        if inner.startswith("#"):
            return inner
        return inner
    alpha = None
    base = token
    if "/" in token:
        base, alpha = token.split("/", 1)
    if base not in COLORS:
        return None
    color = COLORS[base]
    if alpha is None:
        return color
    r, g, b = hex_to_rgb(color)
    return f"rgba({r}, {g}, {b}, {alpha_to_float(alpha):.4f})"


def resolve_size(token: str, mapping: dict[str, str]) -> str | None:
    if token.startswith("[") and token.endswith("]"):
        return token[1:-1].replace("_", " ")
    return mapping.get(token)


def rule(declarations: str, template: str = "{selector}") -> tuple[str, str]:
    return template, declarations


def utility_rule(base: str) -> tuple[str, str] | None:
    exact = {
        "absolute": rule("position:absolute;"),
        "fixed": rule("position:fixed;"),
        "relative": rule("position:relative;"),
        "sticky": rule("position:sticky;"),
        "hidden": rule("display:none;"),
        "inline": rule("display:inline;"),
        "inline-block": rule("display:inline-block;"),
        "inline-flex": rule("display:inline-flex;"),
        "flex": rule("display:flex;"),
        "flex-row": rule("flex-direction:row;"),
        "grid": rule("display:grid;"),
        "border": rule("border-width:1px;border-style:solid;"),
        "border-0": rule("border-width:0;"),
        "border-b": rule("border-bottom-width:1px;border-bottom-style:solid;"),
        "border-t": rule("border-top-width:1px;border-top-style:solid;"),
        "border-r": rule("border-right-width:1px;border-right-style:solid;"),
        "border-dashed": rule("border-style:dashed;"),
        "font-bold": rule("font-weight:700;"),
        "font-medium": rule("font-weight:500;"),
        "font-normal": rule("font-weight:400;"),
        "font-semibold": rule("font-weight:600;"),
        "font-mono": rule("font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace;"),
        "font-sans": rule('font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;'),
        "uppercase": rule("text-transform:uppercase;"),
        "text-center": rule("text-align:center;"),
        "text-right": rule("text-align:right;"),
        "leading-tight": rule("line-height:1.25;"),
        "leading-relaxed": rule("line-height:1.625;"),
        "truncate": rule("overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"),
        "whitespace-nowrap": rule("white-space:nowrap;"),
        "pointer-events-none": rule("pointer-events:none;"),
        "object-contain": rule("object-fit:contain;"),
        "overflow-hidden": rule("overflow:hidden;"),
        "overflow-x-auto": rule("overflow-x:auto;"),
        "overflow-y-auto": rule("overflow-y:auto;"),
        "min-h-full": rule("min-height:100%;"),
        "min-h-screen": rule("min-height:100vh;"),
        "h-full": rule("height:100%;"),
        "w-full": rule("width:100%;"),
        "min-w-0": rule("min-width:0;"),
        "select-none": rule("user-select:none;"),
        "antialiased": rule("-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;"),
        "top-0": rule("top:0;"),
        "right-0": rule("right:0;"),
        "left-0": rule("left:0;"),
        "inset-0": rule("top:0;right:0;bottom:0;left:0;"),
        "inset-y-0": rule("top:0;bottom:0;"),
        "flex-1": rule("flex:1 1 0%;"),
        "flex-col": rule("flex-direction:column;"),
        "flex-wrap": rule("flex-wrap:wrap;"),
        "flex-shrink-0": rule("flex-shrink:0;"),
        "items-center": rule("align-items:center;"),
        "items-start": rule("align-items:flex-start;"),
        "items-end": rule("align-items:flex-end;"),
        "justify-between": rule("justify-content:space-between;"),
        "justify-center": rule("justify-content:center;"),
        "justify-end": rule("justify-content:flex-end;"),
        "opacity-40": rule("opacity:0.4;"),
        "opacity-80": rule("opacity:0.8;"),
        "transition": rule("transition-property:color,background-color,border-color,text-decoration-color,fill,stroke,opacity,box-shadow,transform,filter,backdrop-filter;transition-duration:150ms;transition-timing-function:cubic-bezier(0.4,0,0.2,1);"),
        "transition-transform": rule("transition-property:transform;transition-duration:150ms;transition-timing-function:cubic-bezier(0.4,0,0.2,1);"),
        "duration-200": rule("transition-duration:200ms;"),
        "backdrop-blur-sm": rule("backdrop-filter:blur(4px);"),
        "sr-only": rule("position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border-width:0;"),
        "underline": rule("text-decoration:underline;"),
        "shadow-inner": rule("box-shadow:inset 0 2px 4px 0 rgba(15,23,42,0.08);"),
        "shadow-md": rule("box-shadow:0 4px 6px -1px var(--tw-shadow-color, rgba(15,23,42,0.12)),0 2px 4px -2px var(--tw-shadow-color, rgba(15,23,42,0.08));"),
        "shadow-lg": rule("box-shadow:0 10px 15px -3px var(--tw-shadow-color, rgba(15,23,42,0.14)),0 4px 6px -4px var(--tw-shadow-color, rgba(15,23,42,0.1));"),
        "shadow-xl": rule("box-shadow:0 20px 25px -5px var(--tw-shadow-color, rgba(15,23,42,0.15)),0 8px 10px -6px var(--tw-shadow-color, rgba(15,23,42,0.1));"),
        "shadow-2xl": rule("box-shadow:0 25px 50px -12px var(--tw-shadow-color, rgba(15,23,42,0.25));"),
        "bg-gradient-to-r": rule("background-image:linear-gradient(to right,var(--tw-gradient-from),var(--tw-gradient-via, var(--tw-gradient-to)));"),
        "bg-gradient-to-br": rule("background-image:linear-gradient(to bottom right,var(--tw-gradient-from),var(--tw-gradient-via, var(--tw-gradient-to)));"),
        "-translate-x-full": rule("transform:translateX(-100%);"),
        "translate-x-0": rule("transform:translateX(0);"),
        "-translate-y-[1px]": rule("transform:translateY(-1px);"),
        "text-base": rule(f"font-size:{TEXT_SIZES['base']};"),
        "text-sm": rule(f"font-size:{TEXT_SIZES['sm']};"),
        "text-xs": rule(f"font-size:{TEXT_SIZES['xs']};"),
        "text-lg": rule(f"font-size:{TEXT_SIZES['lg']};"),
        "text-xl": rule(f"font-size:{TEXT_SIZES['xl']};"),
        "text-2xl": rule(f"font-size:{TEXT_SIZES['2xl']};"),
        "text-3xl": rule(f"font-size:{TEXT_SIZES['3xl']};"),
        "tracking-wide": rule("letter-spacing:0.025em;"),
    }
    if base in exact:
        return exact[base]
    if base in RADIUS:
        return rule(f"border-radius:{RADIUS[base]};")
    if re.fullmatch(r"z-\d+", base):
        return rule(f"z-index:{base.split('-', 1)[1]};")
    if re.fullmatch(r"z-\[[^\]]+\]", base):
        return rule(f"z-index:{base[3:-1]};")
    if re.fullmatch(r"(top|right|left)-.+", base):
        side, value_key = base.split("-", 1)
        value = resolve_size(value_key, SPACING)
        if value:
            return rule(f"{side}:{value};")
    if base.startswith("text-[") and base.endswith("]"):
        return rule(f"font-size:{base[6:-1]};")
    if base.startswith("tracking-[") and base.endswith("]"):
        return rule(f"letter-spacing:{base[10:-1]};")
    for prefix, prop in (("p-", "padding"), ("px-", "padding-left|padding-right"), ("py-", "padding-top|padding-bottom"),
                         ("pt-", "padding-top"), ("pb-", "padding-bottom"), ("pl-", "padding-left"),
                         ("mt-", "margin-top"), ("mb-", "margin-bottom"), ("mx-", "margin-left|margin-right"), ("my-", "margin-top|margin-bottom")):
        if base.startswith(prefix):
            raw = base[len(prefix):]
            if raw == "auto":
                value = "auto"
            else:
                value = resolve_size(raw, SPACING)
            if value:
                if "|" in prop:
                    a, b = prop.split("|")
                    return rule(f"{a}:{value};{b}:{value};")
                return rule(f"{prop}:{value};")
    if base == "ml-auto":
        return rule("margin-left:auto;")
    for prefix, prop, source in (
        ("w-", "width", SPACING),
        ("h-", "height", SPACING),
        ("min-w-", "min-width", SPACING),
        ("max-w-", "max-width", MAX_WIDTH),
    ):
        if base.startswith(prefix):
            raw = base[len(prefix):]
            value = resolve_size(raw, source)
            if value is None and prefix in {"w-", "h-", "min-w-", "max-w-"}:
                value = resolve_size(raw, SPACING)
            if value:
                return rule(f"{prop}:{value};")
    if base.startswith("grid-cols-"):
        raw = base[len("grid-cols-"):]
        if raw.isdigit():
            return rule(f"grid-template-columns:repeat({raw},minmax(0,1fr));")
        value = resolve_size(raw, {})
        if value:
            return rule(f"grid-template-columns:{value};")
    if base.startswith("col-span-"):
        raw = base[len("col-span-"):]
        if raw.isdigit():
            return rule(f"grid-column:span {raw} / span {raw};")
    if base.startswith("gap-"):
        value = resolve_size(base[4:], SPACING)
        if value:
            return rule(f"gap:{value};")
    if base.startswith("space-y-"):
        value = resolve_size(base[8:], SPACING)
        if value:
            return rule(f"margin-top:{value};", "{selector} > :not([hidden]) ~ :not([hidden])")
    if base.startswith("space-x-"):
        value = resolve_size(base[8:], SPACING)
        if value:
            return rule(f"margin-left:{value};", "{selector} > :not([hidden]) ~ :not([hidden])")
    if base == "divide-y":
        return rule("border-top-width:1px;border-top-style:solid;", "{selector} > :not([hidden]) ~ :not([hidden])")
    if base.startswith("divide-"):
        color = resolve_color(base[len("divide-"):])
        if color:
            return rule(f"border-top-color:{color};", "{selector} > :not([hidden]) ~ :not([hidden])")
    if base.startswith("bg-"):
        color = resolve_color(base[3:])
        if color:
            return rule(f"background-color:{color};")
    if base.startswith("text-"):
        color = resolve_color(base[5:])
        if color:
            return rule(f"color:{color};")
    if base.startswith("border-"):
        color = resolve_color(base[7:])
        if color:
            return rule(f"border-color:{color};")
    if base.startswith("from-"):
        color = resolve_color(base[5:])
        if color:
            return rule(f"--tw-gradient-from:{color};--tw-gradient-to:{color};")
    if base.startswith("via-"):
        color = resolve_color(base[4:])
        if color:
            return rule(f"--tw-gradient-via:{color};")
    if base.startswith("to-"):
        color = resolve_color(base[3:])
        if color:
            return rule(f"--tw-gradient-to:{color};")
    if base.startswith("shadow-"):
        color = resolve_color(base[7:])
        if color:
            return rule(f"--tw-shadow-color:{color};")
    if base.startswith("ring-"):
        color = resolve_color(base[len("ring-"):])
        if color:
            return rule(f"box-shadow:0 0 0 3px {color};")
    return None


def wrap_rule(token: str, template: str, declarations: str) -> str:
    parts = split_variants(token)
    variants = parts[:-1]
    selector = escape_selector(token)
    base_selector = selector
    media_queries: list[str] = []

    for variant in variants:
        if variant in BREAKPOINTS:
            media_queries.append(f"@media (min-width: {BREAKPOINTS[variant]})")
        elif variant == "hover":
            base_selector += ":hover"
        elif variant == "focus":
            base_selector += ":focus"

    css = f"{template.format(selector=base_selector)}{{{declarations}}}"
    for media in reversed(media_queries):
        css = f"{media}{{{css}}}"
    return css


def collect_tokens() -> list[str]:
    tokens: set[str] = set()
    for path in TEMPLATES:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r'class="([^"]+)"', text):
            for token in match.group(1).split():
                if "{{" in token or "{%" in token or token in IGNORE:
                    continue
                if token.endswith("%}") or token.startswith("%}"):
                    continue
                if any(piece in token for piece in ("'", "==")):
                    continue
                if token in {"if", "else", "endif", "in", "not", "num", "status_filter", "preview_mode"}:
                    continue
                if "." in token and token not in {"space-y-0.5", "gap-1.5", "gap-2.5", "mt-0.5", "mt-1.5", "mt-2.5", "py-2.5", "h-2.5", "w-2.5", "text-[9.5px]"}:
                    continue
                tokens.add(token)
    return sorted(tokens)


def build_css() -> tuple[str, list[str]]:
    rules: list[str] = [
        "/* Local utility subset replacing the Tailwind CDN in production. */",
        "*,::before,::after{box-sizing:border-box;}",
        ".transform{transform:translate(var(--tw-translate-x,0),var(--tw-translate-y,0));}",
    ]
    unknown: list[str] = []
    for token in collect_tokens():
        info = utility_rule(token)
        if info is None:
            parts = split_variants(token)
            if len(parts) > 1:
                info = utility_rule(parts[-1])
        if info is None:
            unknown.append(token)
            continue
        template, declarations = info
        rules.append(wrap_rule(token, template, declarations))
    return "\n".join(rules) + "\n", unknown


def update_manifest(asset_name: str, content: str) -> None:
    STATICFILES_DIR.mkdir(parents=True, exist_ok=True)
    plain_target = STATICFILES_DIR / asset_name
    plain_target.write_text(content, encoding="utf-8")

    digest = hashlib.md5(content.encode("utf-8")).hexdigest()[:12]
    hashed_name = f"{Path(asset_name).stem}.{digest}{Path(asset_name).suffix}"
    (STATICFILES_DIR / hashed_name).write_text(content, encoding="utf-8")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    data["paths"][f"css/{asset_name}"] = f"css/{hashed_name}"
    manifest_bytes = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    data["hash"] = hashlib.md5(manifest_bytes).hexdigest()[:12]
    MANIFEST.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")


def main() -> None:
    css, unknown = build_css()
    OUTPUT.write_text(css, encoding="utf-8")
    update_manifest("tailwind-lite.css", css)
    if unknown:
        print("Unknown tokens:")
        for token in unknown:
            print(token)
    else:
        print("All tokens handled.")


if __name__ == "__main__":
    main()
