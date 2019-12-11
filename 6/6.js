const { orbitInputs } = require('./6_input.js');

const CENTER_OF_MASS = { name: 'COM', parentCount: 0 };
const DESTINATION = { name: 'SAN', parentCount: 0 };
const start = 'YOU';

const inputArray = orbitInputs.split('\n');

const childrenMap = {};
const regexp = /(.+)\)(.+)/;

const mappedInput = inputArray.map((relation) => {
  const [, left, right] = relation.match(regexp);
  return { left, right };
});

mappedInput.forEach(({ left, right }) => {
  const leftArray = childrenMap[left] || [];
  leftArray.push({ name: right });
  childrenMap[left] = leftArray;
});

// count parents indirect orbits recursively

const countIndirect = ({ name, parents = [] }) => {
  const children = childrenMap[name];
  if (children) {
    children.forEach((child) => {
      child.parents = [...parents, name];

      countIndirect(child);
    });
  }
};
countIndirect(CENTER_OF_MASS);

const sum = ({ name, parents = [] }) => {
  const children = childrenMap[name] || [];
  const sumChildren = children.reduce((result, child) => {
    const childSum = sum(child);
    return result + childSum;
  }, 0);
  return sumChildren + parents.length;
};

const findAncestor = (a, b) => {
  const childrenArray = Object.values(childrenMap);
  const [objectA] = childrenArray.find((children) => children.find((child) => child.name === a));
  const [objectB] = childrenArray.find((children) => children.find((child) => child.name === b));

  if (objectA && objectB) {
    console.log('ob', objectA, objectB);
    const objectBParents = [...objectB.parents].reverse();
    const commonAncestor = [...objectA.parents]
      .reverse()
      .find((aParent) => objectBParents.find((bParent) => bParent === aParent));
    return commonAncestor;
  }
  return false;
};

const commonAncestor = findAncestor('SAN', 'YOU');
console.log(commonAncestor);

const childrenArray = Object.values(childrenMap);
const [santa] = childrenArray.find((children) => children.find((child) => child.name === 'SAN'));
const [you] = childrenArray.find((children) => children.find((child) => child.name === 'YOU'));
const [ancestor] = childrenArray.find((children) => children.find((child) => child.name === commonAncestor));

if (santa && you && ancestor) {
  console.log(
    santa.parents.length + you.parents.length - 2 * ancestor.parents.length - 2,
  );
}

// console.log(sum(CENTER_OF_MASS));

// find ancestor
// find santa,
// find you;
// santa + you - 2ancestor parentcount -2
