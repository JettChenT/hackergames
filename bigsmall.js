for (let value of state.values) {
  if (value[0] > value[1]) {
    state.inputs.push(">");
  } else {
    state.inputs.push("<");
  }
}
console.log("waiting....");
setTimeout(() => {
  submit(state.inputs);
}, 5000);
