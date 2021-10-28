#! /usr/bin/env node
// Add to the current folder your custom translation strings, with the following file hierarchy:
//
//   i18n/
//     <app name>/
//       <language code>.json
//
// For instance, to override French strings from the payment app:
//
//   i18n/
//     payment/
//       fr.json
//
// Your custom translation strings will automatically be compiled in the MFE Docker image.

const fs = require('fs');
const path = require('path');

function main() {
  // Merge the messages from multiple directories and aggregate the content in a single directory.
  // This is certainly not great idiomatic nodejs code. Please open a PR to improve this bit!
  merge(process.argv[2], process.argv[3], process.argv[4])
}

function merge(dir1, dir2, outputDir) {
  fs.readdirSync(dir1, {
    withFileTypes: true
  }).forEach(file1 => {
    if (file1.isFile() && file1.name.endsWith(".json")) {
      var path1 = path.resolve(path.join(dir1, file1.name));
      var data1 = require(path1);
      var path2 = path.resolve(path.join(dir2, file1.name));
      fs.access(path2, (err) => {
        if (err) {
          return;
        }
        var pathOutput = path.resolve(path.join(outputDir, file1.name));
        console.log("Merging i18 strings from " + path1 + " with " + path2 + " to " + pathOutput);
        var data2 = require(path2);
        var final = Object.assign(data1, data2);
        fs.writeFileSync(pathOutput, JSON.stringify(final, null, 2));
      });
    }
  });
}

main()
