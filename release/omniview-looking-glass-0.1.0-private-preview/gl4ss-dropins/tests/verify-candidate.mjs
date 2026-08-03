#!/usr/bin/env node

import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

function parseArgs(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key || !key.startsWith('--') || value === undefined) {
      throw new Error('Usage: node verify-candidate.mjs --control PATH --candidate PATH');
    }
    values[key.slice(2)] = path.resolve(value);
  }
  return values;
}

function run(command, args, cwd, encoding = 'utf8') {
  const result = spawnSync(command, args, {
    cwd,
    encoding,
    maxBuffer: 16 * 1024 * 1024,
    windowsHide: true,
  });
  if (result.error) throw result.error;
  if (result.status !== 0) {
    const stdout = result.stdout ? String(result.stdout) : '';
    const stderr = result.stderr ? String(result.stderr) : '';
    throw new Error(
      command + ' ' + args.join(' ') + ' failed with exit ' + result.status +
      '\n' + stdout + '\n' + stderr,
    );
  }
  return result.stdout;
}

async function sha256(filePath) {
  return createHash('sha256').update(await readFile(filePath)).digest('hex');
}

function pass(label) {
  process.stdout.write('PASS ' + label + '\n');
}

function ordered(text, phrases) {
  let cursor = -1;
  for (const phrase of phrases) {
    const next = text.indexOf(phrase);
    assert.ok(next > cursor, 'Expected ordered phrase: ' + phrase);
    cursor = next;
  }
}

function count(text, fragment) {
  return text.split(fragment).length - 1;
}

function hasExportModifier(node, ts) {
  return Boolean(node.modifiers?.some((modifier) => modifier.kind === ts.SyntaxKind.ExportKeyword));
}

function normal(text) {
  return text.replace(/\s+/g, ' ').trim();
}

function publicSurface(sourceText, fileName, ts) {
  const source = ts.createSourceFile(
    fileName,
    sourceText,
    ts.ScriptTarget.Latest,
    true,
    ts.ScriptKind.TS,
  );
  const names = [];
  const functions = {};
  const types = {};

  for (const statement of source.statements) {
    if (!hasExportModifier(statement, ts)) continue;

    if (ts.isFunctionDeclaration(statement) && statement.name) {
      const name = statement.name.text;
      names.push('function:' + name);
      const bodyStart = statement.body ? statement.body.getStart(source) : statement.end;
      functions[name] = normal(sourceText.slice(statement.getStart(source), bodyStart));
      continue;
    }

    if (ts.isInterfaceDeclaration(statement)) {
      const name = statement.name.text;
      names.push('interface:' + name);
      types[name] = statement.members.map((member) => {
        const memberName = member.name ? member.name.getText(source) : member.getText(source);
        const optional = member.questionToken ? '?' : '';
        const memberType = member.type ? member.type.getText(source) : member.getText(source);
        return normal(memberName + optional + ':' + memberType);
      });
      continue;
    }

    if (ts.isTypeAliasDeclaration(statement)) {
      const name = statement.name.text;
      names.push('type:' + name);
      types[name] = normal(statement.type.getText(source));
      continue;
    }

    if (ts.isEnumDeclaration(statement) || ts.isClassDeclaration(statement)) {
      const name = statement.name?.text ?? '<anonymous>';
      names.push(ts.SyntaxKind[statement.kind] + ':' + name);
      continue;
    }

    if (ts.isVariableStatement(statement)) {
      for (const declaration of statement.declarationList.declarations) {
        names.push('const:' + declaration.name.getText(source));
      }
    }
  }

  names.sort();
  return { names, functions, types };
}

async function comparePublicContracts(control, candidate, ts) {
  const files = [
    'src/lib/openrouter.ts',
    'src/lib/promptcraft.ts',
    'src/lib/promptTemplate.ts',
  ];

  for (const relative of files) {
    const controlText = await readFile(path.join(control, relative), 'utf8');
    const candidateText = await readFile(path.join(candidate, relative), 'utf8');
    const before = publicSurface(controlText, relative, ts);
    const after = publicSurface(candidateText, relative, ts);
    assert.deepEqual(after.names, before.names, relative + ' exported names changed');
    assert.deepEqual(after.functions, before.functions, relative + ' exported function signatures changed');
    assert.deepEqual(after.types, before.types, relative + ' exported type shapes changed');
  }
}

