import {readFileSync,writeFileSync} from 'node:fs';
import ts from 'typescript';
import {SUBJECT_INDEX,SUBJECT_STATS} from '../src/data/chapterIndex.generated';
let source=readFileSync('src/data/chapterIndex.generated.ts','utf8');
for(const [name,value] of Object.entries({SUBJECT_INDEX:SUBJECT_INDEX.filter(s=>['english_listening','english_grammar'].includes(s.id)),SUBJECT_STATS:{english_listening:SUBJECT_STATS.english_listening,english_grammar:SUBJECT_STATS.english_grammar}})) {
 const ast=ts.createSourceFile('index.ts',source,ts.ScriptTarget.Latest,true);
 function visit(n:ts.Node){if(ts.isVariableDeclaration(n)&&n.name.getText(ast)===name&&n.initializer){const p=n.initializer;source=source.slice(0,p.getStart(ast))+JSON.stringify(value,null,2)+source.slice(p.end);}else ts.forEachChild(n,visit);}visit(ast);
}
writeFileSync('src/data/chapterIndex.generated.ts',source);
