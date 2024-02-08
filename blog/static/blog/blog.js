for (let i = 0; i < 10; i++) {
  console.log("For-loop counter: " + i);
}

let j = 0;
while (j < 10) {
  console.log("While-loop j: " + j);
  j += 1;
}

let k = 10;

do {
  console.log("do-while loop k: " + k);
} while (k < 10);

const numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

numbers.forEach((value) => {console.log("Element: " + value)});
const squared = numbers.map(value => value ** 2);
console.log(squared);