const args = parseArgs(process.argv.slice(2));
assert.ok(args.control, '--control is required');
assert.ok(args.candidate, '--candidate is required');

const packRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  '..',
);
const integrationRoot = path.join(packRoot, 'integration');
const baseline = JSON.parse(
  await readFile(path.join(integrationRoot, 'gl4ss-baseline.json'), 'utf8'),
);
const manifest = JSON.parse(
  await readFile(path.join(integrationRoot, 'dropin-manifest.json'), 'utf8'),
);

assert.equal(
  run('git', ['rev-parse', 'HEAD'], args.control).trim(),
  baseline.commit,
  'Control checkout is not at the frozen commit',
);
assert.equal(
  run('git', ['status', '--short'], args.control).trim(),
  '',
  'Control checkout is not pristine',
);
pass('frozen control commit and pristine state');

for (const file of baseline.files) {
  const target = path.join(args.control, file.path);
  assert.equal((await readFile(target)).length, file.bytes, file.path + ' byte count changed');
  assert.equal(await sha256(target), file.sha256, file.path + ' SHA-256 changed');
}
pass('frozen source bytes');

const patchPaths = manifest.patches.map((entry) => path.resolve(integrationRoot, entry.path));
for (let index = 0; index < manifest.patches.length; index += 1) {
  const entry = manifest.patches[index];
  const target = patchPaths[index];
  assert.equal((await readFile(target)).length, entry.bytes, entry.id + ' patch byte count changed');
  assert.equal(await sha256(target), entry.sha256, entry.id + ' patch SHA-256 changed');
}
pass('patch manifest bytes');

run('git', ['apply', '--check', ...patchPaths], args.control);
pass('combined git apply check');

for (let index = 0; index < manifest.patches.length; index += 1) {
  const entry = manifest.patches[index];
  const expected = run(
    'git',
    ['diff', '--no-ext-diff', '--binary', '--', ...entry.targets],
    args.candidate,
    null,
  );
  const actual = await readFile(patchPaths[index]);
  assert.ok(Buffer.from(expected).equals(actual), entry.id + ' patch differs from candidate bytes');
}
assert.deepEqual(
  run('git', ['diff', '--name-only'], args.candidate)
    .trim()
    .split(/\r?\n/)
    .filter(Boolean)
    .sort(),
  ['src/lib/openrouter.ts', 'src/lib/promptTemplate.ts', 'src/lib/promptcraft.ts'],
  'Candidate changed an unexpected tracked file',
);
pass('patches exactly reproduce the bounded candidate');

const typescriptModule = await import(
  pathToFileURL(path.join(args.candidate, 'node_modules', 'typescript', 'lib', 'typescript.js')).href,
);
const ts = typescriptModule.default ?? typescriptModule;
await comparePublicContracts(args.control, args.candidate, ts);
pass('public TypeScript contracts');

const viteModule = await import(
  pathToFileURL(path.join(args.candidate, 'node_modules', 'vite', 'dist', 'node', 'index.js')).href,
);
let plannerExposed = false;
const server = await viteModule.createServer({
  root: args.candidate,
  configFile: false,
  appType: 'custom',
  logLevel: 'error',
  optimizeDeps: { noDiscovery: true },
  server: { middlewareMode: true },
  plugins: [
    {
      name: 'expose-private-planner-for-verification',
      enforce: 'pre',
      transform(code, id) {
        const cleanId = id.split('?')[0].replaceAll('\\', '/');
        if (!cleanId.endsWith('/src/lib/openrouter.ts')) return null;
        const needle = 'function buildSceneDirectionPrompt(';
        assert.equal(count(code, needle), 1, 'Private planner seam moved or multiplied');
        plannerExposed = true;
        return {
          code: code.replace(needle, 'export function buildSceneDirectionPrompt('),
          map: null,
        };
      },
    },
  ],
});

