import os
import glob
import re

css_snippet = """
.exit-lesson-btn {
    position: fixed;
    top: 14px;
    left: 14px;
    z-index: 998;
    display: flex;
    align-items: center;
    justify-content: center;
    background: color-mix(in srgb, var(--bg) 80%, var(--line) 20%);
    color: var(--ref);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid color-mix(in srgb, var(--ref) 12%, transparent);
    border-radius: 99px;
    padding: 6px 14px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    -webkit-tap-highlight-color: transparent;
}
.exit-lesson-btn:hover {
    border-color: color-mix(in srgb, var(--ref) 30%, transparent);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
</style>"""

html_snippet = """
<!-- Exit Lesson Button -->
<a href="https://keep-the-flow.vercel.app/" class="exit-lesson-btn" title="Return to Dashboard">
    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" style="margin-right: 6px;"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
    Dashboard
</a>
<!-- Theme Toggle -->"""

lessons_dir = r"D:\KeepTheFlow\lessons"

def patch_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'class="exit-lesson-btn"' in content:
        print(f"Skipping {path} - already patched.")
        return

    # Inject CSS before </style>
    # Note: We need to make sure we replace the LAST </style> before </head> or just the one associated with the main block.
    # Usually it's </style>\n</head>
    new_content = re.sub(r'</style>\s*</head>', css_snippet + '\n</head>', content, flags=re.IGNORECASE)

    # Inject HTML before <!-- Theme Toggle -->
    # Some older files might not have <!-- Theme Toggle --> but instead just <div class="theme-toggle"
    if '<!-- Theme Toggle -->' in new_content:
        new_content = new_content.replace('<!-- Theme Toggle -->', html_snippet)
    elif '<div class="theme-toggle"' in new_content:
        html_fallback = html_snippet.replace('<!-- Theme Toggle -->\n', '')
        new_content = new_content.replace('<div class="theme-toggle"', html_fallback + '\n<div class="theme-toggle"')
    else:
        # Fallback to after <body> if theme toggle is missing entirely
        new_content = re.sub(r'(<body[^>]*>)', r'\1\n' + html_snippet.replace('<!-- Theme Toggle -->\n', ''), new_content, count=1, flags=re.IGNORECASE)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Patched {path}")

def main():
    for root, dirs, files in os.walk(lessons_dir):
        for file in files:
            if file == "index.html":
                patch_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
