import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = "/Users/weipeilong/Downloads/璀璨家的空气答案_层高篇脚本 (1).xlsx";
const outDir = "/Users/weipeilong/Desktop/Aaaaaaa/AI工作台/06_codex项目/璀璨codex任务/output/EP01_script_v4/00_script_inspection";

await fs.mkdir(outDir, { recursive: true });
const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);

const sheetSummary = await workbook.inspect({
  kind: "sheet",
  include: "id,name",
  maxChars: 12000,
});

const workbookSummary = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 16000,
  tableMaxRows: 12,
  tableMaxCols: 14,
  tableMaxCellChars: 180,
});

const sheets = [];
for (let index = 0; ; index += 1) {
  let sheet;
  try {
    sheet = workbook.worksheets.getItemAt(index);
  } catch {
    break;
  }
  if (!sheet) break;
  const used = sheet.getUsedRange();
  const item = {
    index,
    name: sheet.name,
    address: used?.address ?? null,
    values: used?.values ?? [],
    formulas: used?.formulas ?? [],
  };
  sheets.push(item);

  const preview = await workbook.render({
    sheetName: sheet.name,
    autoCrop: "all",
    scale: 1.5,
    format: "png",
  });
  const bytes = new Uint8Array(await preview.arrayBuffer());
  const safeName = sheet.name.replace(/[\\/:*?"<>|]/g, "_");
  await fs.writeFile(path.join(outDir, `${String(index + 1).padStart(2, "0")}_${safeName}.png`), bytes);
}

await fs.writeFile(
  path.join(outDir, "workbook_inspection.json"),
  JSON.stringify(
    {
      input: inputPath,
      sheetSummary: sheetSummary.ndjson,
      workbookSummary: workbookSummary.ndjson,
      sheets,
    },
    null,
    2,
  ),
  "utf8",
);

console.log(JSON.stringify({ outDir, sheetCount: sheets.length, sheets: sheets.map((s) => ({ name: s.name, address: s.address, rows: s.values.length, cols: s.values[0]?.length ?? 0 })) }, null, 2));