try {
  const openrouter = await server.ssrLoadModule('/src/lib/openrouter.ts');
  const promptcraft = await server.ssrLoadModule('/src/lib/promptcraft.ts');
  const promptTemplate = await server.ssrLoadModule('/src/lib/promptTemplate.ts');
  assert.ok(plannerExposed, 'Planner test transform did not run');

  const location = 'Point Nemo';
  const coordinates = { lat: -48.8763, lng: -123.3933 };
  const neighbours = { earlier: 1400, later: 1600 };
  const style = 'ultraviolet salt-silver documentary';
  const wide = openrouter.buildSceneDirectionPrompt(
    location,
    coordinates,
    1500,
    'wide-field',
    style,
    neighbours,
    'midnight',
  );
  ordered(wide, [
    '1. SUPPORT',
    '2. GROUND',
    '3. PRESENCE',
    '4. TIME',
    '5. SCENE',
    '6. LIGHT',
  ]);
  for (const level of ['uninhabited', 'traces-only', 'sparse', 'settled', 'dense']) {
    assert.ok(wide.includes(level), 'Planner omitted habitation level ' + level);
  }
  for (const key of [
    '"habitation"',
    '"narrative"',
    '"atmosphere"',
    '"cameraNotes"',
    '"biome"',
    '"periodMarkers"',
    '"leftSubject"',
    '"centerSubject"',
    '"rightSubject"',
  ]) {
    assert.ok(wide.includes(key), 'Planner omitted JSON key ' + key);
  }
  assert.ok(wide.includes('LOCATION LABEL: "Point Nemo"'));
  assert.ok(wide.includes('COORDINATE: lat -48.88, lng -123.39'));
  assert.ok(wide.includes('FIXED LOCAL LIGHT: "midnight"'));
  assert.ok(wide.includes('VISUAL INTENTION: "' + style + '"'));
  assert.ok(wide.includes('Every field value is literal, image-ready description'));
  for (const taboo of [
    'do not',
    'never',
    'must not',
    'nothing',
    'no music',
    'no narration',
    'aftermath-free',
  ]) {
    assert.ok(!wide.toLowerCase().includes(taboo), 'Planner contains taboo-shaped cue: ' + taboo);
  }

  const selfie = openrouter.buildSceneDirectionPrompt(
    'Uruk',
    { lat: 31.3222, lng: 45.6361 },
    -3200,
    'chrono-selfie',
    null,
    { earlier: -3500, later: -2800 },
  );
  assert.ok(selfie.includes('"travelerLook"'));

  const cinematic = openrouter.buildSceneDirectionPrompt(
    location,
    coordinates,
    1500,
    'cinematic',
    null,
    neighbours,
    'midnight',
  );
  for (const key of ['"cinematicSubject"', '"cinematicCameraMove"', '"cinematicSoundCue"']) {
    assert.ok(cinematic.includes(key), 'Cinematic planner omitted ' + key);
  }
  pass('planner sequence, modes, schema, and positive emitted form');

  const expectedDefault = [
    '{capture}',
    '',
    '{subject}, at {location} in {year}. {habitation}',
    '',
    '{periodMarkers} {period}',
    '',
    '{biome}',
    '',
    '{light}',
    '',
    '{style}{aspect}',
  ].join('\n');
  const priorDefault = [
    '{capture}',
    '',
    '{subject}, at {location} in {year}.',
    '',
    '{habitation}',
    '',
    '{periodMarkers}',
    '',
    '{period}',
    '',
    '{biome}',
    '',
    '{light}',
    '',
    '{style}{aspect}',
  ].join('\n');
  assert.equal(promptTemplate.DEFAULT_IMAGE_TEMPLATE, expectedDefault);
  assert.ok(
    promptTemplate.LEGACY_IMAGE_TEMPLATES.includes(priorDefault),
    'Previous default is missing from legacy migration bytes',
  );
  assert.equal(
    promptTemplate.fillTemplate('CUSTOM {subject} {unknown}', { subject: 'salt-white swell' }),
    'CUSTOM salt-white swell {unknown}',
  );
  pass('default ordering, legacy migration, and unknown-placeholder behavior');

  const wildDirection = {
    habitation: 'uninhabited',
    narrative: 'Cold swell crosses the aperture.',
    atmosphere: 'salt haze dragged low beneath a black cloud shelf',
    cameraNotes: 'floating aperture 1.5 metres above the swell, level horizon, hard moonlight from camera left',
    periodMarkers: 'long-period swell lifting slate water, moonlit salt haze combed east by wind',
    biome: 'Open subantarctic ocean rolls beneath a low cloud shelf; wind shears white spray from the wave crests.',
    leftSubject: 'a slate swell shouldering into a torn fan of spray',
    centerSubject: 'crossing wave trains lifting one bright ridge',
    rightSubject: 'a rain squall drawing a charcoal veil across the horizon',
    cinematicSubject: 'crossing wave trains rise through moonlit spray',
    cinematicCameraMove: 'a slow lateral drift just above the swell',
    cinematicSoundCue: 'wind combing spray from the wave crests',
  };
  const wildOptions = {
    phase: 'midnight',
    location,
    coordinates,
    year: 1500,
    mode: 'wide-field',
    aspect: '16:9',
  };
  const wildPrompts = promptcraft.buildImagePromptsFromDirection(wildOptions, wildDirection);
  assert.equal(wildPrompts.length, 3);
  for (const prompt of wildPrompts) {
    assert.match(prompt, /^Shot on /);
    assert.ok(prompt.includes('Wilderness fills the frame.'));
    assert.ok(prompt.includes('The date is carried by ' + wildDirection.periodMarkers + '.'));
    assert.ok(
      prompt.includes(
        'Underfoot and through the distance: ' +
        wildDirection.biome.replace(/\.$/, '') +
        '.',
      ),
    );
    assert.ok(prompt.includes('Midnight.'));
    assert.ok(prompt.includes('an unforced composition held a little loose and off centre'));
    assert.ok(
      !/\b(garment|tool|crowd|smartphone|frescoed|walnut|gas-lamp)\b/i.test(prompt),
      'Wild prompt leaked peopled era matter',
    );
  }

  const denseDirection = {
    habitation: 'dense',
    narrative: 'Uruk works at full pressure.',
    atmosphere: 'sun-warmed dust turning luminous between walls',
    cameraNotes: 'roof-height view across a lane, near wall sharp, hard morning light from camera right',
    periodMarkers: 'bevelled mudbrick courses under fresh plaster, clay sealings passing hand to hand, reed baskets darkened by use',
    biome: 'Packed earthen lanes run between maintained mudbrick walls; irrigated date palms and reed beds mark the lower distance.',
    leftSubject: 'porters pivoting reed baskets around a plastered corner',
    centerSubject: 'seal cutters and carriers converging beneath a cone-mosaic facade',
    rightSubject: 'a loaded donkey pressing through the market lane',
  };
  const denseOptions = {
    phase: 'morning',
    location: 'Uruk',
    coordinates: { lat: 31.3222, lng: 45.6361 },
    year: -3200,
    mode: 'wide-field',
    aspect: '16:9',
  };
  const densePrompt = promptcraft.buildImagePromptsFromDirection(denseOptions, denseDirection)[1];
  assert.ok(densePrompt.includes('The frame is crowded. People fill it at every distance'));
  assert.ok(densePrompt.includes('Every visible material, garment, tool and structure carries'));

  const custom = promptcraft.buildImagePromptsFromDirection(
    { ...denseOptions, template: 'CUSTOM {subject} :: {unknown}' },
    denseDirection,
  )[0];
  assert.ok(custom.startsWith('CUSTOM '));
  assert.ok(custom.includes('{unknown}'));
  assert.equal(count(custom, 'The frame is crowded.'), 1);
  assert.equal(count(custom, 'Every visible material, garment, tool and structure carries'), 1);
  pass('real still compiler: wild, dense, and custom-template behavior');

  const cinematicPrompt = promptcraft.buildCinematicPromptFromDirection(
    { ...wildOptions, mode: 'cinematic' },
    wildDirection,
  );
  assert.ok(cinematicPrompt.includes('Midnight.'));
  assert.ok(cinematicPrompt.includes('Viewpoint: ' + wildDirection.cameraNotes + '.'));
  assert.ok(cinematicPrompt.includes('Diegetic sound from the scene: ' + wildDirection.cinematicSoundCue + '.'));
  assert.ok(!cinematicPrompt.includes('No music'));
  assert.ok(!cinematicPrompt.includes('no narration'));
  assert.ok(
    !/\b(garment|tool|crowd|smartphone|frescoed|walnut|gas-lamp)\b/i.test(cinematicPrompt),
    'Wild cinematic prompt leaked peopled era matter',
  );
  pass('real cinematic compiler: hour, viewpoint, sound, and wild gate');
} finally {
  await server.close();
}

process.stdout.write('RESULT verified candidate at ' + manifest.source.commit + '\n');
