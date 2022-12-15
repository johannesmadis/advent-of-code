const { initialMemory, INPUT } = require('./5_input');

const OP_CODE_END = 99;
const OP_CODE_ADD = 1;
const OP_CODE_MULTIPLY = 2;
const OP_CODE_INPUT = 3;
const OP_CODE_OUTPUT = 4;
const OP_CODE_JUMP_IF_TRUE = 5;
const OP_CODE_JUMP_IF_FALSE = 6;
const OP_CODE_LESS_THAN = 7;
const OP_CODE_EQUALS = 8;
const START_INDEX = 0;

const multiply = (input, input1, input2, outputIndex) => {
  input[outputIndex] = input1 * input2;
};

const add = (input, input1, input2, outputIndex) => {
  input[outputIndex] = input1 + input2;
};

const set = (input, index) => {
  input[index] = INPUT;
};

const get = (input1) => input1;

const jumpIfTrue = (input1, input2, fallBackIndex) => {
  if (input1) {
    return input2;
  }
  return fallBackIndex + 3;
};

const jumpIfFalse = (input1, input2, fallBackIndex) => {
  if (!input1) {
    return input2;
  }
  return fallBackIndex + 3;
};

const lessThan = (input, input1, input2, outputIndex) => {
  input[outputIndex] = input1 < input2 ? 1 : 0;
};

const equals = (input, input1, input2, outputIndex) => {
  input[outputIndex] = input1 === input2 ? 1 : 0;
};

const getParameterModes = (op) => {
  const stringArray = [...String(op)];
  // start from last two as opcode:
  const opCode = Number(stringArray.splice(-2, 2).join(''));
  const parameterModes = stringArray.map((mode) => Number(mode)).reverse();
  return { opCode, parameterModes };
};

const intCode = (index, input) => {
  const op = input[index];
  const { parameterModes, opCode } = getParameterModes(op);

  const primaryInputIndex = input[index + 1];
  const secondaryInputIndex = input[index + 2];
  const tertiaryInputIndex = input[index + 3];

  const primaryInput = parameterModes[0]
    ? primaryInputIndex
    : input[primaryInputIndex];
  const secondaryInput = parameterModes[1]
    ? secondaryInputIndex
    : input[secondaryInputIndex];

  switch (opCode) {
    case OP_CODE_ADD:
      add(input, primaryInput, secondaryInput, tertiaryInputIndex);
      return intCode(index + 4, input);
    case OP_CODE_MULTIPLY:
      multiply(input, primaryInput, secondaryInput, tertiaryInputIndex);
      return intCode(index + 4, input);
    case OP_CODE_INPUT: {
      set(input, primaryInputIndex);
      return intCode(index + 2, input);
    }
    case OP_CODE_OUTPUT: {
      const value = get(primaryInput);
      console.log('output', value);
      return intCode(index + 2, input);
    }
    case OP_CODE_JUMP_IF_TRUE: {
      const newPointer = jumpIfTrue(primaryInput, secondaryInput, index);
      return intCode(newPointer, input);
    }
    case OP_CODE_JUMP_IF_FALSE: {
      const newPointer = jumpIfFalse(primaryInput, secondaryInput, index);
      return intCode(newPointer, input);
    }
    case OP_CODE_LESS_THAN: {
      lessThan(input, primaryInput, secondaryInput, tertiaryInputIndex);
      return intCode(index + 4, input);
    }
    case OP_CODE_EQUALS: {
      equals(input, primaryInput, secondaryInput, tertiaryInputIndex);
      return intCode(index + 4, input);
    }
    case OP_CODE_END:
      console.log('End', index);
      return undefined;
    default:
      return console.log('Something wrong');
  }
};

intCode(START_INDEX, initialMemory);
