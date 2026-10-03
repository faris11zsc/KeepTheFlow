/**
 * Lesson Integrity Validator
 * ──────────────────────────
 * Scans every lesson in D:\KeepTheFlow\lessons\ and verifies:
 *   1. Every admin-hide-btn has a matching admin-copy-link-btn (same data-instance)
 *   2. The JS reveal logic shows copy-link buttons for admins
 *   3. The JS click handler for copy-link exists with clipboard.writeText
 *
 * Run:  node D:\KeepTheFlow\validate-lessons.js
 * Exit code 0 = all OK, 1 = failures found
 */
const fs = require('fs');
const path = require('path');

const lessonsDir = 'D:\\KeepTheFlow\\lessons';
const dirs = fs.readdirSync(lessonsDir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);

let allPassed = true;
const results = [];

for (const dir of dirs) {
    const file = path.join(lessonsDir, dir, 'index.html');
    if (!fs.existsSync(file)) continue;

    const html = fs.readFileSync(file, 'utf8');
    const errors = [];

    // Extract all data-instance IDs from hide buttons
    const hideInstances = new Set();
    const hideRegex = /admin-hide-btn[^>]*data-instance="(\d+)"/g;
    let m;
    while ((m = hideRegex.exec(html)) !== null) hideInstances.add(m[1]);

    // Extract all data-instance IDs from copy-link buttons
    const copyInstances = new Set();
    const copyRegex = /admin-copy-link-btn[^>]*data-instance="(\d+)"/g;
    while ((m = copyRegex.exec(html)) !== null) copyInstances.add(m[1]);

    // Check 1: Every hide instance must have a copy instance
    const missingCopy = [...hideInstances].filter(id => !copyInstances.has(id));
    if (missingCopy.length > 0) {
        errors.push(`MISSING ${missingCopy.length} copy-link buttons (have hide but no copy)`);
    }

    // Check 2: Reveal logic
    const hasReveal = /admin-copy-link-btn.*forEach.*display|querySelectorAll.*admin-copy-link-btn.*display/.test(html);
    if (!hasReveal && copyInstances.size > 0) {
        errors.push('MISSING JS reveal logic for admin-copy-link-btn');
    }

    // Check 3: Click handler with clipboard
    const hasClickHandler = /admin-copy-link-btn.*forEach[\s\S]{0,500}clipboard\.writeText/.test(html);
    if (!hasClickHandler && copyInstances.size > 0) {
        errors.push('MISSING JS click handler with clipboard for admin-copy-link-btn');
    }

    const status = errors.length === 0 ? '✅' : '❌';
    if (errors.length > 0) allPassed = false;

    results.push({
        lesson: dir,
        status,
        hideCount: hideInstances.size,
        copyCount: copyInstances.size,
        errors
    });
}

console.log('\n  ╔══════════════════════════════════════════════════╗');
console.log('  ║     LESSON INTEGRITY VALIDATOR                  ║');
console.log('  ╚══════════════════════════════════════════════════╝\n');

for (const r of results) {
    console.log(`  ${r.status} ${r.lesson}  (hide=${r.hideCount}, copy=${r.copyCount})`);
    for (const e of r.errors) console.log(`     ❌ ${e}`);
}

console.log('\n  ' + (allPassed ? '✅ ALL LESSONS PASSED' : '❌ FAILURES DETECTED — fix before deploying'));
console.log('');

process.exit(allPassed ? 0 : 1);
