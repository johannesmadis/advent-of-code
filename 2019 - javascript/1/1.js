const { inputs } = require('./1_inputs');

const calculateAdditionalFuel = (initialFuel) => {
  const fuelFuel = Math.floor(initialFuel / 3) - 2;
  if (fuelFuel < 1) {
    return 0;
  }
  return fuelFuel + calculateAdditionalFuel(fuelFuel);
};

const calculateMass = (modules) => modules.reduce((totalFuel, moduleMass) => {
  const moduleFuel = Math.floor(moduleMass / 3) - 2;
  const additionalFuel = calculateAdditionalFuel(moduleFuel);
  return totalFuel + moduleFuel + additionalFuel;
}, 0);

const totalMass = calculateMass(inputs);
console.log('totalMass', totalMass);
