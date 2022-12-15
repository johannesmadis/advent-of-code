const { initialMemory } = require('./2_inputs');

const OP_CODE_END = 99;
const OP_CODE_ADD = 1;
const OP_CODE_MULTIPLY = 2;
const START_INDEX = 0;

const multiply = (
  input,
  primaryInputIndex,
  secondaryInputIndex,
  outputIndex,
) => {
  input[outputIndex] = input[primaryInputIndex] * input[secondaryInputIndex];
};

const add = (input, primaryInputIndex, secondaryInputIndex, outputIndex) => {
  input[outputIndex] = input[primaryInputIndex] + input[secondaryInputIndex];
};

const gravity = (index, input) => {
  const opCode = input[index];
  const primaryInputIndex = input[index + 1];
  const secondaryInputIndex = input[index + 2];
  const outputIndex = input[index + 3];

  switch (opCode) {
    case OP_CODE_ADD:
      add(input, primaryInputIndex, secondaryInputIndex, outputIndex);
      return gravity(index + 4, input);
    case OP_CODE_MULTIPLY:
      multiply(input, primaryInputIndex, secondaryInputIndex, outputIndex);
      return gravity(index + 4, input);
    case OP_CODE_END:
      console.log('End', index);
      return undefined;
    default:
      return console.log('Something wrong');
  }
};

const EXPECTED_OUTPUT = 19690720;
const RANGE_MIN = 0;
const RANGE_MAX = 100;
const NOUN_INDEX = 1;
const VERB_INDEX = 2;

const findInputs = (expected, min, max) => {
  for (let noun = min; noun < max; noun += 1) {
    for (let verb = min; verb < max; verb += 1) {
      const inputArray = [...initialMemory];
      inputArray[NOUN_INDEX] = noun;
      inputArray[VERB_INDEX] = verb;

      gravity(START_INDEX, inputArray);
      console.log(noun, verb, inputArray[0]);

      if (inputArray[0] === EXPECTED_OUTPUT) {
        return [noun, verb];
      }
    }
  }
  return [NaN, NaN];
};

const [noun, verb] = findInputs(EXPECTED_OUTPUT, RANGE_MIN, RANGE_MAX);

console.log('Result', noun, verb);
