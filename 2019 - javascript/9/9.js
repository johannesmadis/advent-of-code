import { IntCode } from './IntCode';
import { input } from './input';

const test3 = new IntCode({ memory: input });

console.log('test3', test3.run(2));
