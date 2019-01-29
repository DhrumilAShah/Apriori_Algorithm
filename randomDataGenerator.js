function makeid() {
  var text = "";
  var possible = "ABCDEFGHIJ";

  for (var i = 0; i < (Math.round(Math.random() * 10)); i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));

  return text;
}

console.log(makeid());
