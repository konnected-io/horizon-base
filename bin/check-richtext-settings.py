#!/usr/bin/env python3
"""Validate `richtext` setting values in theme JSON against Shopify's allowlist.

WHY THIS EXISTS
---------------
`shopify theme check` is a static linter. It validates Liquid syntax, `{% schema %}`
JSON, translation keys and block-type references — but it never inspects a setting's
*value* against the rules for that setting's *type*. Those rules are enforced
server-side, when a file is uploaded (`shopify theme push`, or the GitHub sync).

For settings declared `"type": "richtext"`, Shopify permits only a small set of tags
and attributes. An offending value makes the upload reject the **entire template
file**. On `theme push` you at least get an error; on a GitHub-connected theme the
file is just silently absent, and every page using it falls back to the default
template. That is how four templates went missing from a preview theme in Sept 2026
while `theme check` reported 0 errors:

    Setting 'text' is invalid. Attribute 'data-content-slug="gdo-blaq"' is not
    permitted on tag '<a>' ...

Note that Shopify *also* strips these attributes at render time, so they never reach
the DOM from a richtext setting anyway — they are pure downside. Analytics hooks that
need to survive belong in a `custom-liquid` block, whose value is not sanitized
(see `page.joshai.json`, where the same `data-content-*` attributes do render).

USAGE
-----
    python3 bin/check-richtext-settings.py [root]

Exits 1 and prints every offending value if anything is found. `root` defaults to the
repo root; pass another directory to check a different checkout.
"""

import json
import os
import re
import sys

# Tags Shopify accepts inside a richtext value.
ALLOWED_TAGS = {
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'span', 'a',
    'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
}

# Attributes accepted per tag. `*` applies to every tag. `style` is listed because
# this theme ships it on <span> in templates Shopify accepts; `data-*`, `class` and
# `id` are NOT accepted and are what this check exists to catch.
ALLOWED_ATTRS = {
    '*': {'style'},
    'a': {'href', 'target', 'title', 'rel'},
}

TAG_RE = re.compile(r'<\s*(/?)([a-zA-Z][a-zA-Z0-9]*)((?:\s+[^\s=>]+(?:\s*=\s*"[^"]*")?)*)\s*/?>')
ATTR_RE = re.compile(r'(?:^|\s)([^\s=]+)(?:\s*=\s*"([^"]*)")?')


def richtext_ids(liquid_path):
    """Setting ids declared as `richtext` in a block's or section's {% schema %}."""
    try:
        source = open(liquid_path, encoding='utf-8').read()
    except OSError:
        return set()
    match = re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}', source, re.S)
    if not match:
        return set()
    try:
        schema = json.loads(match.group(1))
    except ValueError:
        return set()  # a schema we can't parse is theme-check's problem, not ours
    return {
        s['id'] for s in schema.get('settings', [])
        if isinstance(s, dict) and s.get('type') == 'richtext' and s.get('id')
    }


def load_json_with_comments(path):
    """Theme JSON files carry a leading /* ... */ banner written by Shopify."""
    raw = open(path, encoding='utf-8').read()
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', raw, count=1, flags=re.S))


def offenses(value):
    """Disallowed tags/attributes in one richtext value."""
    found = []
    for closing, tag, attrs, in ((m.group(1), m.group(2).lower(), m.group(3)) for m in TAG_RE.finditer(value)):
        if tag not in ALLOWED_TAGS:
            found.append('tag <%s>' % tag)
            continue
        if closing:
            continue
        permitted = ALLOWED_ATTRS.get('*', set()) | ALLOWED_ATTRS.get(tag, set())
        for name, _ in ATTR_RE.findall(attrs):
            if name and name.lower() not in permitted:
                found.append('attribute %s= on <%s>' % (name, tag))
    return found


def walk(node, path, richtext_by_type, results, filename):
    if isinstance(node, dict):
        settings = node.get('settings')
        node_type = node.get('type')
        if isinstance(settings, dict) and isinstance(node_type, str):
            for sid in richtext_by_type.get(node_type, set()):
                value = settings.get(sid)
                if isinstance(value, str):
                    for bad in offenses(value):
                        results.append((filename, path, node_type, sid, bad))
        for key, child in node.items():
            if key != 'settings':
                walk(child, '%s/%s' % (path, key) if path else key,
                     richtext_by_type, results, filename)
    elif isinstance(node, list):
        for index, child in enumerate(node):
            walk(child, '%s[%d]' % (path, index), richtext_by_type, results, filename)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    richtext_by_type = {}
    for folder in ('blocks', 'sections'):
        directory = os.path.join(root, folder)
        for name in sorted(os.listdir(directory)) if os.path.isdir(directory) else []:
            if name.endswith('.liquid'):
                richtext_by_type[name[:-len('.liquid')]] = richtext_ids(os.path.join(directory, name))

    targets = []
    for folder in ('templates', 'templates/metaobject', 'sections', 'config'):
        directory = os.path.join(root, folder)
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if name.endswith('.json'):
                targets.append(os.path.join(directory, name))

    results = []
    for path in targets:
        try:
            data = load_json_with_comments(path)
        except (ValueError, OSError):
            continue  # unparseable JSON is theme-check's job to report
        walk(data, '', richtext_by_type, results, os.path.relpath(path, root))

    if not results:
        print('richtext settings OK — %d JSON files checked' % len(targets))
        return 0

    print('Invalid richtext setting values (Shopify will reject these files on push):\n')
    for filename, path, node_type, sid, bad in results:
        print('  %s' % filename)
        print('      %s  (%s.%s)' % (path, node_type, sid))
        print('      %s\n' % bad)
    print('%d offense(s). Shopify strips these at render anyway; move analytics'
          ' hooks into a custom-liquid block instead.' % len(results))
    return 1


if __name__ == '__main__':
    sys.exit(main())
