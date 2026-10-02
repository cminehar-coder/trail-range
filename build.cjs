const fs=require('node:fs');
fs.mkdirSync('dist',{recursive:true});
fs.cpSync('public','dist',{recursive:true});
console.log('Built standalone static site in dist/.');
