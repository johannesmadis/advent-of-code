const { input } = require('./input');
const Robot = require('./Robot');

const COLORS = { BLACK: 0, WHITE: 1 };

const robot = new Robot(input, COLORS.WHITE);

const map = robot.run();

const sum = Object.values(map).reduce((totalSum, row) => {
  const localSum = Object.values(row).length;
  return totalSum + localSum;
}, 0);

const drawMap = () => {
  // find max x and y and min x and y,
  const mapEntries = Object.entries(map);
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  mapEntries.forEach(([rowIndex, row]) => {
    const nrY = Number(rowIndex);
    if (nrY > maxY) maxY = nrY;
    if (nrY < minY) minY = nrY;

    const rowEntries = Object.keys(row);
    rowEntries.forEach((key) => {
      const nrX = Number(key);
      if (nrX > maxX) maxX = nrX;
      if (nrX < minX) minX = nrX;
    });
  });

  for (let i = maxY; i >= minY; i -= 1) {
    let rowStr = '';
    for (let n = minX; n <= maxX; n += 1) {
      const char = map[i] && map[i][n];
      rowStr += char === COLORS.WHITE ? '##' : '  ';
    }
    console.log(rowStr);
  }
};
console.log('map', robot.tileCounter, sum);

drawMap();
