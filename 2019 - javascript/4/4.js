const INPUT_MAX = 652527;
const INPUT_LOW = 156218;

const suitors = [];

for (let i = INPUT_LOW; i <= INPUT_MAX; i += 1) {
  const arrInput = [...String(i)].map((n) => Number(n));
  let isGrowing = true;
  let hasUniqueDouble = false;
  for (let a = 0; a < 6; a += 1) {
    if (arrInput[a] < arrInput[a - 1]) {
      isGrowing = false;
      break;
    }
    if (
      arrInput[a] === arrInput[a + 1]
      && arrInput[a] !== arrInput[a + 2]
      && arrInput[a] !== arrInput[a - 1]
    ) {
      hasUniqueDouble = true;
    }
  }
  if (isGrowing && hasUniqueDouble) {
    suitors.push(i);
  }
}

console.log('suitor', suitors.length, suitors);
