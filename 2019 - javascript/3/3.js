/* eslint-disable no-param-reassign */
const { inputString } = require('./3_input_mock');

const OP_CODE_UP = 'U';
const OP_CODE_RIGHT = 'R';
const OP_CODE_LEFT = 'L';
const OP_CODE_DOWN = 'D';

const getDirections = (input) => {
  const inputs = input.split('\n');
  return inputs.map((line) => line.split(','));
};

const [firstLine, secondLine] = getDirections(inputString);

const positionsFirst = [];
const positionsFirstMap = {};
const positionsSecond = [];
const positionsSecondMap = {};

const calculatePositions = (arr, map) => (op) => {
  const opCode = op.substr(0, 1);
  const length = Number(op.substr(1));
  const prevPos = arr[arr.length - 1] || [0, 0];

  for (let i = 1; i <= length; i += 1) {
    let x;
    let y;
    switch (opCode) {
      case OP_CODE_UP:
        [x] = prevPos;
        y = prevPos[1] + i;
        break;
      case OP_CODE_DOWN:
        [x] = prevPos;
        y = prevPos[1] - i;
        break;
      case OP_CODE_RIGHT:
        x = prevPos[0] + i;
        [, y] = prevPos;
        break;
      case OP_CODE_LEFT:
        x = prevPos[0] - i;
        [, y] = prevPos;
        break;
      default:
        break;
    }

    arr.push([x, y]);
    map[x] = map[x] || {};
    map[x][y] = map[x][y] || arr.length;
  }
};

firstLine.forEach(calculatePositions(positionsFirst, positionsFirstMap));
secondLine.forEach(calculatePositions(positionsSecond, positionsSecondMap));

const intersections = [];
positionsFirst.forEach((position) => {
  const [x, y] = position;
  if (positionsSecondMap[x] && positionsSecondMap[x][y] !== undefined) {
    intersections.push(position);
  }
});
/*
const manhattans = intersections.map(([x, y]) => Math.abs(x) + Math.abs(y));
*/

const distances = intersections.map((intersection) => {
  const [x, y] = intersection;
  const lengthFirst = positionsFirstMap[x][y];
  const lengthSecond = positionsSecondMap[x][y];
  return lengthFirst + lengthSecond;
});

// distances.sort((a, b) => a - b);

let max = Infinity;
distances.forEach((distance) => {
  if (distance < max) {
    max = distance;
  }
});

console.log('distances', max);
