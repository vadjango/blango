function resolvedCallback(data) {
  console.log("Resolved with data: " + data);
}

function rejectedCallback(message) {
  console.log("Rejected with message: " + message)
}

const lazyAdd = (a, b) => {
  const addNum = (resolve, reject) => {
    if (typeof a !== "number" || typeof b !== "number") {
      reject("Both arguments should be numbers!");
    } else {
      resolve(a + b);
    }
  }
  return new Promise(addNum)
}

const p = lazyAdd(2, 3);

p.then(resolvedCallback, rejectedCallback);
lazyAdd("nan", "lol").then(resolvedCallback, rejectedCallback)
