const evaluateCondition = (condition, data) => {
  const { not, key, value } = condition;

  return not ? data[key] !== value : data[key] === value;
};

const evaluate = (group, data) => {
  const { or, list } = group;

  if (or) {
    return list.some((condition) => (condition.isGroup
      ? evaluate(condition, data)
      : evaluateCondition(condition, data)));
  }

  return list.every((condition) => (condition.isGroup
    ? evaluate(condition, data)
    : evaluateCondition(condition, data)));
};

const condition = {
  key: 'Group',
  value: 'A',
  not: false,
  isCondition: true,
};
const group = { or: false, list: [condition, condition], isGroup: true };

const group2 = { or: true, list: [group, condition] };

const data = { Group: 'A' };

console.log(evaluate(group2, data));
