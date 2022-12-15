const md5 = require('md5');

const Moon = require('./Moon');
const { input } = require('./input');

const test = `<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>`;

const regexp = /<x=(.+), y=(.+), z=(.+)>/;
const makeMoons = (data) => data.split(/\n\r?/g).map((moonRow, index) => {
  const matches = moonRow.match(regexp);
  const [, x, y, z] = matches;
  return new Moon(index, Number(x), Number(y), Number(z));
});
const moons = makeMoons(input);

const applyGravity = () => {
  moons.forEach((moon) => {
    const d = { x: 0, y: 0, z: 0 };

    moons.forEach((otherMoon) => {
      if (moon.id !== otherMoon.id) {
        ['x', 'y', 'z'].forEach((axis) => {
          if (moon[axis] > otherMoon[axis]) {
            d[axis] -= 1;
          } else if (moon[axis] < otherMoon[axis]) {
            d[axis] += 1;
          }
        });
      }
    });

    moon.applyGravity(d.x, d.y, d.z);
  });
};
/*
const steps = 1000;

for (let i = 0; i < steps; i += 1) {
  applyGravity();
  moons.forEach((moon) => moon.updatePosition());
}
const totalEnergies = moons.map((moon) => moon.getTotalEnergy());

console.log('moons', moons, totalEnergies.reduce((a, b) => a + b, 0));
*/
// history

const arrCompare = (a, b) => a.length === b.length && a.every((value, index) => value === b[index]);

const makeLocalHistory = (moon) => {
  const {
    x, y, z, vX, vY, vZ,
  } = moon;
  return `${x} ${y} ${z} ${vX} ${vY} ${vZ}`;
};

let i = 0;

const initialpX = moons.map((moon) => moon.x);
const initialpY = moons.map((moon) => moon.y);
const initialpZ = moons.map((moon) => moon.z);
const initialvX = moons.map((moon) => moon.vX);
const initialvY = moons.map((moon) => moon.vY);
const initialvZ = moons.map((moon) => moon.vZ);

// periods
let pX;
let pY;
let pZ;
let pVX;
let pVY;
let pVZ;

while (pX === undefined || pY === undefined || pZ === undefined) {
  i += 1;

  applyGravity();
  moons.forEach((moon) => {
    moon.updatePosition();
  });
  const currentpX = moons.map((moon) => moon.x);
  const currentpY = moons.map((moon) => moon.y);
  const currentpZ = moons.map((moon) => moon.z);
  const currentvX = moons.map((moon) => moon.vX);
  const currentvY = moons.map((moon) => moon.vY);
  const currentvZ = moons.map((moon) => moon.vZ);

  if (
    arrCompare(currentpX, initialpX)
    && arrCompare(currentvX, initialvX)
    && pX === undefined
  ) {
    pX = i;
  }
  if (
    arrCompare(currentpY, initialpY)
    && arrCompare(currentvY, initialvY)
    && pY === undefined
  ) {
    pY = i;
  }
  if (
    arrCompare(currentpZ, initialpZ)
    && arrCompare(currentvZ, initialvZ)
    && pZ === undefined
  ) {
    pZ = i;
  }
}

console.log('history repeats', pX, pY, pZ);

161427;
113027;
231613;
