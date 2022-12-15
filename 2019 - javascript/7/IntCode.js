const OP_CODE_END = 99;
const OP_CODE_ADD = 1;
const OP_CODE_MULTIPLY = 2;
const OP_CODE_INPUT = 3;
const OP_CODE_OUTPUT = 4;
const OP_CODE_JUMP_IF_TRUE = 5;
const OP_CODE_JUMP_IF_FALSE = 6;
const OP_CODE_LESS_THAN = 7;
const OP_CODE_EQUALS = 8;

const getParameterModes = (op) => {
  const stringArray = String(op).split('');
  // start from last two as opcode:
  const opStrings = stringArray.splice(-2, 2);
  let opCode = '';
  for (let i = 0; i < opStrings.length; i += 1) {
    opCode += opStrings[i];
  }
  const parameterModes = stringArray.map((mode) => Number(mode)).reverse();
  return { opCode: Number(opCode), parameterModes };
};

class IntCode {
  constructor({ memory, initialInput }) {
    this.reset(memory, initialInput);
  }

  reset(memory, initialInput) {
    this.terminated = false;
    this.outputValue = null;
    this.inputs = [];
    this.opIndex = 0;
    this.memory = [...memory];
    if (initialInput !== undefined) this.inputs.push(initialInput);
  }

  multiply(input1, input2, outputIndex) {
    this.memory[outputIndex] = input1 * input2;

    this.opIndex += 4;
  }

  add(input1, input2, outputIndex) {
    this.memory[outputIndex] = input1 + input2;

    this.opIndex += 4;
  }

  input(index) {
    const value = this.inputs.shift();
    this.memory[index] = value;
    this.opIndex += 2;
  }

  output(outputValue) {
    this.outputValue = outputValue;
    this.opIndex += 2;
  }

  jumpIfTrue(input1, input2) {
    if (input1) {
      this.opIndex = input2;
    } else {
      this.opIndex += 3;
    }
  }

  jumpIfFalse(input1, input2) {
    if (!input1) {
      this.opIndex = input2;
    } else {
      this.opIndex += 3;
    }
  }

  lessThan(input1, input2, outputIndex) {
    this.memory[outputIndex] = input1 < input2 ? 1 : 0;

    this.opIndex += 4;
  }

  equals(input1, input2, outputIndex) {
    this.memory[outputIndex] = input1 === input2 ? 1 : 0;

    this.opIndex += 4;
  }

  run(input) {
    this.inputs.push(input);
    this.outputValue = null;

    let stopped = false;
    while (!this.terminated && !stopped) {
      const op = this.memory[this.opIndex];
      const { parameterModes, opCode } = getParameterModes(op);

      const primaryInputIndex = this.memory[this.opIndex + 1];
      const secondaryInputIndex = this.memory[this.opIndex + 2];
      const outputIndex = this.memory[this.opIndex + 3];

      const primaryInput = parameterModes[0]
        ? primaryInputIndex
        : this.memory[primaryInputIndex];
      const secondaryInput = parameterModes[1]
        ? secondaryInputIndex
        : this.memory[secondaryInputIndex];

      switch (Number(opCode)) {
        case OP_CODE_ADD:
          this.add(primaryInput, secondaryInput, outputIndex);
          break;

        case OP_CODE_MULTIPLY:
          this.multiply(primaryInput, secondaryInput, outputIndex);
          break;

        case OP_CODE_INPUT: {
          this.input(primaryInputIndex);
          break;
        }
        case OP_CODE_OUTPUT: {
          this.output(Number(primaryInput));
          stopped = true;
          break;
        }
        case OP_CODE_JUMP_IF_TRUE: {
          this.jumpIfTrue(primaryInput, secondaryInput);
          break;
        }
        case OP_CODE_JUMP_IF_FALSE: {
          this.jumpIfFalse(primaryInput, secondaryInput);
          break;
        }
        case OP_CODE_LESS_THAN: {
          this.lessThan(primaryInput, secondaryInput, outputIndex);
          break;
        }
        case OP_CODE_EQUALS: {
          this.equals(primaryInput, secondaryInput, outputIndex);
          break;
        }
        case OP_CODE_END: {
          this.terminated = true;
          break;
        }
        default: {
          console.log('something wrong', opCode, op);
          this.terminated = true;
        }
      }
    }
    return this.outputValue;
  }
}
exports.IntCode = IntCode;
