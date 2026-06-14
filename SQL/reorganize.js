const fs = require('fs');
const path = require('path');

const targetDir = 'D:\\learning\\theory\\SQL';

const files = [
  "00_Introduction_And_Setup.md",
  "01_What_Is_SQL.md",
  "02_Databases_And_Tables.md",
  "03_Data_Types.md",
  "04_Create_Drop_Alter.md",
  "05_Insert_Update_Delete.md",
  "06_Select_Basics.md",
  "07_Where_Clause_And_Filters.md",
  "08_Sorting_And_Limiting.md",
  "09_Aggregate_Functions.md",
  "10_Group_By_And_Having.md",
  "11_Joins.md",
  "12_Subqueries.md",
  "13_Views.md",
  "14_Indexes.md",
  "15_Transactions.md",
  "16_Stored_Procedures.md",
  "17_Triggers.md",
  "18_Normalization.md",
  "19_SQL_Vs_NoSQL.md",
  "20_Final_Project.md",
  "21_Deployment_On_EC2.md"
];

// 1. Create file mappings
const mappings = files.map((oldName) => {
  const num = parseInt(oldName.slice(0, 2));
  const newNum = String(num + 1).padStart(2, '0');
  const newName = newNum + oldName.slice(2);
  return { oldName, newName, index: num };
});

console.log("Mappings created:", mappings.length);

// Helper to transform the footer
function transformFooter(content, isFirst, isLast) {
  const lines = content.split('\n');
  let rowIdx = -1;
  let separatorIdx = -1;
  for (let i = lines.length - 1; i >= lines.length - 15 && i >= 0; i--) {
    const line = lines[i].trim();
    if (line.startsWith('|') && (line.includes('Previous:') || line.includes('Next:') || line.includes('Congratulations!'))) {
      rowIdx = i;
      if (i + 1 < lines.length && lines[i + 1].trim().startsWith('|---')) {
        separatorIdx = i + 1;
      }
      break;
    }
  }
  
  if (rowIdx === -1 || separatorIdx === -1) {
    console.log("Warning: Could not find footer in file content.");
    return content;
  }
  
  const row = lines[rowIdx];
  const cells = row.split('|').map(c => c.trim()).filter((c, idx, arr) => idx > 0 && idx < arr.length - 1);
  
  let newRow = "";
  let newSeparator = "";
  
  if (isFirst) {
    newRow = `| [Index](./00_index.md) | ${cells[1]} |`;
    newSeparator = `|---|---|`;
  } else if (isLast) {
    newRow = `| ${cells[0]} | [Index](./00_index.md) | ${cells[1]} |`;
    newSeparator = `|---|---|---|`;
  } else {
    newRow = `| ${cells[0]} | [Index](./00_index.md) | ${cells[1]} |`;
    newSeparator = `|---|---|---|`;
  }
  
  lines[rowIdx] = newRow;
  lines[separatorIdx] = newSeparator;
  return lines.join('\n');
}

// 2. Process files in reverse order
for (let i = mappings.length - 1; i >= 0; i--) {
  const { oldName, newName, index } = mappings[i];
  const oldPath = path.join(targetDir, oldName);
  const newPath = path.join(targetDir, newName);
  
  console.log(`Processing: ${oldName} -> ${newName}`);
  
  if (!fs.existsSync(oldPath)) {
    console.error(`Error: File does not exist at ${oldPath}`);
    continue;
  }
  
  let content = fs.readFileSync(oldPath, 'utf8');
  
  // Transform footer navigation
  const isFirst = (index === 0);
  const isLast = (index === mappings.length - 1);
  content = transformFooter(content, isFirst, isLast);
  
  // Replace internal file name references (descending order to prevent cascade)
  for (let j = mappings.length - 1; j >= 0; j--) {
    const map = mappings[j];
    // Global replace for the filename
    content = content.split(map.oldName).join(map.newName);
  }
  
  // Write to new path
  fs.writeFileSync(newPath, content, 'utf8');
  console.log(`Wrote: ${newName}`);
  
  // Delete old file
  fs.unlinkSync(oldPath);
  console.log(`Deleted: ${oldName}`);
}

console.log("All files shifted successfully!");
