const OP_CODE_END = 99;
const OP_CODE_ADD = 1;
const OP_CODE_MULTIPLY = 2;
const OP_CODE_INPUT = 3;
const OP_CODE_OUTPUT = 4;
const OP_CODE_JUMP_IF_TRUE = 5;
const OP_CODE_JUMP_IF_FALSE = 6;
const OP_CODE_LESS_THAN = 7;
const OP_CODE_EQUALS = 8;
const OP_CODE_SET_RELATIVE_BASE = 9;
const MODE_POSITION = 0;
const MODE_IMMEDIATE = 1;
const MODE_RELATIVE = 2;

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
  constructor({ memory, initialInput, pauseAfterOutput }) {
    this.reset(memory, initialInput, pauseAfterOutput);
  }

  reset(memory, initialInput, pauseAfterOutput = false) {
    this.terminated = false;
    this.outputValue = [];
    this.inputs = [];
    this.opIndex = 0;
    this.memory = [...memory];
    this.relativeBase = 0;
    this.pauseAfterOutput = pauseAfterOutput;
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
    this.outputValue.push(outputValue);
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

  setRelativeBase(newBase) {
    this.relativeBase += newBase;
    this.opIndex += 2;
  }

  getInputIndex(mode, index) {
    switch (mode) {
      case MODE_RELATIVE:
        return this.memory[index] + this.relativeBase || 0;
      case MODE_POSITION:
      case MODE_IMMEDIATE:
      default:
        return this.memory[index] || 0;
    }
  }

  getInput(mode, index) {
    switch (mode) {
      case MODE_IMMEDIATE:
        return index || 0;
      case MODE_RELATIVE:
      case MODE_POSITION:
      default:
        return this.memory[index] || 0;
    }
  }

  run(input) {
    if (input !== undefined) this.inputs.push(input);
    this.outputValue = [];

    let stopped = false;
    while (!this.terminated && !stopped) {
      const op = this.memory[this.opIndex];
      const { parameterModes, opCode } = getParameterModes(op);

      const primaryInputIndex = this.getInputIndex(
        parameterModes[0],
        this.opIndex + 1,
      );
      const secondaryInputIndex = this.getInputIndex(
        parameterModes[1],
        this.opIndex + 2,
      );
      const outputIndex = this.getInputIndex(
        parameterModes[2],
        this.opIndex + 3,
      );

      const primaryInput = this.getInput(parameterModes[0], primaryInputIndex);

      const secondaryInput = this.getInput(
        parameterModes[1],
        secondaryInputIndex,
      );
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
          stopped = this.pauseAfterOutput;
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
        case OP_CODE_SET_RELATIVE_BASE: {
          this.setRelativeBase(primaryInput);
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
