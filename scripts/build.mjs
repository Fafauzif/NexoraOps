import{rm,mkdir,cp}from'node:fs/promises';
await rm(new URL('../dist/',import.meta.url),{recursive:true,force:true});await mkdir(new URL('../dist/',import.meta.url),{recursive:true});await cp(new URL('../website/',import.meta.url),new URL('../dist/',import.meta.url),{recursive:true});console.log('Built NexoraOps → dist/ (no external runtime dependencies)');
