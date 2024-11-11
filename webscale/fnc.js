let cmds = {
  getsource: "cat server.js",
  test: "echo 'hello, world!'",
};

let store = {};

const st = (key, value) => {
  const keys = key.split(".");
  let current = store;

  for (let i = 0; i < keys.length - 1; i++) {
    const key = keys[i];
    if (!current[key]) {
      current[key] = {};
    }
    current = current[key];
  }

  // Set the value at the last key
  current[keys[keys.length - 1]] = value;
};

const exc = (query) => {
  const key = query.cmd;
  const cmd = cmds[key];
  console.log("executing", cmd);
};
