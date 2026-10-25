// Reproducible native-SVG export. Requires Playwright and a local Edge browser.
// Optional TELARIO_PLAYWRIGHT_MODULE may point to an existing playwright/index.mjs.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const { chromium } = await import(process.env.TELARIO_PLAYWRIGHT_MODULE || 'playwright');
const root=process.env.TELARIO_PORTFOLIO_ROOT || path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(root,'assets/images/portfolio/telario');
const logo=await fs.readFile(path.join(output,'telario-logo.svg'),'utf8');
const mark=await fs.readFile(path.join(output,'telario-mark.svg'),'utf8');
const browser=await chromium.launch({channel:process.env.PLAYWRIGHT_BROWSER_CHANNEL || 'msedge'});
try{
 for(const job of [
  {name:'telario-index.jpg',width:1280,height:720,logoWidth:760,svg:logo,type:'jpeg'},
  {name:'telario-cover.jpg',width:1536,height:1024,logoWidth:900,svg:logo,type:'jpeg'},
  {name:'telario-logo-1024x1024.png',width:1024,height:1024,logoWidth:560,svg:mark,type:'png'},
 ]){
  const page=await browser.newPage({viewport:{width:job.width,height:job.height},deviceScaleFactor:1});
  await page.setContent(`<html><head><meta charset="utf-8"><style>*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden}body{background:#F7F5EF;display:flex;align-items:center;justify-content:center}.brand{width:${job.logoWidth}px}.brand svg{display:block;width:100%;height:auto}</style></head><body><div class="brand">${job.svg}</div></body></html>`);
  await page.screenshot({path:path.join(output,job.name),type:job.type,...(job.type==='jpeg'?{quality:96}:{})});
  await page.close();
  console.log(`${job.name}: ${job.width}×${job.height}; logo box ${job.logoWidth}px`);
 }
}finally{await browser.close();}
