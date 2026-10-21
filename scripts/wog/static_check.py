# -*- coding: utf-8 -*-
"""Static cross-check: L.<fn> usages vs WOG_LOGIC keys, engine fns vs engines.
Catches 'works only if user clicks X first' bugs without a browser."""
import io, os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib

ENGINE_FNS = {
    "common": {"$", "$$", "ce", "fa", "FA_D", "shuffle", "rint", "pick", "clamp",
               "toast", "hud", "ovl", "bestOf", "storeBest", "store"},
    "card": {"makeDeck", "isRed", "suitOf", "rankShort", "rankFa", "cardEl", "cardStack", "SUITS"},
    "arcade": {"makeCanvas", "keyState", "bindPad", "rafStep"},
    "word": {"FA_LETTERS", "normFa", "faKb"},
}

def extract_section(src, start, end):
    i = src.find(start)
    j = src.find(end, i + len(start)) if i >= 0 else -1
    if i < 0 or j < 0:
        return None
    return src[i + len(start):j]

def game_sources(g):
    """Return (ui_code, logic_code, engines) for a G instance."""
    return g.ui, g.logic, g.engines

def extract_wog_logic_keys(logic):
    """Find `var WOG_LOGIC={...}` with balanced braces; return key set."""
    m = re.search(r'var\s+WOG_LOGIC\s*=\s*\{', logic)
    if not m:
        return None
    i = m.end() - 1
    depth = 0
    for j in range(i, len(logic)):
        if logic[j] == '{':
            depth += 1
        elif logic[j] == '}':
            depth -= 1
            if depth == 0:
                body = logic[i + 1:j]
                break
    else:
        return None
    keys = set(re.findall(r'(?:^|[,{])\s*([A-Za-z_$][\w$]*)\s*:', body))
    return keys

problems = []
batch_files = sorted(__import__("glob").glob(os.path.join(HERE, "games", "*.py")))

for bf in batch_files:
    import importlib.util
    sys.modules.setdefault('lib_mini', lib)
    spec = importlib.util.spec_from_file_location(os.path.basename(bf)[:-3], bf)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        problems.append(("BATCH %s load" % bf, str(e)[:120]))
        continue
    for g in getattr(mod, "GAMES", []):
        ui, logic, engines = game_sources(g)
        eng_set = set(engines) if engines else {"common"}
        avail = set()
        for e in eng_set:
            avail |= ENGINE_FNS[e]
        # 1) engine function usage vs availability
        for fn in sorted(avail):
            if fn == "store":
                continue
            if re.search(r'(?<![.\w])' + re.escape(fn) + r'\s*\(', ui):
                pass  # available, fine
        used_fns = set()
        for fn in set().union(*ENGINE_FNS.values()):
            if fn == "store":
                continue
            if re.search(r'(?<![.\w])' + re.escape(fn) + r'\s*\(', ui):
                used_fns.add(fn)
        missing_eng = used_fns - avail
        if missing_eng:
            problems.append((g.slug, "uses %s but engines=%s" % (sorted(missing_eng), engines)))
        # 2) L.<fn> usages vs WOG_LOGIC keys
        keys = extract_wog_logic_keys(logic)
        if keys is None:
            problems.append((g.slug, "WOG_LOGIC literal not found"))
            continue
        # shorthand keys like  {norm,feedback}  -> also catch 'fnName' in short form
        used_l = set(re.findall(r'\bL\.([A-Za-z_$][\w$]*)', ui))
        miss = used_l - keys
        if miss:
            problems.append((g.slug, "L.%s used in UI but not exported" % sorted(miss)))
        # 3) functions called in UI that exist nowhere (neither engines, nor logic, nor defined in ui)
        ui_defs = set(re.findall(r'function\s+([A-Za-z_$][\w$]*)', ui)) | set(re.findall(r'var\s+([A-Za-z_$][\w$]*)\s*=\s*function', ui))
        known = avail | keys | ui_defs | {"init", "draw", "update", "render", "tick", "move", "ai",
                                          "requestAnimationFrame", "setTimeout", "setInterval", "clearTimeout",
                                          "clearInterval", "parseInt", "parseFloat", "isNaN", "String", "Number",
                                          "Math", "JSON", "Object", "Array", "Date", "Boolean", "RegExp", "Error"}
        calls = set(re.findall(r'(?<![.\w$])([a-z][A-Za-z_$][\w$]*)\s*\(', ui))
        builtin_ok = {"document", "window", "console", "alert", "try", "catch", "function", "if", "for",
                      "while", "switch", "return", "typeof", "new", "var", "let", "const"}
        unknown = calls - known - builtin_ok
        # filter likely local closures: defined anywhere in ui as var x = ...
        vars_defined = set(re.findall(r'var\s+([A-Za-z_$][\w$]*)', ui))
        unknown -= vars_defined
        if unknown:
            problems.append((g.slug, "UI calls undefined-looking: %s" % sorted(unknown)[:10]))

print("STATIC CHECK: %d problems" % len(problems))
for slug, p in problems:
    print("---", slug, "::", p)
