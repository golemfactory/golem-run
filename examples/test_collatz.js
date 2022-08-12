function collatz(initial) {
  let x = initial;
  let top_value = initial;
  let iters = 0;
  while (Math.round(x) !== 1) {
    if(x % 2 === 0) {
      x = x / 2
    } else {
      x = 3 * x + 1
    }
    iters += 1;
    if(x > top_value) {
      top_value = x
    }
  }
  console.log(`[${initial}]: Found; max=${top_value},iters=${iters}`)
}

for (let i = parseInt(process.argv[2]); i < parseInt(process.argv[3]); i++) {
  collatz(i);
}