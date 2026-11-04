const vm = require('node:vm');
const { selectElectronContext } = require('../../tools/desktop_smoke.cjs');

test('selects the Electron browser context instead of the default Node embedding context', async () => {
  const contexts = new Map([
    [1, vm.createContext({ process: { versions: {}, type: undefined } })],
    [2, vm.createContext({ process: { type: 'renderer', resourcesPath: '/renderer' } })],
    [3, vm.createContext({ process: { type: 'browser', resourcesPath: '/app/resources' } })],
  ]);
  const selected = await selectElectronContext(contexts.keys(), (expression, id) => vm.runInContext(expression, contexts.get(id)));
  expect(selected).toBe(3);
});

test('keeps waiting if no initialized Electron browser context exists', async () => {
  const context = vm.createContext({ process: { type: 'browser' } });
  expect(await selectElectronContext([1], expression => vm.runInContext(expression, context))).toBeUndefined();
});

test('a destroyed context does not hide a later initialized context', async () => {
  const context = vm.createContext({ process: { type: 'browser', resourcesPath: '/app/resources' } });
  const selected = await selectElectronContext([1, 2], (expression, id) => {
    if (id === 1) throw new Error('Cannot find context with specified id');
    return vm.runInContext(expression, context);
  });
  expect(selected).toBe(2);
});
