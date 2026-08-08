// Syntax-check every inline <script> block in frontend/index.html
const fs = require("fs");
const path = require("path");
const html = fs.readFileSync(path.join(__dirname, "..", "frontend", "index.html"), "utf8");
const blocks = html.split("<script>").slice(1).map(b => b.split("</script>")[0]);
let failed = 0;
blocks.forEach((block, i) => {
  try {
    new Function(block);
    console.log(`block ${i + 1} OK (${block.length} chars)`);
  } catch (e) {
    failed++;
    console.error(`block ${i + 1} SYNTAX ERROR: ${e.message}`);
  }
});
console.log(failed ? `FAILED: ${failed} blocks` : "ALL BLOCKS OK");
process.exit(failed ? 1 : 0);
